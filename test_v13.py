"""Production gates specific to the approved v13 experience."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib
ROOT=Path(__file__).resolve().parent
class D(HTMLParser):
 def __init__(self):super().__init__();self.duplicates=[]
 def handle_starttag(self,tag,attrs):
  names=[a[0] for a in attrs]
  if len(names)!=len(set(names)):self.duplicates.append((tag,names))
manifest=json.loads((ROOT/'approved-v13-sha256.json').read_text())
for name,expected in manifest.items():
 p=ROOT/name;data=p.read_bytes()
 if name.endswith('.html'):
  s=data.decode();doc=D();doc.feed(s);assert not doc.duplicates,(name,doc.duplicates)
  if p.name not in ('dziekuje.html','thank-you.html','danke.html'):assert 'noindex' not in s,name
  if '<main' in s:
   assert '/site-v13.css?v=13' in s and '/site-v13.js?v=13' in s,name
   assert 'site-v10.' not in s and '/case-study.css' not in s,name
   assert s.count('aria-current="page"')<=1,name
  # Only the unpublished package's noindex directive differs.
  data=s.replace('<meta name="robots" content="noindex,nofollow">','').encode()
 assert hashlib.sha256(data).hexdigest()==expected,('approved version mismatch',name)
for lang,process,private,business in [('pl','proces','dla-klienta-prywatnego','dla-firm'),('en','process','private-clients','for-companies'),('de','arbeitsweise','privatkunden','fuer-unternehmen')]:
 assert 'control-timeline' in (ROOT/lang/(process+'.html')).read_text()
 assert 'situation-picker' in (ROOT/lang/(private+'.html')).read_text()
 assert 'delivery-chain' in (ROOT/lang/(business+'.html')).read_text()
print(f'PASS v13 production: {len(manifest)} approved files, no preview noindex, no duplicate attributes, localized experience')
