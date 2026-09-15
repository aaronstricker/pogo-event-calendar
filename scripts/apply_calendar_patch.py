#!/usr/bin/env python3
import base64, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / '.calendar-patches'
ALLOWED = {
    'index.html',
    'README.md',
    'discord_digest.py',
    'discord-digest.yml',
    'scripts/discord_digest.py',
    '.github/workflows/discord-digest.yml',
}

def safe_path(rel):
    if rel not in ALLOWED:
        raise ValueError(f'Path not allowed: {rel}')
    path = (ROOT / rel).resolve()
    if ROOT not in path.parents and path != ROOT:
        raise ValueError(f'Unsafe path: {rel}')
    return path

def apply_request(req_path):
    data = json.loads(req_path.read_text())
    for op in data.get('operations', []):
        rel = op['path']
        action = op['action']
        path = safe_path(rel)
        if action == 'replace':
            raw = base64.b64decode(op['content_b64'])
            text = raw.decode('utf-8')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        elif action == 'delete':
            if path.exists():
                path.unlink()
        else:
            raise ValueError(f'Unsupported action: {action}')
    req_path.unlink()


def main():
    if not PATCH_DIR.exists():
        return 0
    requests = sorted(PATCH_DIR.glob('*.json'))
    if not requests:
        print('No patch requests found.')
        return 0
    for req in requests:
        print(f'Applying {req.name}')
        apply_request(req)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
