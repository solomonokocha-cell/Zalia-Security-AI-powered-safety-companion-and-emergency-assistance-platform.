from pathlib import Path

path = Path('ZaziAi.html')
text = path.read_text(encoding='utf-8')
lines = text.splitlines(True)
cleaned = ''.join(line for line in lines if not line.lstrip().startswith('/* ========================================================='))
path.write_text(cleaned, encoding='utf-8')
print('removed divider comments from', path)
