from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parent
langs={
'pl':{
 'home':'Start','private':'Dla klienta prywatnego','business':'Dla firm','process':'Jak pracuję','proof':'Dowody','about':'O mnie','contact':'Opisz projekt','privacy':'Polityka prywatności','faq':'FAQ','back':'Wróć na górę',
 'hero':'Prowadzę i kontroluję realizacje mebli na wymiar oraz fit-out.','lead':'Pomagam klientom prywatnym i firmom uporządkować zakres, dokumentację, decyzje, jakość, montaż i odbiór. Dwie osobne ścieżki współpracy, ten sam standard: widoczne ryzyka, pisemne ustalenia i udokumentowany rezultat.','b2c_cta':'Jestem klientem prywatnym','b2b_cta':'Reprezentuję firmę',
 'private_title':'Niezależna kontrola mebli na wymiar — przed zamówieniem, przy montażu i odbiorze.','private_lead':'Sprawdzam zakres i dostępne dokumenty, porządkuję pytania do wykonawcy oraz dokumentuję stan i poprawki. Konin + 50 km; dalej po uzgodnieniu.','business_title':'Zewnętrzny PM dla realizacji meblowych i fit-out — od diagnozy ryzyka do zamknięcia etapu.','business_lead':'Łączę dokumentację, produkcję, logistykę, gotowość miejsca, montaż i odbiór w kontrolowany proces. Wsparcie PL/EN/DE.','send_b2c':'Opisz realizację B2C','send_b2b':'Prześlij dane projektu B2B',
},
'en':{
 'home':'Home','private':'Private clients','business':'For companies','process':'How I work','proof':'Evidence','about':'About','contact':'Describe your project','privacy':'Privacy policy','faq':'FAQ','back':'Back to top',
 'hero':'I lead and control custom furniture and fit-out delivery.','lead':'I help private clients and companies structure scope, documentation, decisions, quality, installation and handover. Two distinct service paths, one standard: visible risks, written agreements and a documented outcome.','b2c_cta':'I am a private client','b2b_cta':'I represent a company',
 'private_title':'Independent control of custom furniture — before ordering, during installation and at handover.','private_lead':'I review scope and available documents, structure questions for the contractor, and document condition and corrective work. Konin + 50 km; other locations by agreement.','business_title':'External PM for custom furniture and fit-out — from risk diagnosis to stage close-out.','business_lead':'I connect documentation, production, logistics, site readiness, installation and handover in a controlled process. PL/EN/DE support.','send_b2c':'Describe a private project','send_b2b':'Submit B2B project data',
},
'de':{
 'home':'Start','private':'Privatkunden','business':'Für Unternehmen','process':'Arbeitsweise','proof':'Nachweise','about':'Über mich','contact':'Projekt beschreiben','privacy':'Datenschutz','faq':'FAQ','back':'Nach oben',
 'hero':'Ich steuere und kontrolliere Projekte für Maßmöbel und Fit-out.','lead':'Ich unterstütze Privatkunden und Unternehmen bei Leistungsumfang, Dokumentation, Entscheidungen, Qualität, Montage und Abnahme. Zwei getrennte Wege, ein Standard: sichtbare Risiken, schriftliche Festlegungen und dokumentierte Ergebnisse.','b2c_cta':'Ich bin Privatkunde','b2b_cta':'Ich vertrete ein Unternehmen',
 'private_title':'Unabhängige Kontrolle von Maßmöbeln — vor Bestellung, bei Montage und Abnahme.','private_lead':'Ich prüfe Umfang und Unterlagen, strukturiere Fragen an den Auftragnehmer und dokumentiere Zustand und Nacharbeiten. Konin + 50 km; weitere Orte nach Vereinbarung.','business_title':'Externer PM für Möbel- und Fit-out-Projekte — von der Risikodiagnose bis zum Abschluss einer Phase.','business_lead':'Ich verbinde Dokumentation, Produktion, Logistik, Baustellenbereitschaft, Montage und Abnahme zu einem kontrollierten Prozess. PL/EN/DE.','send_b2c':'Privates Projekt beschreiben','send_b2b':'B2B-Projektdaten senden',
}}

