from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / 'index.html'
text = index_path.read_text(encoding='utf-8')

script = '<script src="assets/client-item-icons.js"></script>'
if script not in text:
    marker = '<script src="assets/client-sync.js"></script>'
    if marker in text:
        text = text.replace(marker, marker + '\n' + script, 1)
    elif '</body>' in text:
        text = text.replace('</body>', script + '\n</body>', 1)
    else:
        raise SystemExit('Could not locate insertion point for item icon renderer')

index_path.write_text(text, encoding='utf-8')
print('Lazy item micro-icon renderer enabled.')
