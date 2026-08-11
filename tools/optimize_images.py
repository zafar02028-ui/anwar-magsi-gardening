from PIL import Image
from pathlib import Path
import sys

SRC=Path('.')
OUT=Path('assets/img')
OUT.mkdir(parents=True,exist_ok=True)

sizes = [400, 800, 1000, 1200, 1600]

# target quality for larger "web" images
WEB_QUALITY = 80
LOW_QUALITY = 70

def process(p:Path):
    try:
        img=Image.open(p)
    except Exception as e:
        print('skip',p,e)
        return
    name=p.stem
    for w in sizes:
        if w > img.width:
            # don't upscale
            continue
        h = int(img.height * (w / img.width))
        im2 = img.resize((w, h), Image.LANCZOS)
        q = WEB_QUALITY if w >= 1200 else LOW_QUALITY
        out_webp = OUT / f"{name}-{w}.webp"
        im2.save(out_webp, 'webp', quality=q, method=6)
        print('wrote',out_webp)

if __name__=='__main__':
    exts = ['.jpg','.jpeg','.png','.webp']
    files = [p for p in SRC.iterdir() if p.suffix.lower() in exts]
    if not files:
        print('No image files found in project root')
        sys.exit(0)
    for p in files:
        process(p)