extra={
'pl':{
'b2c_products':[
('Konsultacja przed zamówieniem','Jedna oferta i dokumentacja jednej zabudowy. Rezultat: pisemna lista braków, ryzyk i pytań do wykonawcy.','590 zł — cena testowa'),
('Odbiór mebli i raport','Kontrola widocznego zakresu, dokumentacja zdjęciowa oraz raport niezgodności, spraw otwartych i elementów niesprawdzonych.','od 990 zł — cena testowa'),
('Kontrola poprawek','Ponowna kontrola wyłącznie pozycji z raportu bazowego. Rezultat: status zamknięte / częściowo / otwarte / niesprawdzalne.','od 590 zł + dojazd'),
('Opieka w limicie','Kontrola uzgodnionych etapów w limicie czasu i wizyt; rejestr decyzji, ryzyk i następnych działań.','od 3 600 zł / 12 h')],
'b2b_products':[
('Project Health Check','Diagnoza stanu, rejestr ryzyk i spraw otwartych, priorytety oraz plan 14/30 dni.','od 2 200 zł netto'),
('Sprint / kontrola etapu','Jeden krytyczny rezultat: gotowość produkcji, wysyłki, montażu, plan naprawczy albo zamknięcie listy.','od 4 500 zł netto'),
('PM etapu lub projektu','Plan, rejestry decyzji i ryzyk, statusy, kontrola interfejsów i formalne zamknięcie uzgodnionego zakresu.','po płatnej diagnozie'),
('Fractional PM','Zarezerwowane bloki czasu, KPI, SLA i przewidywalny rytm — bez obietnicy stałej dostępności.','po udanym Health Checku lub sprincie')],
'boundary':'Nie projektuję wnętrz, nie wykonuję robót, nie wydaję opinii prawnych ani ekspertyz wymagających uprawnień. Nie gwarantuję terminu, ceny lub jakości zależnych od innych stron. Dokumentuję stan, wskazuję ryzyka i kontroluję wyłącznie zakres zapisany w ofercie.',
},
'en':{
'b2c_products':[
('Pre-order consultation','One quotation and one built-in furniture scope. Outcome: written list of gaps, risks and questions for the contractor.','PLN 590 test price'),
('Furniture handover report','Visible-scope inspection, photo record and report of non-conformities, open items and unverified elements.','from PLN 990 test price'),
('Corrective-work check','A return visit limited to items in the baseline report. Outcome: closed / partial / open / not verifiable.','from PLN 590 + travel'),
('Controlled support package','Defined stages within agreed hours and visits; decisions, risks and next actions documented.','from PLN 3,600 / 12 h')],
'b2b_products':[
('Project Health Check','Current-state diagnosis, risks and open items, priorities, and a 14/30-day action plan.','from PLN 2,200 net'),
('Sprint / stage control','One critical outcome: production, dispatch or installation readiness, recovery plan or close-out.','from PLN 4,500 net'),
('Stage or project PM','Plan, decision and risk logs, reporting, interface control and formal close-out of the agreed scope.','after a paid diagnosis'),
('Fractional PM','Reserved time blocks, KPI, SLA and a predictable rhythm — not unlimited availability.','after a successful Health Check or sprint')],
'boundary':'I do not design interiors, perform construction work, provide legal opinions or regulated expert services. I do not guarantee price, timing or quality controlled by other parties. I document status, identify risks and control only the written scope.',
},
'de':{
'b2c_products':[
('Beratung vor Bestellung','Ein Angebot und eine Einbau-Situation. Ergebnis: schriftliche Liste von Lücken, Risiken und Fragen.','590 PLN Testpreis'),
('Möbelabnahme mit Bericht','Prüfung des sichtbaren Umfangs, Fotos und Bericht zu Abweichungen, offenen und ungeprüften Punkten.','ab 990 PLN Testpreis'),
('Kontrolle der Nacharbeiten','Erneute Prüfung nur der Positionen aus dem Ausgangsbericht.','ab 590 PLN + Anfahrt'),
('Begleitung mit Stundenlimit','Kontrolle vereinbarter Phasen mit begrenzten Stunden und Besuchen.','ab 3.600 PLN / 12 h')],
'b2b_products':[
('Project Health Check','Statusdiagnose, Risiko- und Offene-Punkte-Liste, Prioritäten und 14/30-Tage-Plan.','ab 2.200 PLN netto'),
('Sprint / Phasenkontrolle','Ein kritisches Ergebnis: Produktions-, Versand- oder Montagebereitschaft, Recovery oder Abschluss.','ab 4.500 PLN netto'),
('PM für Phase oder Projekt','Plan, Entscheidungs- und Risikolog, Status, Schnittstellen und formaler Abschluss.','nach bezahlter Diagnose'),
('Fractional PM','Reservierte Zeitblöcke, KPI, SLA und planbarer Rhythmus — keine ständige Verfügbarkeit.','nach Health Check oder Sprint')],
'boundary':'Ich plane keine Innenräume, führe keine Bauarbeiten aus und erbringe keine Rechts- oder Sachverständigenleistungen. Preise, Termine oder Qualität anderer Parteien werden nicht garantiert. Kontrolliert wird nur der schriftlich vereinbarte Umfang.',
}}

