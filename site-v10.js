(()=>{
  const menu=document.querySelector('.menu');
  const nav=document.querySelector('#nav');
  if(menu&&nav){
    menu.addEventListener('click',()=>{
      const open=nav.classList.toggle('open');
      menu.setAttribute('aria-expanded',String(open));
    });
  }

  const params=new URLSearchParams(location.search);
  const messages={
    pl:{invalid:'Uzupełnij wymagane pola.',ready:'Wiadomość została przygotowana w programie pocztowym. Wyślij ją, aby przekazać zapytanie.'},
    en:{invalid:'Please complete the required fields.',ready:'The message has been prepared in your email application. Send it to submit your enquiry.'},
    de:{invalid:'Bitte füllen Sie die Pflichtfelder aus.',ready:'Die Nachricht wurde in Ihrem E-Mail-Programm vorbereitet. Senden Sie sie, um Ihre Anfrage zu übermitteln.'}
  };
  const language=document.documentElement.lang||'en';

  document.querySelectorAll('[data-mailto-form]').forEach(form=>{
    const service=params.get('service');
    if(service&&form.elements.service&&[...form.elements.service.options].some(option=>option.value===service)){
      form.elements.service.value=service;
    }

    form.addEventListener('submit',event=>{
      event.preventDefault();
      const status=form.querySelector('.form-status');
      if(!form.checkValidity()){
        form.reportValidity();
        if(status) status.textContent=(messages[language]||messages.en).invalid;
        return;
      }

      const lines=[];
      for(const [name,value] of new FormData(form).entries()){
        const clean=String(value).trim();
        if(clean) lines.push(`${name}: ${clean}`);
      }
      lines.push('',`page: ${location.href.split('?')[0]}`);
      const subject=`${form.dataset.subject}: ${form.elements.service.value}`;
      const destination=new URL(form.action);
      destination.searchParams.set('subject',subject);
      destination.searchParams.set('body',lines.join('\n'));
      if(status) status.textContent=(messages[language]||messages.en).ready;
      window.location.href=destination.toString();
    });
  });
})();
