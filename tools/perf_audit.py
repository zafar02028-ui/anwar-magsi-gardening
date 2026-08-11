import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import sys

BASE='http://127.0.0.1:8000/'

def fetch(url):
    t0=time.time()
    r=requests.get(url, timeout=10)
    t=time.time()-t0
    return r, t

def head_size(url):
    try:
        h=requests.head(url, timeout=6, allow_redirects=True)
        if 'Content-Length' in h.headers:
            return int(h.headers['Content-Length'])
    except:
        pass
    try:
        r=requests.get(url, timeout=10)
        return len(r.content)
    except:
        return 0

def main():
    print('Fetching', BASE)
    r, t = fetch(BASE)
    print('Status', r.status_code, 'Time', f'{t:.2f}s')
    soup = BeautifulSoup(r.text, 'html.parser')
    assets = set()
    # CSS
    for l in soup.find_all('link', rel='stylesheet'):
        href=l.get('href')
        if href:
            assets.add(urljoin(BASE, href))
    # scripts
    for s in soup.find_all('script'):
        src=s.get('src')
        if src:
            assets.add(urljoin(BASE, src))
    # images
    images = []
    for img in soup.find_all('img'):
        src=img.get('src')
        if src:
            u=urljoin(BASE, src)
            assets.add(u)
            images.append({'tag':img, 'url':u})
    # picture sources (srcset)
    for src in soup.find_all('source'):
        ss=src.get('srcset')
        if ss:
            parts=[p.strip().split(' ')[0] for p in ss.split(',')]
            for p in parts:
                assets.add(urljoin(BASE, p))
    # background-images in style attributes
    for el in soup.find_all(style=True):
        st=el['style']
        if 'background-image' in st:
            # crude extract
            import re
            m=re.search(r'url\(["\']?(.*?)["\']?\)', st)
            if m:
                assets.add(urljoin(BASE, m.group(1)))

    total_bytes=0
    results=[]
    print('\nFound', len(assets), 'assets')
    for a in sorted(assets):
        sz = head_size(a)
        results.append((a,sz))
        total_bytes += sz
    results.sort(key=lambda x: x[1], reverse=True)
    print('\nTop assets by size:')
    for u,sz in results[:10]:
        print(f"{sz:9d} bytes  {u}")

    print(f"\nTotal asset bytes: {total_bytes/1024:.1f} KB across {len(results)} assets")
    print(f"Images on page: {len(images)}")
    webp_count=0
    without_srcset=0
    for im in images:
        url=im['url']
        if url.lower().endswith('.webp'):
            webp_count+=1
        # check if img has srcset or picture parent
        tag=im['tag']
        if not tag.get('srcset') and not tag.find_parent('picture'):
            without_srcset+=1
    print(f"WebP images: {webp_count}")
    print(f"Images without srcset/picture: {without_srcset}")

    # basic SEO checks
    print('\nSEO checks:')
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta_desc = soup.find('meta', attrs={'name':'description'})
    og = soup.find('meta', property='og:image')
    print('Title:', title)
    print('Meta description:', 'present' if meta_desc else 'missing')
    print('OG image:', 'present' if og else 'missing')

if __name__=='__main__':
    main()