path_map={
'index.html':('index.html','index.html','index.html'),
'dla-klienta-prywatnego.html':('dla-klienta-prywatnego.html','private-clients.html','privatkunden.html'),
'dla-firm.html':('dla-firm.html','for-companies.html','fuer-unternehmen.html'),
'proces.html':('proces.html','process.html','arbeitsweise.html'),
'dowody.html':('dowody.html','evidence.html','nachweise.html'),
'o-mnie.html':('o-mnie.html','about.html','ueber-mich.html'),
'kontakt.html':('kontakt.html','contact.html','kontakt.html'),
'formularz-b2c.html':('formularz-b2c.html','b2c-form.html','b2c-formular.html'),
'formularz-b2b.html':('formularz-b2b.html','b2b-form.html','b2b-formular.html'),
'polityka-prywatnosci.html':('polityka-prywatnosci.html','privacy.html','datenschutz.html'),
'faq.html':('faq.html','faq.html','faq.html'),
'dziekuje.html':('dziekuje.html','thank-you.html','danke.html'),
}

def fname(canonical,lang):
    if canonical not in path_map: return canonical
    return path_map[canonical][['pl','en','de'].index(lang)]
def url(canonical,lang): return f'/{lang}/{fname(canonical,lang)}' if canonical!='index.html' else f'/{lang}/'

def head(lang,title,desc,canonical):
    alt=''.join(f'<link rel="alternate" hreflang="{l}" href="https://adam-jakubowski.com{url(canonical,l)}">' for l in langs)
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#11100f"><title>{escape(title)} — Adam Jakubowski</title><link rel="icon" href="/assets/logo-aj.svg"><link rel="stylesheet" href="/site-v9.css?v=9"><script defer src="/site-v9.js?v=9"></script><link rel="canonical" href="https://adam-jakubowski.com{url(canonical,lang)}">{alt}</head><body><a class="skip" href="#main">Skip to content</a>'''

def nav(lang):
    c=langs[lang]
    links=[('dla-klienta-prywatnego.html',c['private']),('dla-firm.html',c['business']),('proces.html',c['process']),('dowody.html',c['proof']),('o-mnie.html',c['about'])]
    alts=''.join(f'<a href="{url("index.html",l)}" lang="{l}">{l.upper()}</a>' for l in langs)
    return f'''<header class="topbar"><a class="brand" href="{url('index.html',lang)}" aria-label="Adam Jakubowski — {c['home']}"><img src="/assets/logo-aj.svg" alt=""><span><b>ADAM JAKUBOWSKI</b><small>PROJECT DELIVERY</small></span></a><button class="menu" aria-expanded="false" aria-controls="nav">Menu</button><nav id="nav">{''.join(f'<a href="{url(k,lang)}">{v}</a>' for k,v in links)}<span class="langs">{alts}</span><a class="nav-cta" href="{url('kontakt.html',lang)}">{c['contact']}</a></nav></header>'''

def foot(lang):
    c=langs[lang]
    return f'''<footer><div><b>Adam Jakubowski</b><p>Custom furniture & fit-out project delivery · Konin, Poland · PL/EN/DE</p></div><div><a href="mailto:info@adam-jakubowski.com">info@adam-jakubowski.com</a><a href="{url('privacy.html' if False else 'polityka-prywatnosci.html',lang)}">{c['privacy']}</a><a href="{url('faq.html',lang)}">FAQ</a></div><p class="fine">Scope is agreed in writing before work begins.</p></footer></body></html>'''

def cards(items):
    return '<div class="cards">'+''.join(f'<article class="card"><h3>{escape(a)}</h3><p>{escape(b)}</p><strong>{escape(d)}</strong></article>' for a,b,d in items)+'</div>'

def layout(lang,title,desc,canonical,body): return head(lang,title,desc,canonical)+nav(lang)+f'<main id="main">{body}</main>'+foot(lang)

