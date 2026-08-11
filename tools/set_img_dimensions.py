from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image

HTML='index.html'
doc=Path(HTML).read_text(encoding='utf-8')
soup=BeautifulSoup(doc,'html.parser')

def resolve_src(src):
    if src.startswith('http'):
        return None
    p = Path(src)
    if p.exists():
        return p
    # try assets/img variants
    # remove query
    src_clean = src.split('?')[0]
    candidates = [Path(src_clean)]
    candidates += list(Path('assets/img').glob(Path(src_clean).stem + '*'))
    for c in candidates:
        if c.exists():
            return c
    return None

changed = 0
for img in soup.find_all('img'):
    src = img.get('src')
    if not src:
        continue
    p = resolve_src(src)
    if p:
        try:
            with Image.open(p) as im:
                w,h = im.size
            img['width']=str(w)
            img['height']=str(h)
            changed += 1
        except Exception as e:
            pass

if changed:
    Path(HTML).write_text(str(soup), encoding='utf-8')
    print('Updated', changed, 'img tags with dimensions')
else:
    print('No images updated')
