"""Keep every secondary route consistent with the current offer; preserve case facts."""
import re,json
from html import escape as e

def update(s,l,d,slug):
 if 'http-equiv="refresh"' in s.lower():return s
 # Navigation labels are targeted by their existing local destination.
 paths=[d['paths'][1],d['paths'][2],d['paths'][3],d['evpath'],{'pl':'o-mnie','en':'about','de':'ueber-mich'}[l],d['paths'][4]]
 def navlabels(m):
  nav=m[0]
  for path,label in zip(paths,d['nav']):
   nav=re.sub(r'(<a\b[^>]*href="/'+l+'/'+re.escape(path)+r'"[^>]*>).*?(</a>)',lambda m:m[1]+e(label)+m[2],nav)
  return nav
 s=re.sub(r'<nav\b[^>]*>.*?</nav>',navlabels,s,flags=re.S)
 s=s.replace('aria-current="true"','data-active-language="true"')
 s=re.sub(r'(<footer>.*?<p>).*?(</p>)',lambda m:m[1]+e(d['footer'])+m[2],s,flags=re.S)
 for old in ['Opisz swoją sytuację','Describe your situation','Situation beschreiben']:
  s=s.replace(old,e(d['brief']))
 about={'pl':'o-mnie','en':'about','de':'ueber-mich'}[l]
 if slug==about:
  old={'pl':'Nie zastępuję projektanta, wykonawcy ani rzeczoznawcy. Wspieram przygotowanie i kontrolę realizacji w uzgodnionym zakresie.','en':'I do not replace the designer, contractor or expert witness. I support preparation and control of delivery within the agreed scope.','de':'Ich ersetze weder Planer noch Auftragnehmer oder Sachverständige. Ich unterstütze Vorbereitung und Kontrolle der Umsetzung im vereinbarten Umfang.'}[l]
  s=s.replace(old,d['boundary'])
  s=re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*',lambda m:m[1]+e(d['lead'],quote=True),s)
  # The former schema described an advice-only service model.
  s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
 if slug==d['evpath']:
  note='<p class="evidence-note">'+e(d['prooftext'])+'</p>'
  s=s.replace('</h1>','</h1>'+note,1)
  # The professional reference precedes clearly illustrative documents.
  feature=re.search(r'<section class="case-feature">.*?</section>',s,re.S)
  if feature:
   s=s[:feature.start()]+s[feature.end():]
   s=re.sub(r'(<header class="page-hero[^\"]*">.*?</header>)',lambda m:m[1]+feature.group(),s,count=1,flags=re.S)
 if slug=='landbyska-verket':
  s=s.replace('<main id="main">','<main id="main"><p class="notice case-scope">'+e(d['photo'])+'</p>',1)
 if slug in ['pre-order-checklist','sample-handover-report','sample-risk-register']:
  note={'pl':'Materiał poglądowy do przygotowania ustaleń, nie oferta wykonania ani wezwanie do wpłaty. Niezależny odbiór dotyczy tylko cudzej realizacji.','en':'Illustrative material to help prepare agreements, not an execution offer or a request for payment. Independent handover support is only for another contractor’s work.','de':'Beispielmaterial zur Vorbereitung von Abstimmungen, kein Ausführungsangebot und keine Zahlungsaufforderung. Unabhängige Übergabebegleitung betrifft nur Leistungen anderer Betriebe.'}[l]
  s=s.replace('</main>','<p class="notice">'+e(note)+'</p></main>')
 if slug in ['polityka-prywatnosci','privacy','datenschutz']:
  note={'pl':'Ten podgląd działa lokalnie na tym komputerze. Poniższa polityka opisuje witrynę produkcyjną i korespondencję e-mail; podgląd nie publikuje ani nie wysyła danych formularza.','en':'This preview runs locally on this computer. The policy below describes the production website and email correspondence; the preview does not publish or send form data.','de':'Diese Vorschau läuft lokal auf diesem Computer. Die folgende Erklärung beschreibt die produktive Website und E-Mail-Korrespondenz; die Vorschau veröffentlicht und versendet keine Formulardaten.'}[l]
  s=s.replace('</h1>','</h1><p class="notice">'+e(note)+'</p>',1)
 return s