for lang,c in langs.items():
    e=extra[lang]
    home=f'''<section class="hero"><p class="eyebrow">PROJECT DELIVERY / CUSTOM FURNITURE / FIT-OUT</p><h1>{c['hero']}</h1><p class="lead">{c['lead']}</p><div class="dual-actions"><a class="button b2c" data-track="choose_b2c" href="{url('dla-klienta-prywatnego.html',lang)}">{c['b2c_cta']}</a><a class="button b2b" data-track="choose_b2b" href="{url('dla-firm.html',lang)}">{c['b2b_cta']}</a></div></section>
<section><div class="section-head"><p>01 / TWO PATHS</p><h2>{'Wybierz właściwy punkt startu.' if lang=='pl' else 'Choose the right starting point.' if lang=='en' else 'Wählen Sie den richtigen Einstieg.'}</h2></div><div class="split"><article><span>B2C</span><h3>{c['private']}</h3><p>{c['private_lead']}</p><a class="text-link" href="{url('dla-klienta-prywatnego.html',lang)}">{c['b2c_cta']} →</a></article><article><span>B2B</span><h3>{c['business']}</h3><p>{c['business_lead']}</p><a class="text-link" href="{url('dla-firm.html',lang)}">{c['b2b_cta']} →</a></article></div></section>
<section class="dark"><div class="section-head"><p>02 / ENTRY PRODUCTS</p><h2>{'Zacznij od zamkniętego rezultatu.' if lang=='pl' else 'Start with a defined outcome.' if lang=='en' else 'Beginnen Sie mit einem definierten Ergebnis.'}</h2></div>{cards([e['b2c_products'][0],e['b2c_products'][1],e['b2b_products'][0]])}</section>
<section><div class="section-head"><p>03 / METHOD</p><h2>{'Najpierw zakres. Potem kontrola.' if lang=='pl' else 'Scope first. Then control.' if lang=='en' else 'Zuerst der Umfang. Dann die Kontrolle.'}</h2></div><ol class="steps"><li>Qualification and fit</li><li>Written outcome, scope and exclusions</li><li>Control of agreed points</li><li>Report, decision log or action plan</li><li>Formal close-out and next-step decision</li></ol><a class="text-link" href="{url('proces.html',lang)}">{c['process']} →</a></section>
<section class="boundary"><h2>{'Jasna rola od początku.' if lang=='pl' else 'A clear role from the start.' if lang=='en' else 'Eine klare Rolle von Anfang an.'}</h2><p>{e['boundary']}</p></section>
<section class="cta"><h2>{'Opisz projekt bez wybierania pakietu w ciemno.' if lang=='pl' else 'Describe the project without guessing the package.' if lang=='en' else 'Beschreiben Sie das Projekt, ohne das Paket zu erraten.'}</h2><a class="button" href="{url('kontakt.html',lang)}">{c['contact']}</a></section>'''
    (ROOT/lang).mkdir(exist_ok=True)
    (ROOT/lang/fname('index.html',lang)).write_text(layout(lang,c['home'],c['lead'],'index.html',home),encoding='utf-8')

    private=f'''<header class="page-hero"><p class="eyebrow">B2C / KONIN + 50 KM</p><h1>{c['private_title']}</h1><p class="lead">{c['private_lead']}</p><a class="button" href="{url('formularz-b2c.html',lang)}">{c['send_b2c']}</a></header><section><div class="section-head"><p>01 / SERVICES</p><h2>{c['private']}</h2></div>{cards(e['b2c_products'])}</section><section class="boundary"><h2>Scope boundaries</h2><p>{e['boundary']}</p></section><section class="cta"><h2>{c['private_title']}</h2><a class="button" href="{url('formularz-b2c.html',lang)}">{c['send_b2c']}</a></section>'''
    (ROOT/lang/fname('dla-klienta-prywatnego.html',lang)).write_text(layout(lang,c['private'],c['private_lead'],'dla-klienta-prywatnego.html',private),encoding='utf-8')

    business=f'''<header class="page-hero"><p class="eyebrow">B2B / PL · EN · DE</p><h1>{c['business_title']}</h1><p class="lead">{c['business_lead']}</p><p class="notice">{'Nie przesyłaj poufnych dokumentów przed screeningiem dopasowania i konfliktu.' if lang=='pl' else 'Do not send confidential documents before fit and conflict screening.' if lang=='en' else 'Senden Sie vor dem Fit- und Konflikt-Screening keine vertraulichen Dokumente.'}</p><a class="button" href="{url('formularz-b2b.html',lang)}">{c['send_b2b']}</a></header><section><div class="section-head"><p>01 / SERVICE LADDER</p><h2>{c['business']}</h2></div>{cards(e['b2b_products'])}</section><section class="dark"><h2>Screening first</h2><p class="lead">Client, beneficiary, key contractors, suppliers and contact source are checked before an offer, NDA and confidential materials. A non-clear result stops the process.</p></section><section class="boundary"><h2>Authority and responsibility</h2><p>{e['boundary']}</p></section><section class="cta"><h2>{c['business_title']}</h2><a class="button" href="{url('formularz-b2b.html',lang)}">{c['send_b2b']}</a></section>'''
    (ROOT/lang/fname('dla-firm.html',lang)).write_text(layout(lang,c['business'],c['business_lead'],'dla-firm.html',business),encoding='utf-8')

    process=f'''<header class="page-hero"><p class="eyebrow">METHOD</p><h1>{c['process']}</h1></header><section><ol class="steps detailed"><li><b>Qualification</b><span>Segment, need, timing, capacity and fit.</span></li><li><b>Screening for B2B</b><span>Conflict and confidentiality before documents.</span></li><li><b>Written scope</b><span>Outcome, inputs, exclusions, limits, price and timing.</span></li><li><b>Controlled execution</b><span>Only agreed points; changes require written acceptance.</span></li><li><b>Documented outcome</b><span>Report, register, gate status or action plan.</span></li><li><b>Close-out</b><span>Formal handover and decision whether another stage is needed.</span></li></ol></section><section class="boundary"><p>{e['boundary']}</p></section>'''
    (ROOT/lang/fname('proces.html',lang)).write_text(layout(lang,c['process'],'Defined scope, controlled execution and documented close-out.','proces.html',process),encoding='utf-8')

    proof=f'''<header class="page-hero"><p class="eyebrow">EVIDENCE</p><h1>{c['proof']}</h1><p class="lead">{'Zobacz format rezultatu, nie tylko deklaracje.' if lang=='pl' else 'See the format of the outcome, not only claims.' if lang=='en' else 'Sehen Sie das Ergebnisformat, nicht nur Aussagen.'}</p></header><section><div class="cards"><article class="card"><h3>Sample handover report</h3><p>Status, reference, evidence, classification, next action and closure. Example content is anonymous.</p><a class="text-link" href="/{lang}/sample-handover-report.html">Open sample →</a></article><article class="card"><h3>Pre-order checklist</h3><p>Scope, materials, dimensions, responsibilities, timing, payment, installation and handover.</p><a class="text-link" href="/{lang}/pre-order-checklist.html">Open checklist →</a></article><article class="card"><h3>Risk & decision register</h3><p>Issue, impact, owner, deadline, decision, evidence and status.</p><a class="text-link" href="/{lang}/sample-risk-register.html">Open example →</a></article></div></section><section class="case-feature"><img src="/assets/projects/landbyska-verket/landbyska-verket-cover.webp" alt="Landbyska Verket"><div><p class="eyebrow">VERIFIED PROFESSIONAL EXPERIENCE</p><h2>Landbyska Verket, Stockholm</h2><p>{'Lead Project Manager po stronie wykonawcy zabudowy meblowej — firmy STOLPIN. Case study nie sugeruje autorstwa całego wnętrza ani niezależnej realizacji.' if lang=='pl' else 'Lead Project Manager on the custom furniture contractor side — STOLPIN. The case study does not claim authorship of the whole interior or an independent commission.' if lang=='en' else 'Lead Project Manager auf Seiten des Möbelbau-Auftragnehmers STOLPIN. Keine Urheberschaft des gesamten Interieurs und kein unabhängiger Auftrag.'}</p><a class="text-link" href="/{lang}/landbyska-verket.html">Case study →</a></div></section>'''
    (ROOT/lang/fname('dowody.html',lang)).write_text(layout(lang,c['proof'],'Evidence, sample deliverables and verified professional experience.','dowody.html',proof),encoding='utf-8')

    about=f'''<header class="page-hero"><p class="eyebrow">ADAM JAKUBOWSKI</p><h1>{c['about']}</h1><p class="lead">{'Ponad 20 lat praktyki w branży meblarskiej: produkcja, zespoły, jakość, serwis i międzynarodowa koordynacja projektów.' if lang=='pl' else 'Over 20 years of practical furniture-industry experience: production, teams, quality, service and international project coordination.' if lang=='en' else 'Über 20 Jahre Praxis in der Möbelbranche: Produktion, Teams, Qualität, Service und internationale Projektkoordination.'}</p></header><section class="about-grid"><img src="/assets/adam-jakubowski-portrait.jpg" alt="Adam Jakubowski"><div><h2>Documentation → production → logistics → installation → handover</h2><p>{e['boundary']}</p><p>PL / EN / DE</p></div></section>'''
    (ROOT/lang/fname('o-mnie.html',lang)).write_text(layout(lang,c['about'],'Experience in custom furniture, quality and project delivery.','o-mnie.html',about),encoding='utf-8')

    contact=f'''<header class="page-hero compact"><p class="eyebrow">START</p><h1>{c['contact']}</h1><p class="lead">{'Najpierw wybierz segment. Formularze nie rezerwują terminu ani nie tworzą umowy.' if lang=='pl' else 'Choose the segment first. The forms do not reserve capacity or create a contract.' if lang=='en' else 'Wählen Sie zuerst das Segment. Formulare reservieren keinen Termin und begründen keinen Vertrag.'}</p></header><section><div class="split"><article><span>B2C</span><h2>{c['private']}</h2><p>{c['private_lead']}</p><a class="button" data-track="form_b2c_open" href="{url('formularz-b2c.html',lang)}">{c['send_b2c']}</a></article><article><span>B2B</span><h2>{c['business']}</h2><p>{c['business_lead']}</p><a class="button" data-track="form_b2b_open" href="{url('formularz-b2b.html',lang)}">{c['send_b2b']}</a></article></div><p class="email-line"><a href="mailto:info@adam-jakubowski.com">info@adam-jakubowski.com</a></p></section>'''
    (ROOT/lang/fname('kontakt.html',lang)).write_text(layout(lang,c['contact'],'Choose the B2C or B2B enquiry path.','kontakt.html',contact),encoding='utf-8')

    common_hidden=f'''<input type="hidden" name="_subject" value="Nowe zapytanie ze strony — {lang.upper()}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off"><input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="_next" value="https://adam-jakubowski.com{url('dziekuje.html',lang)}">'''
    consent=f'''<label class="check"><input type="checkbox" name="privacy_ack" required><span>{'Zapoznałem/am się z polityką prywatności i zgadzam się na kontakt w sprawie zapytania.' if lang=='pl' else 'I have read the privacy policy and agree to be contacted about this enquiry.' if lang=='en' else 'Ich habe die Datenschutzerklärung gelesen und stimme der Kontaktaufnahme zu.'}</span></label>'''
    b2c_form=f'''<header class="page-hero compact"><p class="eyebrow">B2C / ENQUIRY</p><h1>{c['send_b2c']}</h1><p class="lead">{c['private_lead']}</p></header><section class="form-section"><form class="lead-form" action="https://formsubmit.co/info@adam-jakubowski.com" method="POST" data-segment="B2C">{common_hidden}<input type="hidden" name="segment" value="B2C"><label>Name *<input name="name" autocomplete="name" required></label><label>Email *<input type="email" name="email" autocomplete="email" required></label><label>Phone / preferred time<input name="phone" autocomplete="tel"></label><label>Location / postal code *<input name="location" required></label><label>Stage *<select name="stage" required><option value="">—</option><option>Before order</option><option>In delivery</option><option>Installation</option><option>Handover</option><option>Corrective work</option></select></label><label>Furniture / built-in type *<input name="scope_type" required></label><label>Planned date *<input name="planned_date" required></label><label>Situation and expected outcome *<textarea name="message" rows="7" required></textarea></label><label>Source<input name="source" placeholder="LinkedIn / Google / recommendation / other"></label>{consent}<p class="fine">No attachments are accepted at this stage. Sending does not confirm a date or accept an order.</p><button class="button" type="submit">{c['send_b2c']}</button><p class="form-status" role="status" aria-live="polite"></p></form></section>'''
    (ROOT/lang/fname('formularz-b2c.html',lang)).write_text(layout(lang,c['send_b2c'],'B2C custom furniture project enquiry.','formularz-b2c.html',b2c_form),encoding='utf-8')

    b2b_form=f'''<header class="page-hero compact"><p class="eyebrow">B2B / SCREENING</p><h1>{c['send_b2b']}</h1><p class="notice">{'Nie załączaj NDA, rysunków, wycen ani materiałów poufnych. Najpierw sprawdzę dopasowanie i możliwy konflikt.' if lang=='pl' else 'Do not attach NDA, drawings, quotations or confidential material. Fit and potential conflict are checked first.' if lang=='en' else 'Keine NDA, Zeichnungen, Angebote oder vertrauliche Unterlagen senden. Zuerst erfolgen Fit- und Konfliktprüfung.'}</p></header><section class="form-section"><form class="lead-form" action="https://formsubmit.co/info@adam-jakubowski.com" method="POST" data-segment="B2B">{common_hidden}<input type="hidden" name="segment" value="B2B"><label>Name and surname *<input name="name" autocomplete="name" required></label><label>Company *<input name="company" autocomplete="organization" required></label><label>Role *<input name="role" required></label><label>Business email *<input type="email" name="email" autocomplete="email" required></label><label>Country and project location *<input name="location" required></label><label>Project type and current stage *<input name="project_stage" required></label><label>Critical date *<input name="critical_date" required></label><label>Expected outcome *<textarea name="expected_outcome" rows="5" required></textarea></label><label>Client, contractors, manufacturers or categories needed for conflict screening *<textarea name="screening_parties" rows="4" required></textarea></label><label>Preferred language *<select name="language" required><option>PL</option><option>EN</option><option>DE</option></select></label><label>Source<input name="source"></label><label class="check"><input type="checkbox" name="confidentiality_ack" required><span>I confirm that this first-stage submission contains no unapproved confidential information.</span></label>{consent}<p class="fine">Submission does not accept the project and is not permission to send confidential documents.</p><button class="button" type="submit">{c['send_b2b']}</button><p class="form-status" role="status" aria-live="polite"></p></form></section>'''
    (ROOT/lang/fname('formularz-b2b.html',lang)).write_text(layout(lang,c['send_b2b'],'B2B fit-out and custom furniture project screening.','formularz-b2b.html',b2b_form),encoding='utf-8')

    privacy=f'''<header class="page-hero compact"><p class="eyebrow">PRIVACY</p><h1>{c['privacy']}</h1></header><article class="legal"><h2>Controller and contact</h2><p>Adam Jakubowski, contact: info@adam-jakubowski.com.</p><h2>Purpose and legal basis</h2><p>Data submitted in a form are used to answer the enquiry, check fit, capacity and — for B2B — potential conflict, and to take steps requested before a possible contract. Records may also be retained where necessary for legitimate interests such as protecting claims and documenting conflict decisions.</p><h2>Data recipients</h2><p>The website is hosted on GitHub Pages. Forms are transmitted through FormSubmit to the email address above. Email, hosting and technical providers may process data under their own infrastructure and terms, potentially outside the EEA. Do not send sensitive or confidential documents at the enquiry stage.</p><h2>Retention</h2><p>Rejected enquiries are intended to be removed after 6 months; enquiries in progress after closure plus 12 months, unless a longer period is required by law, accounting or claims. Project materials are retained only as long as necessary for the service and claims.</p><h2>Your rights</h2><p>You may request access, rectification, erasure, restriction or objection where applicable and lodge a complaint with the President of the Polish Data Protection Office. Contact: info@adam-jakubowski.com.</p><h2>Cookies and analytics</h2><p>This version does not use advertising cookies or automated profiling. Basic technical files may be handled by hosting providers. The site stores no form content in local storage.</p><p class="notice">Working policy: it must be legally reviewed and updated when the business form, analytics, CRM, attachments or additional processors are selected.</p></article>'''
    (ROOT/lang/fname('polityka-prywatnosci.html',lang)).write_text(layout(lang,c['privacy'],'Privacy information for enquiries and website forms.','polityka-prywatnosci.html',privacy),encoding='utf-8')

    faq=f'''<header class="page-hero compact"><p class="eyebrow">FAQ</p><h1>FAQ</h1></header><section class="faq"><details><summary>Do you design furniture or interiors?</summary><p>No. I review and control an agreed delivery scope; I do not replace the designer or contractor.</p></details><details><summary>Do you guarantee cost, timing or quality?</summary><p>No. I document status, risks and decisions in the written scope, but do not guarantee outcomes controlled by other parties.</p></details><details><summary>What is the B2C service area?</summary><p>Konin + 50 km as the primary area. Travel beyond it is agreed individually.</p></details><details><summary>Can I send confidential B2B documents?</summary><p>Not before fit and conflict screening. The initial form does not accept attachments.</p></details><details><summary>Does the form book a date?</summary><p>No. It starts qualification only. Scope, capacity, price and terms are confirmed separately in writing.</p></details></section>'''
    (ROOT/lang/fname('faq.html',lang)).write_text(layout(lang,'FAQ','Questions about custom furniture and fit-out project support.','faq.html',faq),encoding='utf-8')

    thanks=f'''<section class="hero"><p class="eyebrow">MESSAGE RECEIVED</p><h1>{'Dziękuję. Zapytanie zostało wysłane.' if lang=='pl' else 'Thank you. Your enquiry has been sent.' if lang=='en' else 'Danke. Ihre Anfrage wurde gesendet.'}</h1><p class="lead">{'To nie jest potwierdzenie terminu ani przyjęcie zlecenia. Odpowiem po sprawdzeniu zakresu i dostępności.' if lang=='pl' else 'This is not a booking or project acceptance. I will respond after reviewing scope and capacity.' if lang=='en' else 'Dies ist keine Termin- oder Auftragsbestätigung. Ich antworte nach Prüfung von Umfang und Kapazität.'}</p><a class="button" href="{url('index.html',lang)}">{c['home']}</a></section>'''
    (ROOT/lang/fname('dziekuje.html',lang)).write_text(layout(lang,'Thank you','Enquiry confirmation.','dziekuje.html',thanks),encoding='utf-8')

    # Tangible anonymous sample deliverables.
    sample_report='''<header class="page-hero compact"><p class="eyebrow">SAMPLE / ANONYMOUS</p><h1>Sample handover report</h1><p class="lead">Illustrative format only — not a report from a client project.</p></header><article class="legal"><h2>Scope</h2><p>One fitted kitchen; visible elements and available functions compared with drawing revision 03 and the agreed finish schedule.</p><h2>Finding 01 — door alignment</h2><p><strong>Classification:</strong> observed non-conformity. <strong>Reference:</strong> drawing 03, elevation B. <strong>Evidence:</strong> visible difference in the upper edge line. <strong>Status:</strong> open. <strong>Next action:</strong> contractor to adjust and provide a completion photo.</p><h2>Finding 02 — electrical connection</h2><p><strong>Classification:</strong> not inspected. The appliance was not connected during the visit. Verification requires an authorised specialist.</p><h2>Closure</h2><p>12 points closed, 2 open, 1 not inspected. A follow-up visit is a separate service and is limited to the agreed open points.</p></article>'''
    checklist='''<header class="page-hero compact"><p class="eyebrow">CHECKLIST</p><h1>Before paying a deposit</h1></header><article class="legal"><h2>Scope and documents</h2><p>☐ Exact list of furniture and elements<br>☐ Latest drawing revision and dimensions<br>☐ Material, decor, edge, hardware and appliance specification<br>☐ Items excluded from the offer</p><h2>Responsibilities</h2><p>☐ Who measures and approves dimensions<br>☐ Who prepares utilities and the installation site<br>☐ Who coordinates other trades<br>☐ Who accepts changes and additional cost</p><h2>Timing and handover</h2><p>☐ Production, delivery and installation dates<br>☐ Conditions that move the deadline<br>☐ Handover method and defect list<br>☐ Warranty, service and complaint route</p></article>'''
    risk='''<header class="page-hero compact"><p class="eyebrow">SAMPLE / ANONYMOUS</p><h1>Risk & decision register</h1></header><article class="legal"><h2>R-01 — finish approval missing</h2><p><strong>Impact:</strong> production start blocked. <strong>Owner:</strong> client design lead. <strong>Due:</strong> agreed date. <strong>Status:</strong> open. <strong>Decision needed:</strong> approve sample A or B.</p><h2>R-02 — site not ready</h2><p><strong>Impact:</strong> installation cannot start safely. <strong>Owner:</strong> main contractor. <strong>Evidence:</strong> readiness checklist. <strong>Status:</strong> conditional.</p><h2>D-01 — dispatch gate</h2><p><strong>Decision:</strong> conditional go after closure of R-01 and written confirmation of access. <strong>Approved by:</strong> named client decision-maker.</p></article>'''
    for slug,title,body in [('sample-handover-report.html','Sample handover report',sample_report),('pre-order-checklist.html','Pre-order checklist',checklist),('sample-risk-register.html','Sample risk register',risk)]:
        (ROOT/lang/slug).write_text(layout(lang,title,'Anonymous example of a project delivery document.',slug,body),encoding='utf-8')

