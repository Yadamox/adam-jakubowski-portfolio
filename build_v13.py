"""Reproducible production v13: legacy content -> approved experience layer.

Everything needed lives in this repository. No preview/iCloud dependency.
"""
from pathlib import Path
import json,runpy,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_v10.py'),run_name='__main__')
# Case-study content is static; restore its clean input before each transformation.
for name,text in json.loads((ROOT/'case-studies-source.json').read_text()).items():
 (ROOT/name).write_text(text)
with tempfile.TemporaryDirectory(prefix='production-v13-') as temp:
 base=Path(temp)
 files=[p for p in ROOT.rglob('*.html') if 'node_modules' not in p.parts and '.wrangler' not in p.parts]
 assert len(files)==65,len(files)
 for p in files:
  s=p.read_text().replace('/site-v10.css?v=11','/site-v12.css?v=12').replace('/site-v10.js?v=11','/site-v12.js?v=12')
  s=s.replace('<link rel="stylesheet" href="/case-study.css?v=2">','').replace('content="#0f100f"','content="#f7f5f0"')
  s=s.replace('<h1>Spokojniejsza realizacja. Jasne decyzje. Udokumentowany odbiór.</h1>','<h1><span>Spokojniejsza realizacja.</span> <span class="headline-accent">Jasne decyzje.</span> <span>Udokumentowany odbiór.</span></h1>')
  target=base/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
 subprocess.run([sys.executable,str(ROOT/'transform_v13.py'),str(base)],check=True)
 # Public pages are indexable; thank-you remains intentionally noindex.
 for p in files:
  if p.name not in ('dziekuje.html','thank-you.html','danke.html'):
   assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex',p.read_text()),str(p)
print('PASS: production v13 rebuilt without preview-only noindex')
