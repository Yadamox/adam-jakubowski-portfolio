// Local-only message preparation. No network request, storage, or claim of delivery.
(() => {
 const params=new URLSearchParams(location.search),language=document.documentElement.lang||'en';
 const messages={
 pl:{invalid:'Uzupełnij wymagane pola.',ready:'Próba otwarcia programu pocztowego. Wiadomość nie została wysłana przez stronę. Jeśli program się nie otworzył, skopiuj treść poniżej i wyślij ją samodzielnie.',copied:'Skopiowano adres, temat i treść. Wklej je do swojej poczty i wyślij wiadomość.',manual:'Nie udało się skopiować automatycznie. Zaznaczono treść poniżej — skopiuj ją ręcznie i wyślij ze swojej poczty.',to:'Do',subject:'Temat'},
 en:{invalid:'Please complete the required fields.',ready:'Attempting to open your email application. The website has not sent your message. If the application did not open, copy the text below and send it yourself.',copied:'Address, subject and message copied. Paste them into your email and send the message.',manual:'Automatic copying was unavailable. The text below is selected — copy it manually and send it from your email.',to:'To',subject:'Subject'},
 de:{invalid:'Bitte füllen Sie die Pflichtfelder aus.',ready:'Ihr E-Mail-Programm wird angefordert. Die Website hat keine Nachricht versendet. Falls sich kein Programm öffnet, kopieren Sie den Text unten und versenden Sie ihn selbst.',copied:'Adresse, Betreff und Nachricht kopiert. Fügen Sie diese in Ihre E-Mail ein und versenden Sie die Nachricht.',manual:'Automatisches Kopieren war nicht möglich. Der Text unten ist markiert — kopieren Sie ihn manuell und versenden Sie ihn aus Ihrem Postfach.',to:'An',subject:'Betreff'}
 };
 const text=messages[language]||messages.en;
 document.querySelectorAll('[data-mailto-form]').forEach(form=>{
  if(form.__enquiryReady)return;
  form.__enquiryReady=true;
  const service=params.get('service');
  if(service&&[...form.elements.service.options].some(o=>o.value===service))form.elements.service.value=service;
  const copy=form.querySelector('.copy-message'),panel=form.querySelector('.draft-message'),draft=form.querySelector('[data-email-draft]'),status=form.querySelector('.form-status');
  if(copy)copy.hidden=false;
  function prepare(){
   if(!form.checkValidity()){form.reportValidity();status.textContent=text.invalid;return null;}
   const lines=[];
   for(const [name,value] of new FormData(form).entries()){
    const clean=String(value).trim();
    if(!clean)continue;
    const field=form.elements[name];
    const label=(field?.closest('label')?.childNodes[0]?.textContent||name).trim().replace(/\s+/g,' ');
    lines.push(`${label}: ${clean}`);
   }
   lines.push('',`page: ${location.href.split('?')[0]}`);
   const subject=`${form.dataset.subject}: ${form.elements.service.value}`;
   const destination=new URL(form.action);
   destination.searchParams.set('subject',subject);destination.searchParams.set('body',lines.join('\n'));
   draft.value=`${text.to}: ${destination.pathname}\n${text.subject}: ${subject}\n\n${lines.join('\n')}`;
   panel.hidden=false;
   return destination;
  }
  form.addEventListener('submit',event=>{
   event.preventDefault();const destination=prepare();if(!destination)return;
   status.textContent=text.ready;
   window.location.href=destination.toString();
  });
  copy?.addEventListener('click',async()=>{
   if(!prepare())return;
   try{await navigator.clipboard.writeText(draft.value);status.textContent=text.copied;}
   catch(_){draft.focus();draft.select();status.textContent=text.manual;}
  });
  // Do not leave an old, potentially misleading draft after editing the enquiry.
  form.addEventListener('input',event=>{if(event.target===draft)return;panel.hidden=true;draft.value='';status.textContent='';});
 });
})();