# root becomes canonical Polish home instead of a divergent fourth version
(ROOT/'index.html').write_text((ROOT/'pl'/'index.html').read_text(encoding='utf-8').replace('href="/pl/"','href="/"',1).replace('https://adam-jakubowski.com/pl/','https://adam-jakubowski.com/'),encoding='utf-8')

# Compatibility pages: old public URLs keep working and point to new content.
redirects={
 'zakres.html':'dla-klienta-prywatnego.html','projekty.html':'dowody.html'
}
for lang in langs:
    localized=dict(redirects)
    if lang=='en': localized.update({'o-mnie.html':'about.html','proces.html':'process.html','kontakt.html':'contact.html'})
    if lang=='de': localized.update({'o-mnie.html':'ueber-mich.html','proces.html':'arbeitsweise.html'})
    for old,new in localized.items():
        p=ROOT/lang/old
        target=url(new,lang)
        p.write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="https://adam-jakubowski.com{target}"><title>Redirect</title></head><body><a href="{target}">Continue</a></body></html>',encoding='utf-8')
for old,target in {'kontakt.html':'/pl/kontakt.html','zakres.html':'/pl/dla-klienta-prywatnego.html','proces.html':'/pl/proces.html','projekty.html':'/pl/dowody.html','o-mnie.html':'/pl/o-mnie.html'}.items():
    (ROOT/old).write_text(f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="https://adam-jakubowski.com{target}"><title>Przekierowanie</title></head><body><a href="{target}">Przejdź dalej</a></body></html>',encoding='utf-8')

# robots and sitemap
urls=[]
for lang in langs:
    for canonical in path_map:
        urls.append('https://adam-jakubowski.com'+url(canonical,lang))
    for extra_slug in ['sample-handover-report.html','pre-order-checklist.html','sample-risk-register.html','landbyska-verket.html']:
        urls.append(f'https://adam-jakubowski.com/{lang}/{extra_slug}')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://adam-jakubowski.com/sitemap.xml\n',encoding='utf-8')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>',encoding='utf-8')
print('generated',len(urls),'sitemap URLs')
