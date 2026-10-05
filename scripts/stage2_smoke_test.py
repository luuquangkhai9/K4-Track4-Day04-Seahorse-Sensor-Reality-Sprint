"""Reproduce S01 clean on CPU/GPU with frozen DRIVE-C code; save evidence."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
ZIP_URL = "https://zenodo.org/records/19656444/files/drivec_core_v1.zip?download=1"


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / ".lab_cache/drive-c-source")
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "drive-c-dataset/checkpoints/epoch_021_best.pth")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/stage2")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("--threads must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((ROOT / "configs/benchmark.json").read_text(encoding="utf-8"))
    manifest = {
        "started_at": datetime.now(timezone(timedelta(hours=7))).isoformat(),
        "stage": 2, "sample_id": "S01_clean", "status": "running",
        "python": platform.python_version(), "device_requested": "automatic CUDA or CPU",
        "config_sha256": sha256(ROOT / "configs/benchmark.json"),
        "dataset_url": ZIP_URL,
        "scope": "one clean clip, eight frames; not the full 24-clip benchmark",
    }
    log_path = args.output / "run.log"
    with log_path.open("w", encoding="utf-8") as log:
        def say(message):
            print(message, flush=True)
            log.write(message + "\n")
            log.flush()

        try:
            # A real nested clone is required, not a parent repository commit.
            if not (args.source / ".git").exists():
                raise RuntimeError("Source must be a separate clone of the frozen DRIVE-C tag.")
            commit = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
            if commit != cfg["model"]["expected_commit_from_saved_notebook"]:
                raise RuntimeError(f"Unexpected source commit: {commit}")
            dirty = subprocess.check_output(["git", "-C", str(args.source), "status", "--porcelain", "--untracked-files=no"], text=True).strip()
            if dirty:
                raise RuntimeError("Frozen source has tracked modifications; inspect before reproducing.")
            manifest.update(source_url=cfg["model"]["source_url"], source_commit=commit, source_tracked_clean=True)
            tracked = subprocess.check_output(["git", "-C", str(args.source), "ls-files"], text=True).splitlines()
            selected = [p for p in tracked if p.endswith((".py", ".yaml")) and (args.source / p).is_file()]
            manifest["source_hash_scope"] = "tracked Python/YAML files materialized in this checkout; sparse omitted files not hashed"
            manifest["source_file_sha256"] = {p: sha256(args.source / p) for p in selected}
            ckpt_hash = sha256(args.checkpoint)
            if ckpt_hash != cfg["model"]["checkpoint_sha256"]:
                raise RuntimeError("Checkpoint SHA-256 mismatch")
            manifest["checkpoint_sha256"] = ckpt_hash
            say(f"Frozen source/checkpoint verified: {commit}")

            import cv2
            import numpy as np
            import torch
            import torchvision
            from remotezip import RemoteZip

            manifest["versions"] = {p: importlib.metadata.version(p) for p in ["torch", "torchvision", "numpy", "opencv-python-headless", "remotezip", "requests", "PyYAML"]}
            torch.set_num_threads(args.threads)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            manifest.update(device=str(device), cpu_threads=torch.get_num_threads())
            say(f"Imports OK, device={device}, CPU threads={torch.get_num_threads()}")

            expected_zip_name = None
            expected_video_hash = None
            for line in (ROOT / "fetch_sha256.txt").read_text(encoding="utf-8").splitlines():
                digest, name = line.split(maxsplit=1)
                if re.search(r"/clean_clips/S01_.*clean\.mp4$", name):
                    expected_zip_name, expected_video_hash = name, digest
            if expected_zip_name is None:
                raise RuntimeError("Cannot identify S01 clean in saved clip hash manifest")
            video = ROOT / ".lab_cache/data" / expected_zip_name
            video.parent.mkdir(parents=True, exist_ok=True)
            if not video.exists():
                say("Fetching only S01 clean from the remote ZIP (no full archive download)...")
                t0 = time.perf_counter()
                with RemoteZip(ZIP_URL, timeout=(15, 45)) as remote:
                    payload = remote.read(expected_zip_name)
                # RemoteZip validates ZIP CRC; SHA below checks against the saved run.
                video.write_bytes(payload)
                manifest["download_seconds"] = time.perf_counter() - t0
            video_hash = sha256(video)
            if video_hash != expected_video_hash:
                raise RuntimeError("Video SHA-256 differs from the saved dataset manifest")
            manifest.update(video_zip_entry=expected_zip_name, video_sha256=video_hash, video_bytes=video.stat().st_size)
            say(f"Video verified: {video.stat().st_size / 1e6:.2f} MB")

            cap = cv2.VideoCapture(str(video))
            if not cap.isOpened():
                raise RuntimeError("OpenCV cannot decode the baseline MP4")
            video_info = {"frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), "fps": cap.get(cv2.CAP_PROP_FPS)}
            cap.release()
            if (video_info["frame_count"], video_info["height"], video_info["width"]) != (128, 720, 1280):
                raise RuntimeError(f"Unexpected baseline properties: {video_info}")
            manifest["video_properties"] = video_info

            sys.path.insert(0, str(args.source / "scripts"))
            import add_gshi_pred as G
            if Path(G.__file__).resolve() != (args.source / "scripts/add_gshi_pred.py").resolve():
                raise RuntimeError("Imported the wrong inference module")
            frames = G.read_sampled_frames(video, num_frames=8)
            indices = G.sample_frame_indices(video_info["frame_count"], 8)
            assert indices == cfg["dataset"]["sample_frame_indices_zero_based"]
            assert len(frames) == 8
            H, W = cfg["model"]["input"]["height"], cfg["model"]["input"]["width"]
            t0 = time.perf_counter()
            model = G.load_model(args.checkpoint, device, H, W, pretrained_backbone=False)
            manifest["model_load_seconds"] = time.perf_counter() - t0
            say(f"Strict checkpoint load OK in {manifest['model_load_seconds']:.2f}s; running 8-frame batch...")
            x = torch.from_numpy(np.stack([G.preprocess_frame(f, H, W, "resize") for f in frames])).to(device)
            if device.type == "cuda":
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            with torch.inference_mode():
                output = model(x)
            if device.type == "cuda":
                torch.cuda.synchronize()
            elapsed = time.perf_counter() - t0
            health = output["pred_health"].reshape(-1).cpu().numpy()
            if not np.isfinite(health).all() or ((health < 0) | (health > 1)).any():
                raise RuntimeError("Invalid health output")
            manifest.update(frame_indices=indices, input_preprocessing=cfg["model"]["input"], eval_mode=not model.training, inference_batch_size=8, forward_seconds=elapsed)
            with (args.output / "baseline_per_frame.csv").open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["sample_id", "frame_idx", "gshi_pred"])
                writer.writeheader()
                for index, value in zip(indices, health):
                    writer.writerow(dict(sample_id="S01_clean", frame_idx=index, gshi_pred=float(value)))
            with (args.source / "dataset/final_metadata.csv").open(encoding="utf-8-sig", newline="") as stream:
                row = next(r for r in csv.DictReader(stream) if r["sample_id"] == "S01_clean")
            actual, author = float(health.mean()), float(row["gshi_pred"])
            error = abs(actual - author)
            j = indices.index(54)
            g = cv2.cvtColor(frames[j], cv2.COLOR_RGB2GRAY)
            p = np.bincount(g.ravel(), minlength=256) / g.size
            p = p[p > 0]
            metrics = dict(B=float(cv2.Laplacian(g, cv2.CV_64F).var()), S_pct=float(((g <= 5) | (g >= 250)).mean() * 100), H_bit=float(-(p * np.log2(p)).sum()))
            image_path = args.output / "S01_clean_f54.png"
            if not cv2.imwrite(str(image_path), cv2.cvtColor(frames[j], cv2.COLOR_RGB2BGR)):
                raise RuntimeError("Failed to save baseline image")
            manifest.update(health_f54=float(health[j]), health_mean8=actual, author_health_mean8=author, max_allowed_abs_error_exclusive=0.001, abs_error=error, handcrafted_f54=metrics, estimated_24_clip_forward_seconds=24 * elapsed, estimation_note="Extrapolation from one 8-frame batch, excludes download/decode/setup; not a runtime benchmark")
            say(f"S01 clean: frame54={health[j]:.6f}, mean8={actual:.6f}, author={author:.6f}, abs_error={error:.8f}")
            say(f"8-frame forward={elapsed:.2f}s; 24-clip forward-only estimate={24 * elapsed:.1f}s")
            if error >= 0.001:
                raise RuntimeError("Reproduction error exceeds the fixed tolerance")
            manifest["status"] = "pass"
            say("PASS: real clean baseline reproduced; ready to attempt stage 3 on this CPU.")
        except Exception as exc:
            manifest.update(status="failed", error=str(exc))
            say(traceback.format_exc())
        finally:
            manifest["finished_at"] = datetime.now(timezone(timedelta(hours=7))).isoformat()
            (args.output / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if manifest["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
