"""Run four frozen DRIVE-C clips on CPU/GPU, with paired metrics and evidence."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

from stage2_smoke_test import ROOT, ZIP_URL, sha256


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / ".lab_cache/drive-c-source")
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "drive-c-dataset/checkpoints/epoch_021_best.pth")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/stage3_small")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("--threads must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    base_path, small_path = ROOT / "configs/benchmark.json", ROOT / "configs/benchmark_small.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    small = json.loads(small_path.read_text(encoding="utf-8"))
    manifest = {"stage": 3, "scope": small, "status": "running", "python": platform.python_version(),
                "started_at": datetime.now(timezone(timedelta(hours=7))).isoformat(),
                "config_sha256": {"base": sha256(base_path), "small": sha256(small_path)}}
    wall_start = time.perf_counter()
    with (args.output / "run.log").open("w", encoding="utf-8") as log:
        def say(message):
            print(message, flush=True)
            log.write(message + "\n")
            log.flush()

        try:
            if not (args.source / ".git").exists():
                raise RuntimeError("Source must be a separate frozen clone; see STAGE2_REPORT.md")
            commit = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
            dirty = subprocess.check_output(["git", "-C", str(args.source), "status", "--porcelain", "--untracked-files=no"], text=True).strip()
            if commit != base["model"]["expected_commit_from_saved_notebook"] or dirty:
                raise RuntimeError("Source commit/cleanliness check failed")
            if sha256(args.checkpoint) != base["model"]["checkpoint_sha256"]:
                raise RuntimeError("Checkpoint hash mismatch")
            manifest.update(source_commit=commit, source_url=base["model"]["source_url"], source_tracked_clean=True, checkpoint_sha256=sha256(args.checkpoint), dataset_url=ZIP_URL)
            key_files = ["src/models/perception_health_net.py", "scripts/add_gshi_pred.py", "configs/taxonomy/camera_issues.yaml", "dataset/final_metadata.csv"]
            manifest["source_file_sha256"] = {p: sha256(args.source / p) for p in key_files}

            import cv2
            import numpy as np
            import torch
            from remotezip import RemoteZip
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            manifest["versions"] = {p: importlib.metadata.version(p) for p in ["torch", "torchvision", "numpy", "opencv-python-headless", "remotezip", "requests", "PyYAML", "matplotlib"]}
            torch.set_num_threads(args.threads)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            manifest.update(device=str(device), cpu_threads=torch.get_num_threads(), inference_batch_size=8)
            say(f"Small demo: 4 clips, 1 scene, motion blur; device={device}")
            with (args.source / "dataset/final_metadata.csv").open(encoding="utf-8-sig", newline="") as stream:
                metadata = {r["sample_id"]: r for r in csv.DictReader(stream)}
            manifest["corruption_parameters"] = {sid: json.loads(metadata[sid]["extra_json"]) for sid in small["sample_ids"]}
            (args.output / "corruption_parameters.json").write_text(json.dumps(manifest["corruption_parameters"], ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
            manifest["runner_sha256"] = sha256(Path(__file__).resolve())
            hashes = dict(line.split(maxsplit=1)[::-1] for line in (ROOT / "fetch_sha256.txt").read_text().splitlines() if line.strip())
            samples = []
            for sid in small["sample_ids"]:
                hits = [name for name in hashes if ("/clean_clips/S01_" in name and name.endswith("clean.mp4"))] if sid.endswith("_clean") else [name for name in hashes if name.endswith("/" + sid + ".mp4")]
                if len(hits) != 1:
                    raise RuntimeError(f"Cannot resolve dataset hash for {sid}")
                name = hits[0]
                samples.append({"sample_id": sid, "zip_entry": name, "sha256": hashes[name], "path": ROOT / ".lab_cache/data" / name})
            missing = [s for s in samples if not s["path"].exists()]
            t0 = time.perf_counter()
            if missing:
                say(f"Fetching only {len(missing)} missing clips; clean baseline is reused if cached...")
                with RemoteZip(ZIP_URL, timeout=(15, 45)) as remote:
                    for sample in missing:
                        payload = remote.read(sample["zip_entry"])
                        sample["path"].parent.mkdir(parents=True, exist_ok=True)
                        sample["path"].write_bytes(payload)
                        say(f"Fetched {sample['sample_id']}: {len(payload)/1e6:.2f} MB")
            manifest["download_seconds"] = time.perf_counter() - t0
            manifest["downloaded_clip_count"] = len(missing)
            for sample in samples:
                if sha256(sample["path"]) != sample["sha256"]:
                    raise RuntimeError(f"Video hash mismatch: {sample['sample_id']}")
            manifest["videos"] = [{k: v for k, v in s.items() if k != "path"} for s in samples]

            sys.path.insert(0, str(args.source / "scripts"))
            import add_gshi_pred as G
            if Path(G.__file__).resolve() != (args.source / "scripts/add_gshi_pred.py").resolve():
                raise RuntimeError("Wrong inference module imported")
            H, W = base["model"]["input"]["height"], base["model"]["input"]["width"]
            t0 = time.perf_counter()
            model = G.load_model(args.checkpoint, device, H, W, pretrained_backbone=False)
            manifest.update(model_load_seconds=time.perf_counter() - t0, eval_mode=not model.training, preprocessing=base["model"]["input"], handcrafted_metric_config=base["handcrafted_metrics"])
            result, per_frame, images = [], [], []
            for i, sample in enumerate(samples):
                sid, path = sample["sample_id"], sample["path"]
                cap = cv2.VideoCapture(str(path))
                video_info = dict(frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), fps=float(cap.get(cv2.CAP_PROP_FPS)))
                cap.release()
                if (video_info["frames"], video_info["height"], video_info["width"]) != (128, 720, 1280):
                    raise RuntimeError(f"Unexpected video dimensions: {sid}: {video_info}")
                frames = G.read_sampled_frames(path, 8)
                indices = G.sample_frame_indices(video_info["frames"], 8)
                if indices != base["dataset"]["sample_frame_indices_zero_based"] or len(frames) != 8:
                    raise RuntimeError(f"Invalid sampled frames for {sid}")
                x = torch.from_numpy(np.stack([G.preprocess_frame(f, H, W, "resize") for f in frames])).to(device)
                if device.type == "cuda": torch.cuda.synchronize()
                t0 = time.perf_counter()
                with torch.inference_mode(): health = model(x)["pred_health"].reshape(-1).cpu().numpy()
                if device.type == "cuda": torch.cuda.synchronize()
                elapsed = time.perf_counter() - t0
                if not np.isfinite(health).all() or ((health < 0) | (health > 1)).any():
                    raise RuntimeError(f"Invalid health values for {sid}")
                for idx, value in zip(indices, health): per_frame.append(dict(sample_id=sid, frame_idx=idx, gshi_pred=float(value)))
                rgb = frames[indices.index(small["primary_frame_index"])]
                gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
                p = np.bincount(gray.ravel(), minlength=256) / gray.size
                p = p[p > 0]
                meta = metadata[sid]
                severity = float(meta["severity_value"])
                kernel = 0 if sid.endswith("_clean") else int(json.loads(meta["extra_json"])["ksize"])
                if severity != small["severity_values"][i] or kernel != small["blur_kernels_px"][i]:
                    raise RuntimeError(f"Config/metadata mismatch for {sid}")
                row = dict(sample_id=sid, scenario="S01", corruption="clean" if kernel == 0 else "motion_blur", frame_idx=54, severity_value=severity, blur_kernel_px=kernel,
                           B=float(cv2.Laplacian(gray, cv2.CV_64F).var()), S_pct=float(((gray <= 5) | (gray >= 250)).mean() * 100), H_bit=float(-(p * np.log2(p)).sum()),
                           health_f54=float(health[indices.index(54)]), health_mean8=float(health.mean()), gshi_gt_reference=float(meta["gshi_gt"]), author_health_mean8=float(meta["gshi_pred"]), forward_seconds=elapsed)
                row["abs_error_vs_author"] = abs(row["health_mean8"] - row["author_health_mean8"])
                baseline = result[0] if result else row
                row.update(B_delta_vs_clean=row["B"]-baseline["B"], B_percent_change_vs_clean=100*(row["B"]/baseline["B"]-1), health_f54_delta_vs_clean=row["health_f54"]-baseline["health_f54"], health_mean8_delta_vs_clean=row["health_mean8"]-baseline["health_mean8"])
                result.append(row)
                images.append(rgb)
                if not cv2.imwrite(str(args.output / f"{sid}_f54.png"), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)):
                    raise RuntimeError(f"Could not save image for {sid}")
                say(f"[{i+1}/4] {sid}: B={row['B']:.2f}, health54={row['health_f54']:.6f}, mean8={row['health_mean8']:.6f}, source_error={row['abs_error_vs_author']:.8f}, forward={elapsed:.2f}s")
            write_csv(args.output / "benchmark_summary.csv", result)
            write_csv(args.output / "per_frame.csv", per_frame)
            monotonicity = []
            for key in ["B", "health_f54", "health_mean8"]:
                v = [r[key] for r in result]
                monotonicity.append(dict(metric=key, sampled_degraded_levels="s1,s2,s5", degraded_non_increasing=all(a>=b for a,b in zip(v[1:-1],v[2:])), including_clean_non_increasing=all(a>=b for a,b in zip(v[:-1],v[1:])), clean_to_s1_delta=v[1]-v[0]))
            write_csv(args.output / "monotonicity.csv", monotonicity)
            fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
            labels = ["Clean", "Blur 11 px (s1)", "Blur 13 px (s2)", "Blur 33 px (s5)"]
            for ax, key, title, unit in zip(axes.flat, ["health_f54", "B", "S_pct", "H_bit"], ["Health: frame 54 vs clip mean", "Blur proxy", "Extreme-intensity pixels", "Grayscale entropy"], ["Health (0-1)", "Laplacian response variance", "Pixel ratio (%)", "Entropy (bit)"]):
                ax.plot(range(4), [r[key] for r in result], "o-", label="Frame 54")
                if key == "health_f54":
                    ax.plot(range(4), [r["health_mean8"] for r in result], "s--", label="Mean of 8 frames")
                    ax.set_ylim(0,1)
                    ax.legend(fontsize=8)
                ax.set_title(title)
                ax.set_ylabel(unit)
                ax.set_xticks(range(4), labels, rotation=12, fontsize=8)
                ax.grid(alpha=.25)
            fig.suptitle("Small feasibility demo: S01, clean + 3 motion-blur levels")
            fig.savefig(args.output / "metric_curves.png", dpi=150)
            plt.close(fig)
            fig, axes = plt.subplots(2,2,figsize=(12,8), constrained_layout=True)
            for ax, rgb, row, label in zip(axes.flat, images, result, labels):
                ax.imshow(rgb)
                ax.set_title(f"{label} | B={row['B']:.1f} | health54={row['health_f54']:.4f}", fontsize=10)
                ax.axis("off")
            fig.suptitle("Same scene and frame 54; released corruption variants")
            fig.savefig(args.output / "image_grid.png", dpi=150)
            plt.close(fig)
            error = max(r["abs_error_vs_author"] for r in result)
            manifest.update(sample_count=len(result), health_row_count=len(per_frame), frame_indices=indices, forward_total_seconds=sum(r["forward_seconds"] for r in result), max_abs_error_vs_author=error, error_threshold_exclusive=base["analysis"]["author_reproduction_max_abs_error_exclusive"], monotonicity=monotonicity)
            if error >= manifest["error_threshold_exclusive"]:
                raise RuntimeError("Source reproduction error exceeds fixed tolerance")
            manifest["status"] = "pass"
            say(f"PASS: 4 clips / 32 health rows, max reproduction error={error:.8f}")
        except Exception as exc:
            manifest.update(status="failed", error=str(exc))
            say(traceback.format_exc())
        finally:
            manifest.update(finished_at=datetime.now(timezone(timedelta(hours=7))).isoformat(), wall_seconds=time.perf_counter()-wall_start)
            (args.output / "run_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0 if manifest["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
