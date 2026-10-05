"""Prepare frozen source and checkpoint without downloading clips or running inference."""
from pathlib import Path
import hashlib
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    model = json.loads((ROOT / 'configs/benchmark.json').read_text(encoding='utf-8'))['model']
    source = ROOT / '.lab_cache/drive-c-source'
    checkpoint = ROOT / 'drive-c-dataset/checkpoints/epoch_021_best.pth'
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--depth', '1', '--branch', model['expected_tag'],
                        '--filter=blob:none', '--sparse', model['source_url'], str(source)], check=True)
    if not (source / '.git').exists():
        raise RuntimeError('Existing source is not a separate Git clone; inspect it manually.')
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != model['expected_commit_from_saved_notebook']:
        raise RuntimeError('Source commit differs from the frozen benchmark; no checkout was changed.')
    dirty = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain',
                                     '--untracked-files=no'], text=True).strip()
    if dirty:
        raise RuntimeError('Source has tracked changes; inspect them manually.')
    subprocess.run(['git', '-C', str(source), 'sparse-checkout', 'set',
                    'src', 'scripts', 'simulation', 'configs', 'dataset', 'docs'], check=True)
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        url = f'https://raw.githubusercontent.com/shiv-aher/drive-c-dataset/{commit}/checkpoints/epoch_021_best.pth'
        temporary = checkpoint.with_suffix('.download')
        print('Downloading frozen checkpoint (about 94 MB)...', flush=True)
        try:
            with urllib.request.urlopen(url, timeout=60) as response, temporary.open('wb') as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            if digest(temporary) != model['checkpoint_sha256']:
                raise RuntimeError('Downloaded checkpoint failed SHA-256 verification.')
            temporary.replace(checkpoint)
        finally:
            temporary.unlink(missing_ok=True)
    if digest(checkpoint) != model['checkpoint_sha256']:
        raise RuntimeError('Existing checkpoint failed SHA-256 verification; it was not replaced.')
    print(f'PASS: frozen source {commit}; checkpoint SHA-256 verified. No clips downloaded.')


if __name__ == '__main__':
    main()
