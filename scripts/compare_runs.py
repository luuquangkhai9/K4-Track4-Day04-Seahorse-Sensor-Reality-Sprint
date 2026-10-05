"""Compare a repeated four-clip run with the saved evidence; no inference."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['B', 'S_pct', 'H_bit', 'health_f54', 'health_mean8']


def table(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, default=ROOT / 'outputs/stage3_small')
    parser.add_argument('--repeat', type=Path, default=ROOT / 'outputs/stage3_repeat')
    parser.add_argument('--health-tolerance', type=float, default=1e-6)
    args = parser.parse_args()
    ref, rep = table(args.reference / 'benchmark_summary.csv'), table(args.repeat / 'benchmark_summary.csv')
    assert [r['sample_id'] for r in ref] == [r['sample_id'] for r in rep], 'Sample lists differ'
    rows = []
    for a, b in zip(ref, rep):
        image = a['sample_id'] + '_f54.png'
        row = {'sample_id': a['sample_id'],
               'f54_png_identical': sha(args.reference / image) == sha(args.repeat / image)}
        row.update({f'abs_diff_{k}': abs(float(a[k]) - float(b[k])) for k in METRICS})
        rows.append(row)
    ref_frames, rep_frames = table(args.reference / 'per_frame.csv'), table(args.repeat / 'per_frame.csv')
    assert [(r['sample_id'], r['frame_idx']) for r in ref_frames] == \
           [(r['sample_id'], r['frame_idx']) for r in rep_frames], 'Frame lists differ'
    frame_diff = max(abs(float(a['gshi_pred']) - float(b['gshi_pred'])) for a, b in zip(ref_frames, rep_frames))
    with (args.repeat / 'comparison_vs_reference.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifests = [json.loads((d / 'run_manifest.json').read_text(encoding='utf-8')) for d in (args.reference, args.repeat)]
    summary = {
        'reference': args.reference.relative_to(ROOT).as_posix(), 'repeat': args.repeat.relative_to(ROOT).as_posix(),
        'same_runner_config_source_checkpoint': all(manifests[0][k] == manifests[1][k] for k in
                                                    ['runner_sha256', 'config_sha256', 'source_commit', 'checkpoint_sha256']),
        'same_video_sha256': manifests[0]['videos'] == manifests[1]['videos'],
        'image_metrics_identical': all(r[f'abs_diff_{k}'] == 0 for r in rows for k in ['B', 'S_pct', 'H_bit']),
        'f54_png_identical': all(r['f54_png_identical'] for r in rows),
        'max_abs_diff_health_per_frame': frame_diff, 'health_tolerance': args.health_tolerance,
        'reference_python_versions': [manifests[0]['python'], manifests[0]['versions']],
        'repeat_python_versions': [manifests[1]['python'], manifests[1]['versions']],
    }
    summary['status'] = 'pass' if (summary['same_runner_config_source_checkpoint'] and summary['same_video_sha256']
                                   and summary['image_metrics_identical'] and frame_diff < args.health_tolerance) else 'failed'
    (args.repeat / 'comparison_vs_reference.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{summary['status'].upper()}: image metrics identical={summary['image_metrics_identical']}, "
          f"max health diff={frame_diff:.3e} (tolerance {args.health_tolerance:g})")
    return 0 if summary['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
