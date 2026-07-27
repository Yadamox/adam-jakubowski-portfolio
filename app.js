const $=(s,p=document)=>p.querySelector(s);const $$=(s,p=document)=>[...p.querySelectorAll(s)];
const images=['assets/project-stockholm.svg','assets/project-dresden.svg','assets/hero-render.svg'];
let lang=localStorage.getItem('siteLang')||'pl';if(!['pl','en','de'].includes(lang))lang='pl';
function render(l){lang=l;localStorage.setItem('siteLang',l);const c=window.SITE_CONTENT[l];document.documentElement.lang=l;document.title=c.pageTitle;$('[name=description]').content=c.metaDescription;
  $$('[data-i18n]').forEach(e=>e.textContent=c.ui[e.dataset.i18n]||'');$$('[data-section]').forEach(e=>e.textContent=c.sections[e.dataset.section]||'');
  $('#eyebrow').textContent=c.eyebrow;$('#heroTitle').textContent=c.heroTitle;$('#heroLead').textContent=c.heroLead;$('#aboutTitle').textContent=c.aboutTitle;$('#aboutText').innerHTML=c.about.map(x=>`<p>${x}</p>`).join('');
  $('#facts').innerHTML=c.facts.map(x=>`<div class="fact"><b>${x[0]}</b><span>${x[1]}</span></div>`).join('');
  $('#services').innerHTML=c.services.map((x,i)=>`<article class="service"><span>${String(i+1).padStart(2,'0')}</span><div><h3>${x[0]}</h3><p>${x[1]}</p></div></article>`).join('');
  $('#projectGrid').innerHTML=c.projects.map((x,i)=>`<article class="project-card"><img src="${images[i]}" alt="${x[1]}"><div class="project-body"><small>${x[0]}</small><h3>${x[1]}</h3><p>${x[2]}</p><b>${x[3]}</b></div></article>`).join('');
  $('#steps').innerHTML=c.steps.map((x,i)=>`<article class="step"><span>${i+1}</span><div><h3>${x[0]}</h3><p>${x[1]}</p></div></article>`).join('');
  $$('[data-lang]').forEach(b=>{b.classList.toggle('active',b.dataset.lang===l);b.setAttribute('aria-pressed',b.dataset.lang===l)});
}
$$('[data-lang]').forEach(b=>b.addEventListener('click',()=>render(b.dataset.lang)));
const menu=$('.menu');menu.addEventListener('click',()=>{const open=$('.nav nav').classList.toggle('open');menu.setAttribute('aria-expanded',open)});$$('.nav a').forEach(a=>a.addEventListener('click',()=>{$('.nav nav').classList.remove('open');menu.setAttribute('aria-expanded','false')}));
$('#contactForm').addEventListener('submit',e=>{e.preventDefault();const d=new FormData(e.currentTarget),c=window.SITE_CONTENT[lang];const body=`${c.mailLabels.name}: ${d.get('name')}\n${c.mailLabels.email}: ${d.get('email')}\n\n${d.get('message')}`;location.href=`mailto:info@adam-jakubowski.com?subject=${encodeURIComponent(d.get('subject'))}&body=${encodeURIComponent(body)}`});
$('#footerName').textContent=`© ${new Date().getFullYear()} Adam Jakubowski`;render(lang);