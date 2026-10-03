from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re, sys
ROOT=Path(__file__).resolve().parent
errors=[]
class P(HTMLParser):
    def __init__(self,path): super().__init__(); self.path=path
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ('href','src'):
            v=a.get(key,'')
            if not v or v.startswith(('#','mailto:','tel:','http://','https://','data:')): continue
            clean=v.split('#')[0].split('?')[0]
            target=(ROOT/clean.lstrip('/')) if clean.startswith('/') else (self.path.parent/clean)
            if clean.endswith('/'): target=target/'index.html'
            if not target.exists(): errors.append(f'{self.path.relative_to(ROOT)}: missing {v}')
        if tag=='form':
            action=a.get('action') or ''
            if not action.startswith('https://formsubmit.co/'): errors.append(f'{self.path.relative_to(ROOT)}: invalid form action {action}')
for path in ROOT.rglob('*.html'):
    try: P(path).feed(path.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{path}: parse {e}')
# Required public paths.
required=['pl/dla-klienta-prywatnego.html','pl/dla-firm.html','pl/formularz-b2c.html','pl/formularz-b2b.html','pl/polityka-prywatnosci.html','en/private-clients.html','en/for-companies.html','de/privatkunden.html','de/fuer-unternehmen.html','robots.txt','sitemap.xml']
for r in required:
    if not (ROOT/r).exists(): errors.append(f'missing required {r}')
# No fake mailto form and no prohibited broad promises in v9 pages.
for path in [ROOT/'pl/index.html',ROOT/'pl/dla-klienta-prywatnego.html',ROOT/'pl/dla-firm.html']:
    text=path.read_text(encoding='utf-8').lower()
    if '<form' in text and 'mailto:' in text: errors.append(f'{path.name}: mailto form')
    for phrase in ['odpowiadam za cały proces','jedna odpowiedzialność']:
        if phrase in text: errors.append(f'{path.name}: broad promise {phrase}')
    for phrase in ['gwarantuję termin','gwarantuję jakość']:
        if re.search(rf'(?<!nie ){re.escape(phrase)}', text): errors.append(f'{path.name}: broad promise {phrase}')
# Explicit B2C/B2B entry points.
home=(ROOT/'pl/index.html').read_text(encoding='utf-8')
for marker in ['choose_b2c','choose_b2b','dla-klienta-prywatnego.html','dla-firm.html']:
    if marker not in home: errors.append(f'home missing {marker}')
for form in ['pl/formularz-b2c.html','pl/formularz-b2b.html']:
    text=(ROOT/form).read_text(encoding='utf-8')
    for marker in ['privacy_ack','utm_source','_next','form-status']:
        if marker not in text: errors.append(f'{form} missing {marker}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(list(ROOT.rglob("*.html")))} HTML files; internal assets, routes, forms and promises checked')
