"""Audit saved evidence without rerunning inference; personal details are a separate gate."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def close(actual, expected, tolerance=1e-7):
    if not math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=tolerance):
        raise ValueError(f'Values differ: {actual} vs {expected}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-personal-details', action='store_true')
    args = parser.parse_args()
    out = ROOT / 'outputs/stage3_small'
    config = json.loads((ROOT / 'configs/benchmark_small.json').read_text(encoding='utf-8'))
    base = json.loads((ROOT / 'configs/benchmark.json').read_text(encoding='utf-8'))
    manifest = json.loads((out / 'run_manifest.json').read_text(encoding='utf-8'))
    assert manifest['status'] == 'pass'
    assert manifest['scope'] == config
    assert manifest['source_commit'] == base['model']['expected_commit_from_saved_notebook']
    assert manifest['checkpoint_sha256'] == base['model']['checkpoint_sha256']
    assert manifest['runner_sha256'] == sha(ROOT / 'scripts/stage3_small_demo.py')
    assert manifest['config_sha256'] == {'base': sha(ROOT / 'configs/benchmark.json'),
                                         'small': sha(ROOT / 'configs/benchmark_small.json')}
    summary, frames = table(out / 'benchmark_summary.csv'), table(out / 'per_frame.csv')
    assert [r['sample_id'] for r in summary] == config['sample_ids']
    assert len(summary) == manifest['sample_count'] == 4
    assert len(frames) == manifest['health_row_count'] == 32
    assert len({(r['sample_id'], r['frame_idx']) for r in frames}) == 32
    clean = summary[0]
    import cv2
    import numpy as np
    for row in summary:
        selected = [r for r in frames if r['sample_id'] == row['sample_id']]
        assert [int(r['frame_idx']) for r in selected] == manifest['frame_indices']
        close(row['health_mean8'], math.fsum(float(r['gshi_pred']) for r in selected) / 8)
        close(row['health_f54'], next(r['gshi_pred'] for r in selected if r['frame_idx'] == '54'))
        close(row['abs_error_vs_author'], abs(float(row['health_mean8']) - float(row['author_health_mean8'])))
        for metric in ['B', 'health_f54', 'health_mean8']:
            close(row[metric + '_delta_vs_clean'], float(row[metric]) - float(clean[metric]))
        close(row['B_percent_change_vs_clean'], 100 * (float(row['B']) / float(clean['B']) - 1))
        image = cv2.imread(str(out / (row['sample_id'] + '_f54.png')))
        assert image is not None and image.shape == (720, 1280, 3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        close(row['B'], cv2.Laplacian(gray, cv2.CV_64F, ksize=1).var())
        close(row['S_pct'], 100 * np.mean((gray <= 5) | (gray >= 250)))
        hist = np.bincount(gray.ravel(), minlength=256) / gray.size
        hist = hist[hist > 0]
        close(row['H_bit'], -np.sum(hist * np.log2(hist)))
    close(manifest['forward_total_seconds'], sum(float(r['forward_seconds']) for r in summary))
    error = max(float(r['abs_error_vs_author']) for r in summary)
    close(manifest['max_abs_error_vs_author'], error)
    assert error < base['analysis']['author_reproduction_max_abs_error_exclusive']
    for row in table(out / 'monotonicity.csv'):
        values = [float(r[row['metric']]) for r in summary]
        assert row['degraded_non_increasing'] == str(all(a >= b for a, b in zip(values[1:], values[2:])))
        assert row['including_clean_non_increasing'] == str(all(a >= b for a, b in zip(values, values[1:])))
    for filename in ['image_grid.png', 'metric_curves.png']:
        assert cv2.imread(str(out / filename)) is not None
    reports = [ROOT / 'reports' / name for name in (
        '2A202602599_LuuQuangKhai.md', 'LeHung.md',
        '2A202602927_DangDinhDoan.md', '2A202602788_NguyenHoNam.md')]
    assert len(reports) == 4
    pending = []
    for report in reports:
        content = report.read_text(encoding='utf-8')
        for heading in ['## 1. Problem', '## 2. Method', '## 3. Benchmark',
                        '## 4. Failure case', '## 5. Engineering decision']:
            assert heading in content, (report.name, heading)
        for row in summary:
            for key, precision in [('B', 4), ('S_pct', 4), ('H_bit', 4),
                                   ('health_f54', 6), ('health_mean8', 6)]:
                assert f'{float(row[key]):.{precision}f}' in content, (report.name, key)
        if '\u0043h\u1edd b\u1ed5 sung' in content:
            pending.append(report.name + ': student ID missing')
        if '[Th\u00e0nh vi\u00ean b\u1ed5 sung' in content:
            pending.append(report.name + ': actual contribution needs confirmation')
    documents = (list(ROOT.glob('*.md')) + list((ROOT / 'reports').rglob('*.md'))
                 + list((ROOT / 'docs').rglob('*.md'))
                 + list((ROOT / 'drive-c-dataset').rglob('*.md')))
    # A fresh clone leaves the submodule empty; setup_demo.py keeps the same commit in the cache.
    submodule, frozen = ROOT / 'drive-c-dataset', ROOT / '.lab_cache/drive-c-source'
    for doc in documents:
        content = doc.read_text(encoding='utf-8')
        for target in re.findall(r'\]\((<[^>]+>|[^)]+)\)', content):
            target = target.strip('<>')
            if target.startswith(('https://', 'http://', '#')):
                continue
            path = (doc.parent / target.split('#', 1)[0]).resolve()
            if path.is_relative_to(submodule) and not (submodule / '.git').exists():
                assert (frozen / '.git').exists(), 'Run scripts/setup_demo.py to check source links'
                path = frozen / path.relative_to(submodule)
            assert path.exists(), (doc.name, target)
    assert 'url = https://github.com/shiv-aher/drive-c-dataset.git' in (ROOT / '.gitmodules').read_text()
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'technical_evidence': 'pass',
              'scope': 'saved four-clip artifacts, image-derived metrics, CSV aggregation, provenance, reports and local links',
              'documents_checked': len(documents), 'health_rows': 32,
              'personal_details_complete': not pending, 'pending': pending,
              'limitations': 'Does not prove rehearsal, remote upload, access permissions or VLearn submission.'}
    dest = ROOT / 'outputs/submission_check'
    dest.mkdir(exist_ok=True)
    (dest / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PASS: saved evidence, recomputed image metrics, report tables and local links.')
    for item in pending:
        print('PENDING: ' + item)
    if args.require_personal_details and pending:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
