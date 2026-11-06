"""Production-only v16 checks; read-only and never import the generator."""
from pathlib import Path
import json,hashlib,re,subprocess,sys
R=Path(__file__).resolve().parent
manifest=json.loads((R/'built-v16-sha256.json').read_text())
assert len(manifest)==93,len(manifest)
for name,digest in manifest.items():
 assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
html=[R/n for n in manifest if n.endswith('.html')]
assert len(html)==65
for p in html:
 s=p.read_text()
 if p.name in ('dziekuje.html','thank-you.html','danke.html'):
  assert 'content="noindex,follow"' in s,str(p)
 else:assert not re.search(r'<meta[^>]*name="robots"[^>]*noindex',s),str(p)
 assert 'noindex,nofollow' not in s
 assert 'PRIVATE LOCAL PREVIEW' not in s
 if '<form ' in s:
  assert s.count('data-mailto-form')==1
  assert all(x in s for x in ('copy-message','data-email-draft','mailto:info@adam-jakubowski.com'))
for lang,slug in [('pl','dla-klienta-prywatnego'),('en','private-clients'),('de','privatkunden')]:
 s=(R/lang/(slug+'.html')).read_text()
 assert re.search(r'<p class="notice pricing-terms"><strong>.*?(dopiero|only after|erst nach).*?</strong>',s,re.S)
 for slug in ['index','formularz-b2c' if lang=='pl' else 'b2c-form' if lang=='en' else 'b2c-formular']:
  assert '/site-v13.js?v=16' in (R/lang/(slug+'.html')).read_text()
assert 'Disallow: /' not in (R/'robots.txt').read_text()
for f in ('site-v13.js','offer-v16.js','project-v16.js'):subprocess.run(['node','--check',str(R/f)],check=True)
print('PASS: v16 manifest (93 files), indexability, local contact, conditional cancellation terms and JavaScript syntax')
