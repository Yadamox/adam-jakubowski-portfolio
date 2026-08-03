const $=(s,p=document)=>p.querySelector(s);const $$=(s,p=document)=>[...p.querySelectorAll(s)];
const images=['/assets/project-stockholm.svg','/assets/project-dresden.svg','/assets/hero-render.svg'];
const supportedLangs=['pl','en','de'];const pathLang=location.pathname.split('/').filter(Boolean)[0];let lang=supportedLangs.includes(pathLang)?pathLang:(localStorage.getItem('siteLang')||'pl');if(!supportedLangs.includes(lang))lang='pl';
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in-view');revealObserver.unobserve(entry.target)}}),{threshold:.12,rootMargin:'0px 0px -7%'});
function observeReveals(){requestAnimationFrame(()=>$$('.reveal,.service,.project-card,.step,.fact').forEach(el=>{if(!el.classList.contains('in-view'))revealObserver.observe(el)}))}
function setText(selector,value){const el=$(selector);if(el)el.textContent=value||''}
function setHTML(selector,value){const el=$(selector);if(el)el.innerHTML=value||''}
function pageName(){const name=location.pathname.split('/').filter(Boolean).pop()||'index.html';return name.includes('.')?name:'index.html'}
function localizeLinks(l){const page=pageName();$$('a[href]').forEach(a=>{const href=a.getAttribute('href');if(!href||href.startsWith('#')||href.startsWith('mailto:')||href.startsWith('http'))return;const file=href.split('/').pop()||'index.html';a.href=`/${l}/${file}`});$$('[data-lang]').forEach(a=>a.href=`/${a.dataset.lang}/${page}`)}
function render(l){lang=l;localStorage.setItem('siteLang',l);const c=window.SITE_CONTENT[l];localizeLinks(l);document.documentElement.lang=l;document.title=c.pageTitle;const meta=$('[name=description]');if(meta)meta.content=c.metaDescription;
  $$('[data-i18n]').forEach(e=>e.textContent=c.ui[e.dataset.i18n]||'');$$('[data-section]').forEach(e=>e.textContent=c.sections[e.dataset.section]||'');
  setText('#eyebrow',c.eyebrow);setText('#heroTitle',c.heroTitle);setText('#heroLead',c.heroLead);setText('#aboutTitle',c.aboutTitle);setHTML('#aboutText',c.about.map(x=>`<p>${x}</p>`).join(''));
  setHTML('#facts',c.facts.map(x=>`<div class="fact"><b>${x[0]}</b><span>${x[1]}</span></div>`).join(''));
  setHTML('#services',c.services.map((x,i)=>`<article class="service"><span>${String(i+1).padStart(2,'0')}</span><div><h3>${x[0]}</h3><p>${x[1]}</p></div></article>`).join(''));
  setHTML('#projectGrid',c.projects.map((x,i)=>`<article class="project-card"><img src="${images[i]}" alt="${x[1]}"><div class="project-body"><small>${x[0]}</small><h3>${x[1]}</h3><p>${x[2]}</p><b>${x[3]}</b></div></article>`).join(''));
  setHTML('#steps',c.steps.map((x,i)=>`<article class="step"><span>${i+1}</span><div><h3>${x[0]}</h3><p>${x[1]}</p></div></article>`).join(''));
  $$('[data-lang]').forEach(b=>{b.classList.toggle('active',b.dataset.lang===l);b.setAttribute('aria-pressed',b.dataset.lang===l)});observeReveals();
}

const menu=$('.menu');if(menu)menu.addEventListener('click',()=>{const nav=$('.nav nav'),open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',open)});$$('.nav a').forEach(a=>a.addEventListener('click',()=>{const nav=$('.nav nav');if(nav)nav.classList.remove('open');if(menu)menu.setAttribute('aria-expanded','false')}));
const form=$('#contactForm');if(form)form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(e.currentTarget),c=window.SITE_CONTENT[lang];const body=`${c.mailLabels.name}: ${d.get('name')}\n${c.mailLabels.email}: ${d.get('email')}\n\n${d.get('message')}`;location.href=`mailto:info@adam-jakubowski.com?subject=${encodeURIComponent(d.get('subject'))}&body=${encodeURIComponent(body)}`});
let ticking=false;function updateScrollEffects(){const max=document.documentElement.scrollHeight-innerHeight,progress=max>0?scrollY/max:0;const bar=$('.scroll-progress');if(bar)bar.style.transform=`scaleX(${progress})`;const nav=$('.nav');if(nav)nav.classList.toggle('scrolled',scrollY>30);if(!reduceMotion){const hero=$('[data-parallax]');if(hero&&scrollY<innerHeight*1.3)hero.style.setProperty('--parallax-y',`${Math.min(scrollY*.045,34)}px`)}ticking=false}addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(updateScrollEffects);ticking=true}},{passive:true});updateScrollEffects();
setText('#footerName',`© ${new Date().getFullYear()} Adam Jakubowski`);render(lang);
