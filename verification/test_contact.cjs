const fs=require('fs'),path=require('path'),P=require('../node_modules/puppeteer-core');
const R=__dirname,B=(process.env.SITE_URL||'https://adam-jakubowski.com'),checks=[];
const ck=(name,ok,data)=>checks.push({name,ok:!!ok,data});
const routes={pl:['kontakt','formularz-b2c','formularz-b2b'],en:['contact','b2c-form','b2b-form'],de:['kontakt','b2c-formular','b2b-formular']};
const expected={B2C:['email','location','message','name','service'],B2B:['company','confidentiality_ack','email','expected_outcome','location','name','service']};
(async()=>{const browser=await P.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',userDataDir:path.join(process.env.TMPDIR,'v16-contact-'+process.pid),args:['--disable-background-timer-throttling','--disable-renderer-backgrounding'],protocolTimeout:90000});
try{for(const [l,a] of Object.entries(routes)){
 const p=await browser.newPage();await p.setViewport({width:390,height:844});await p.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
 for(let scope=0;scope<3;scope++)for(let segment=1;segment<=2;segment++){
  await p.goto(B+'/'+l+'/',{waitUntil:'networkidle0'});
  const selector='.engagement:nth-child('+(scope+1)+')';
  ck(l+' real scope link '+scope+' '+segment,await p.$eval(selector,x=>x.tagName==='A'&&!!x.href&&x.tabIndex===0));
  await p.focus(selector);await Promise.all([p.waitForNavigation({waitUntil:'networkidle0'}),p.keyboard.press('Enter')]);
  ck(l+' keyboard scope reaches contact '+scope+' '+segment,new URL(p.url()).pathname==='/'+l+'/'+a[0]&&new URL(p.url()).searchParams.get('scope')===String(scope));
  const target=await p.$eval('.split article:nth-child('+segment+') a',x=>x.href);
  await Promise.all([p.waitForNavigation({waitUntil:'networkidle0'}),p.click('.split article:nth-child('+segment+') a')]);
  const result=await p.$eval('[name=service]',s=>({value:s.value,expected:[...s.querySelectorAll('option[data-kind=new]')].map(x=>x.value),kind:s.selectedOptions[0].dataset.kind}));
  ck(l+' scope survives audience selection '+scope+' '+segment,result.value===result.expected[scope]&&result.kind==='new'&&new URL(p.url()).pathname==='/'+l+'/'+a[segment],{target,result});
 }
 for(let segment=1;segment<=2;segment++){
  const prefix=l+' '+segment;
  await p.goto(B+'/'+l+'/'+a[segment],{waitUntil:'networkidle0'});
  const required=await p.$$eval('form [required]',els=>els.map(x=>x.name).sort());
  ck(prefix+' exact required fields preserved',JSON.stringify(required)===JSON.stringify(expected[segment===1?'B2C':'B2B']),required);
  ck(prefix+' no required field inside closed details',await p.$$eval('details [required]',els=>els.length===0));
  ck(prefix+' no false privacy prohibition',await p.$eval('.enquiry-privacy',x=>!/Nie wpisuj danych osób fizycznych, danych kontaktowych|Do not enter personal or contact data|Keine personenbezogenen oder Kontaktdaten/.test(x.textContent)&&/osób trzecich|third-party|Dritter/.test(x.textContent)));
  await p.click('.copy-message');
  ck(prefix+' invalid form produces no draft',await p.$eval('.draft-message',x=>x.hidden));
  await p.evaluate(()=>{
   const f=document.querySelector('form');for(const el of f.elements){if(!el.name)continue;if(el.type==='checkbox')el.checked=true;else if(el.tagName==='SELECT'){if(el.name==='service')el.value=el.querySelector('[data-kind=new]').value;}else if(el.name==='email')el.value='preview@example.invalid';else if(el.type!=='hidden')el.value='TEST LOCAL — Łódź, Prüfung, & question?';}
   Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.__copied=text;}}});
  });
  await p.click('.copy-message');
  await p.waitForFunction(()=>!!window.__copied);
  const copied=await p.evaluate(()=>({value:window.__copied,draft:document.querySelector('[data-email-draft]').value,visible:!document.querySelector('.draft-message').hidden,status:document.querySelector('.form-status').innerText}));
  ck(prefix+' clipboard contains full local enquiry',copied.visible&&copied.value===copied.draft&&copied.value.includes('info@adam-jakubowski.com')&&copied.value.includes('preview@example.invalid')&&copied.value.includes('Łódź, Prüfung, & question?'),copied);
  await p.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw new Error('Permission denied test')};});
  await p.click('.copy-message');await p.waitForFunction(()=>document.activeElement?.matches('[data-email-draft]'));
  ck(prefix+' denied clipboard has selected manual fallback',await p.$eval('[data-email-draft]',x=>x.selectionStart===0&&x.selectionEnd===x.value.length&&x.value.length>0));
  // Exercise submit with intercepted navigation; never contact an external system.
  const script=fs.readFileSync(path.join(__dirname,'../site-v13.js'),'utf8').split('// Original implementation:')[0].replace('window.location.href=destination.toString();','window.__capturedMailto=destination.toString();');
  await p.evaluate(()=>{const f=document.querySelector('form'),c=f.cloneNode(true);for(const el of f.elements){if(!el.name)continue;const target=c.elements[el.name];if(el.type==='checkbox')target.checked=el.checked;else target.value=el.value;}f.replaceWith(c)});await p.evaluate(script);
  await p.evaluate(()=>document.querySelector('form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));
  const sent=await p.evaluate(()=>({url:window.__capturedMailto,status:document.querySelector('.form-status').textContent}));
  ck(prefix+' mailto preserves content and does not claim delivery',!!sent.url&&new URL(sent.url).searchParams.get('body').includes('preview@example.invalid')&&/nie została wysłana|has not sent|keine Nachricht versendet/.test(sent.status),sent);
  await p.type('[name=name]','X');ck(prefix+' edits invalidate stale draft',await p.$eval('.draft-message',x=>x.hidden));
  await p.screenshot({path:path.join(R,'screenshots',`${l}-contact-fixed-${segment}-390.png`),fullPage:true});
  ck(prefix+' no horizontal overflow',await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 }
 await p.goto(B+'/'+l+'/',{waitUntil:'networkidle0'});
 ck(l+' different experience image',await p.evaluate(()=>document.querySelector('.hero-scene img').src!==document.querySelector('.project-proof img').src));
 ck(l+' hero identifies audience and interiors',await p.$eval('.hero-summary',x=>/wnętrz|interior|Innenraum/.test(x.textContent)&&/prywatnych|private clients|Privatkunden/.test(x.textContent)));
 await p.close();
}}finally{await browser.close();fs.writeFileSync(path.join(R,'reports/contact.json'),JSON.stringify(checks,null,2));}
console.log(JSON.stringify({checks:checks.length,failures:checks.filter(x=>!x.ok)},null,2));if(checks.some(x=>!x.ok))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
