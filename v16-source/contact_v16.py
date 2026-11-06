"""Small first enquiry, explicit local email handling, no external processor."""
import re
from html import escape as e
TEXT={
'pl':dict(intro='Wystarczy krótki opis projektu i lokalizacja. Szczegóły ustalimy w dalszej rozmowie.',optional='(opcjonalnie)',message='Projekt, obecny etap i potrzebna pomoc ',privacy='polityka-prywatnosci',policy='Polityka prywatności',note='Podaj własne dane do odpowiedzi. Nie wpisuj danych osób trzecich, danych wrażliwych ani informacji poufnych lub objętych NDA. Formularz nie wysyła danych ze strony: otwiera program pocztowy albo pozwala skopiować wiadomość do własnej poczty. Wysyłasz ją samodzielnie.',copy='Skopiuj wiadomość',fallback='Nie masz programu pocztowego? Skopiuj treść i wyślij ją ze swojej poczty na',draft='Treść do skopiowania',contact='Możesz też napisać bez formularza. Podaj lokalizację, obecny etap i potrzebną pomoc.'),
'en':dict(intro='A short project description and location are enough to start. We can discuss the details afterwards.',optional='(optional)',message='Project, current stage and support needed ',privacy='privacy',policy='Privacy policy',note='Provide your own contact details for a reply. Do not enter third-party personal data, sensitive data, confidential information or NDA-protected content. This form does not send data from the website: it opens your email application or lets you copy the message into your own email. You send it yourself.',copy='Copy message',fallback='No email application? Copy the message and send it from your own email to',draft='Message to copy',contact='You can also email me without the form. Include the location, current stage and support needed.'),
'de':dict(intro='Für den Anfang genügen eine kurze Projektbeschreibung und der Ort. Einzelheiten klären wir im weiteren Gespräch.',optional='(optional)',message='Projekt, aktuelle Phase und benötigte Unterstützung ',privacy='datenschutz',policy='Datenschutz',note='Geben Sie Ihre eigenen Kontaktdaten für die Antwort an. Keine personenbezogenen Daten Dritter, sensiblen Daten, vertraulichen Informationen oder NDA-Inhalte eingeben. Dieses Formular versendet keine Daten von der Website: Es öffnet Ihr E-Mail-Programm oder ermöglicht das Kopieren der Nachricht in Ihre eigene E-Mail. Sie versenden die Nachricht selbst.',copy='Nachricht kopieren',fallback='Kein E-Mail-Programm? Kopieren Sie den Text und senden Sie ihn aus Ihrem eigenen Postfach an',draft='Nachricht zum Kopieren',contact='Sie können auch ohne Formular schreiben. Nennen Sie Ort, aktuelle Phase und die benötigte Unterstützung.')}

def form_content(form,l,i,gate):
 t=TEXT[l]
 # Keep the company for conflict screening. Move nonessential separate stage/language questions to details.
 names=['project_stage','language'] if i==6 else ['stage']
 moved=[]
 for name in names:
  pattern=r'<label>[^<]*(?:<span[^>]*>[^<]*</span>)?<(?:input|select)\b[^>]*name="'+name+r'".*?</label>'
  m=re.search(pattern,form,re.S)
  if not m: raise ValueError('Missing optional field '+name)
  field=m.group().replace(' required','')
  field=re.sub(r'<span aria-hidden="true">\*</span>',f'<span class="optional">{e(t["optional"])}</span>',field)
  if name=='language':
   field=field.replace('<option>'+l.upper()+'</option>','<option selected>'+l.upper()+'</option>')
  moved.append(field);form=form[:m.start()]+form[m.end():]
 form=form.replace('<div><label>', '<div>'+''.join(moved)+'<label>',1)
 if i==6:
  form=re.sub(r'(<label>)[^<]*(?=<span aria-hidden="true">\*</span><textarea name="expected_outcome")',lambda m:m[1]+e(t['message']),form)
 form=re.sub(r'<p class="fine">.*?</p>',f'<p class="fine enquiry-privacy">{e(t["note"])} <a href="/{l}/{t["privacy"]}">{e(t["policy"])}</a>.</p>',form,flags=re.S)
 form=form.replace('<button class="button" type="submit">',gate+'<div class="enquiry-actions"><button class="button" type="submit">',1)
 form=form.replace('</button><p class="form-status"', '</button><button class="button copy-message" type="button" hidden>'+e(t['copy'])+'</button></div><p class="direct-email">'+e(t['fallback'])+' <a href="mailto:info@adam-jakubowski.com">info@adam-jakubowski.com</a>.</p><div class="draft-message" hidden><label>'+e(t['draft'])+'<textarea data-email-draft rows="10" readonly></textarea></label></div><p class="form-status"',1)
 return form

def direct_contact(l):
 return '<div class="direct-contact"><h3>info@adam-jakubowski.com</h3><p>'+e(TEXT[l]['contact'])+'</p><a class="quiet-link" href="mailto:info@adam-jakubowski.com">info@adam-jakubowski.com <span aria-hidden="true">↗</span></a></div>'
