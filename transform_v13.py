"""Build unpublished v13; preserve every word of the v12 offer and formal notices."""
from pathlib import Path
import shutil,re,json,html
from html.parser import HTMLParser
from collections import Counter
ROOT=Path(__file__).resolve().parent
import sys
BASE=Path(sys.argv[1])
OUT=ROOT
shutil.copytree(BASE,OUT,dirs_exist_ok=True)
L={
'pl':dict(close='Zamknij',more='Dodatkowe informacje (opcjonalnie)',start='Od czego chcesz zacząć?',situations=['Mam ofertę do sprawdzenia','Zbliża się odbiór','Chcę sprawdzić poprawki','Potrzebuję kontroli kilku etapów'],sample='Przykładowy rezultat',see='Zobacz przykład',proof='Doświadczenie zawodowe',chain=['Dokumentacja','Produkcja','Logistyka','Montaż','Odbiór']),
'en':dict(close='Close',more='Additional information (optional)',start='Where would you like to start?',situations=['I have a quotation to review','Handover is approaching','I need a snagging follow-up','I need checks across several stages'],sample='Sample deliverable',see='View sample',proof='Professional experience',chain=['Documentation','Production','Logistics','Installation','Handover']),
'de':dict(close='Schließen',more='Weitere Angaben (optional)',start='Wo möchten Sie beginnen?',situations=['Ich möchte ein Angebot prüfen lassen','Die Abnahme steht bevor','Ich möchte Nachbesserungen prüfen lassen','Ich brauche Kontrollen in mehreren Phasen'],sample='Beispiel eines Ergebnisses',see='Beispiel ansehen',proof='Berufliche Erfahrung',chain=['Dokumentation','Produktion','Logistik','Montage','Abnahme'])}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.words=[]
 def handle_starttag(self,t,a):
  if t in ('style','script'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('style','script'):self.skip-=1
 def handle_data(self,s):
  if not self.skip:self.words.extend(s.split())
def words(s):p=Text();p.feed(s);return Counter(p.words)
def plain(s):return html.unescape(re.sub('<[^>]*>','',s))
def preview(lang,slug):
 s=(BASE/lang/(slug+'.html')).read_text()
 body=re.search(r'<article[^>]*>(.*?)</article>',s,re.S)[1]
 pairs=re.findall(r'<h2>(.*?)</h2><p>(.*?)</p>',body,re.S)
 # Actual excerpt of the public sample, not client data or invented records.
 return '<div class="doc-preview" aria-hidden="true"><span class="doc-label">'+L[lang]['sample']+'</span>'+''.join('<div class="doc-row"><b>'+h+'</b><p>'+p+'</p></div>' for h,p in pairs[:2])+'</div>'
checks=[]
for p in sorted(BASE.rglob('*.html')):
 rel=p.relative_to(BASE);s=p.read_text();original=s
 lang=rel.parts[0] if rel.parts[0] in L else 'pl';v=L[lang]
 if '<main' not in s:
  (OUT/rel).write_text(s);checks.append({'path':str(rel),'all_original_words_preserved':True});continue
 route='/'+str(rel).replace('index.html','').removesuffix('.html')
 nav=re.search(r'<nav id="nav">(.*?)</nav>',s,re.S)
 links=re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',nav[1],re.S)
 primary=[u for u,t in links if not re.fullmatch('[A-Z]{2}',plain(t))]
 family='general'
 for i,name in enumerate(['private','business','process','evidence','about','contact']):
  if i<len(primary) and route==primary[i]:family=name
 if 'sample-' in route or 'pre-order-checklist' in route or 'landbyska-verket' in route:family='evidence'
 if re.search('formularz-b2c|private-enquiry|privat.*anfrage',route):family='private'
 if re.search('formularz-b2b|business-enquiry|unternehmen.*anfrage',route):family='business'
 if 'data-segment="B2C"' in s:family='private'
 if 'data-segment="B2B"' in s:family='business'
 s=s.replace('<body','<body data-family="'+family+'"',1)
 active=route
 if 'data-mailto-form' in s:active=primary[0 if family=='private' else 1]
 if family=='evidence' and len(primary)>3:active=primary[3]
 def navactive(m):
  tag=m[0];u=re.search('href="([^"]+)"',tag)[1]
  if u==active and ' hreflang=' not in tag:tag=tag.replace('<a ','<a aria-current="page" ')
  if re.search(r'lang="'+lang+'"',tag):tag=tag.replace('<a ','<a aria-current="true" ')
  return tag
 newnav=re.sub(r'<a\b[^>]*>',navactive,nav[0]);s=s.replace(nav[0],newnav)
 s=s.replace('class="menu"','class="menu" data-close="'+v['close']+'"',1)
 s=s.replace('</head>','<meta name="view-transition" content="same-origin"><noscript><link rel="stylesheet" href="/nojs-v13.css?v=13"></noscript></head>')
 if family=='process':s=s.replace('class="steps detailed"','class="steps detailed control-timeline"')
 # Situation shortcuts lead to existing cards, without removing any scope or price.
 if family in ('private','business') and 'class="cards"' in s:
  idx=[0]
  def cardid(m):idx[0]+=1;return '<article class="card" id="service-'+str(idx[0])+'">'
  s=re.sub(r'<article class="card">',cardid,s)
  if family=='private':
   component='<nav class="situation-picker" aria-label="'+v['start']+'"><p class="eyebrow">'+v['start']+'</p><div>'+''.join('<a href="#service-'+str(i+1)+'"><small>0'+str(i+1)+'</small>'+label+'<span aria-hidden="true">↗</span></a>' for i,label in enumerate(v['situations']))+'</div></nav>'
  else:component='<div class="delivery-chain" aria-label="'+v['start']+'">'+''.join('<span><small>0'+str(i+1)+'</small>'+label+'</span>' for i,label in enumerate(v['chain']))+'</div>'
  s=s.replace('</header><section class="light">','</header>'+component+'<section class="light">',1)
  target='sample-handover-report' if family=='private' else 'sample-risk-register'
  component='<section class="result-bridge"><div><p class="eyebrow">'+v['sample']+'</p><h2>'+re.search(r'<h1>(.*?)</h1>',(BASE/lang/(target+'.html')).read_text(),re.S)[1]+'</h2><a class="text-link" href="/'+lang+'/'+target+'">'+v['see']+' →</a></div>'+preview(lang,target)+'</section>'
  s=s.replace('<section class="boundary">',component+'<section class="boundary">',1)
 # Replace empty material cards with excerpts of their actual sample pages.
 if family=='evidence' and 'class="cards"' in s:
  def doccard(m):
   c=m[0];u=re.search(r'href="([^"]+)"',c)[1];title=plain(re.search(r'<h3>(.*?)</h3>',c)[1]);slug=u.rsplit('/',1)[-1]
   if (BASE/lang/(slug+'.html')).exists():
    c=c.replace('<h3>',preview(lang,slug)+'<h3>',1).replace('class="text-link"','class="text-link" aria-label="'+html.escape(title,quote=True)+'"')
   return c
  s=re.sub(r'<article class="card">.*?</article>',doccard,s,flags=re.S)
 # Collapse only optional fields. Required and confidentiality fields stay visible.
 if 'data-mailto-form' in s:
  optional=[]
  def field(m):
   if 'class="optional"' in m[0]:optional.append(m[0]);return ''
   return m[0]
  s=re.sub(r'<label>.*?</label>',field,s,flags=re.S)
  if optional:s=s.replace('<p class="fine">','<details class="optional-fields"><summary>'+v['more']+'</summary><div>'+''.join(optional)+'</div></details><p class="fine">',1)
 # Keep every original word; additions are layout aids or excerpts, never revised promises.
 missing=words(original)-words(s)
 assert not missing,(str(rel),dict(missing))
 s=s.replace('/site-v12.css?v=12','/site-v13.css?v=13').replace('/site-v12.js?v=12','/site-v13.js?v=13')
 (OUT/rel).write_text(s);checks.append({'path':str(rel),'all_original_words_preserved':True,'family':family})


for n in ['site-v12.css','site-v12.js']:(OUT/n).unlink(missing_ok=True)
(ROOT/'build-content-checks.json').write_text(json.dumps(checks,indent=2))
assert len(checks)==65,len(checks)
print('PASS v13: 65 HTML; every original word preserved; PL/EN/DE; production source built')
