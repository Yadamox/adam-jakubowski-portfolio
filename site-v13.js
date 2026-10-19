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

// Original implementation: word reveals and image framing inspired by the public reference.
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches || !('IntersectionObserver' in window) || !Element.prototype.animate) return;
  const active = new Set();
  function play(el, frames, duration = 780, delay = 0) {
    if (reduced.matches) return;
    const a = el.animate(frames, {duration, delay, easing:'cubic-bezier(.22,1,.36,1)', fill:'backwards'});
    active.add(a); a.finished.then(()=>active.delete(a)).catch(()=>active.delete(a));
  }
  // Preserve spaces, semantic headings, existing emphasis and the original text.
  function heading(el) {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const nodes=[]; while(walker.nextNode()) nodes.push(walker.currentNode);
    const words=[];
    nodes.forEach(node=>{
      const fragment=document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(part=>{
        if(!part) return;
        if(/^\s+$/.test(part)) fragment.append(document.createTextNode(part));
        else {const word=document.createElement('span');word.className='motion-word';word.textContent=part;words.push(word);fragment.append(word);}
      });
      node.replaceWith(fragment);
    });
    words.forEach((word,i)=>play(word,[
      {transform:'translateY(65%)',clipPath:'inset(0 0 100% 0)'},
      {transform:'translateY(0)',clipPath:'inset(0 0 0 0)'}
    ],820,Math.min(i*45,360)));
  }
  const rise=[{opacity:.2,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}];
  document.querySelectorAll('.hero-copy h1,.page-hero h1,.simple-hero h1,.case-study-hero h1').forEach(heading);
  document.querySelectorAll('.hero-copy > .eyebrow,.hero-copy > .lead,.hero-copy > .dual-actions,.page-hero > .lead,.simple-hero > .lead,.case-study-hero > .lead').forEach((el,i)=>play(el,rise,820,Math.min(i,3)*85+90));
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(!entry.isIntersecting) return;
    const el=entry.target;observer.unobserve(el);
    if(el.matches('h2')) {heading(el);return;}
    if(el.matches('.case-gallery figure,.case-cover,.hero-visual figure,.about-grid figure,.case-feature > a')) {
      play(el,[{clipPath:'inset(0 0 18% 0)'},{clipPath:'inset(0 0 0 0)'}],1050);
      const img=el.querySelector('img');
      if(img) play(img,[{transform:'scale(1.045)'},{transform:'scale(1)'}],1250);
    } else {
      const i=el.matches('.card,.split article,.steps li,.proof-strip > div,.case-meta > div')?Array.from(el.parentElement.children).indexOf(el):0;
      play(el,rise,780,Math.min(i,3)*100);
    }
  }),{threshold:.1,rootMargin:'0px 0px -24px 0px'});
  document.querySelectorAll('.section-head h2,.cta h2,.case-gallery-head h2,.case-copy-grid h2,.case-feature h2,.about-grid h2,.section-head > p,.split article,.card,.steps li,.proof-strip > div,.boundary,.case-gallery figure,.case-cover,.hero-visual figure,.about-grid figure,.case-feature > a,.case-meta > div,.lead-form,.faq details').forEach(el=>observer.observe(el));
  const nav=document.querySelector('#nav');
  const menuObserver=new MutationObserver(()=>{
    if(!nav.classList.contains('open')) return;
    nav.querySelectorAll(':scope > a,:scope > .langs').forEach((el,i)=>play(el,[{opacity:.2,transform:'translateX(-10px)'},{opacity:1,transform:'translateX(0)'}],500,i*35));
  });
  if(nav) menuObserver.observe(nav,{attributes:true,attributeFilter:['class']});
  reduced.addEventListener('change',e=>{
    if(!e.matches) return;
    observer.disconnect();menuObserver.disconnect();active.forEach(a=>a.cancel());active.clear();
  });
})();
(() => {
  const menu=document.querySelector('.menu'),nav=document.querySelector('#nav');
  if(!menu || !nav) return;
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape' && nav.classList.contains('open')){
      nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus();
    }
  });
})();

(() => {
 const html=document.documentElement,bar=document.querySelector('.topbar'),nav=document.querySelector('#nav'),menu=document.querySelector('.menu');
 html.classList.add('enhanced');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:1280px)');
 if(bar){const scroll=()=>bar.classList.toggle('is-scrolled',scrollY>40);scroll();addEventListener('scroll',scroll,{passive:true});}
 if(nav&&menu){
  const original=menu.textContent;
  const backdrop=document.createElement('button');backdrop.className='nav-backdrop';backdrop.tabIndex=-1;backdrop.setAttribute('aria-label',menu.dataset.close);document.body.append(backdrop);
  const close=()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus();};
  const sync=()=>{const open=nav.classList.contains('open')&&mobile.matches;html.classList.toggle('menu-open',open);menu.textContent=open?menu.dataset.close:original;nav.inert=mobile.matches&&!open;};
  new MutationObserver(sync).observe(nav,{attributes:true,attributeFilter:['class']});
  backdrop.addEventListener('click',close);
  mobile.addEventListener('change',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');sync();});sync();
  document.addEventListener('keydown',e=>{
   if(e.key==='Escape'&&nav.classList.contains('open'))close();
   if(e.key!=='Tab'||!html.classList.contains('menu-open'))return;
   const items=[menu,...nav.querySelectorAll('a')],first=items[0],last=items[items.length-1];
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
   if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
  });
 }
 const rows=document.querySelectorAll('.control-timeline li');
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-seen');observer.unobserve(e.target);}}),{threshold:.45});rows.forEach(e=>observer.observe(e));}
 else rows.forEach(e=>e.classList.add('is-seen'));
 // Browsers without cross-document transitions receive a short entry, never a delayed click.
 if(!('CSSViewTransitionRule' in window)&&!reduced.matches){const main=document.querySelector('main');if(main)main.animate([{opacity:.4,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:320,easing:'ease-out'});}
})();
