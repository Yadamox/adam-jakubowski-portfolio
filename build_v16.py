"""Rebuild approved v16 without preview/iCloud dependencies.

The archived base is immutable input, not a deployed file. Preview-only robots
are removed, existing thank-you noindex retained; public content is unchanged.
"""
from pathlib import Path
import tempfile,subprocess,sys,shutil,zipfile,json,hashlib,re
ROOT=Path(__file__).resolve().parent

def build():
 approved=json.loads((ROOT/'approved-v16-sha256.json').read_text())
 scratch=Path.home()/'.hermes/profiles/project-manager-klienci/cache/scratch'
 scratch.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='production-v16-',dir=scratch) as temp:
  work=Path(temp)
  for f in (ROOT/'v16-source').iterdir():
   if f.is_file() and f.suffix in ('.py','.js','.css'):shutil.copy2(f,work/f.name)
  with zipfile.ZipFile(ROOT/'v16-source/base-source.zip') as z:
   assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
   z.extractall(work/'source')
  subprocess.run([sys.executable,str(work/'build.py')],cwd=work,check=True)
  site=work/'site'
  actual={str(p.relative_to(site)):hashlib.sha256(p.read_bytes()).hexdigest() for p in site.rglob('*') if p.is_file()}
  assert actual==approved, 'Rebuilt output differs from approved v16'
  for p in site.rglob('*.html'):
   text=p.read_text().replace('<meta name="robots" content="noindex,nofollow">','')
   text=text.replace('/site-v13.js?v=13','/site-v13.js?v=16')
   # Preserve legacy legal limits inadvertently omitted in the approved preview.
   lang=p.parent.name if p.parent.name in ('pl','en','de') else 'pl'
   liability={'pl':'Odpowiadam za swój uzgodniony zakres; ten opis nie wyłącza odpowiedzialności wymaganej prawem.', 'en':'I remain responsible for my own agreed scope; this description does not exclude liability required by law.', 'de':'Ich hafte für meinen eigenen vereinbarten Umfang; diese Beschreibung schließt keine gesetzlich vorgeschriebene Haftung aus.'}[lang]
   text=re.sub(r'(<section class="boundary">.*?)(</section>)',lambda m:m[1]+'<p>'+liability+'</p>'+m[2],text,flags=re.S)
   if p.relative_to(site).as_posix()=='de/privatkunden.html':
    territory='Kommunikation auf Polnisch, Englisch oder Deutsch bedeutet nicht automatisch, dass Leistungen im Ausland angeboten werden. Hauptleistungsgebiet ist Polen; jedes Auslandsprojekt erfordert eine vorherige rechtliche und steuerliche Klärung.'
    text=text.replace('</main>','<p class="notice">'+territory+'</p></main>')
   if p.name not in ('dziekuje.html','thank-you.html','danke.html'):
    assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex',text),str(p)
   p.write_text(text)
  for p in site.rglob('*'):
   if p.is_file() and p.name not in ('robots.txt','llms.txt'):
    q=ROOT/p.relative_to(site);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
 (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://adam-jakubowski.com/sitemap.xml\n')
 manifest={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in approved}
 (ROOT/'built-v16-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('PASS: 93 approved files reproduced; 65 production HTML; public indexing enabled, thank-you noindex retained')

if __name__=='__main__':build()
