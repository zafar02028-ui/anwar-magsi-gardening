from pathlib import Path
txt = Path('assets/css/style.css').read_text(encoding='utf-8')
out = txt
# remove comments
import re
out = re.sub(r'/\*.*?\*/', '', out, flags=re.S)
# remove extra whitespace
out = re.sub(r'\s+', ' ', out)
out = out.replace(' {', '{').replace('; ', ';').replace(': ', ':').replace(', ', ',')
Path('assets/css/style.min.css').write_text(out.strip(), encoding='utf-8')
print('Wrote assets/css/style.min.css')
