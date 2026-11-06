const fs=require('fs'),path=require('path');
const puppeteer=require('../node_modules/puppeteer-core');
const root=__dirname,base=(process.env.SITE_URL||'https://adam-jakubowski.com');
const routes=JSON.parse(fs.readFileSync(path.join(root,'routes.json')));
const report={http:[],matrix:[],links:[],interactions:[],errors:[]};
const check=(name,ok,details)=>{report.interactions.push({name,ok:!!ok,details});if(!ok)report.errors.push({name,details})};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 fs.mkdirSync(path.join(root,'reports'),{recursive:true});fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
 for(const route of routes){const r=await fetch(base+route);const text=await r.text();const ok=r.ok&&(route.includes('dziekuje')||route.includes('thank-you')||route.includes('danke')?text.includes('noindex'):!text.includes('noindex,nofollow'));report.http.push({route,status:r.status,ok});if(!ok)report.errors.push({route,http:r.status});}
 const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-first-run','--disable-background-networking','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'],userDataDir:path.join(process.env.TMPDIR||root,'v14-chrome-'+process.pid)});
 try{
  if(process.env.RESUME_MATRIX==='1'){
   const prior=JSON.parse(fs.readFileSync(path.join(root,'reports/browser.json')));
   if(prior.matrix.length!==520||prior.http.length!==65||prior.errors.length)throw Error('Incomplete/failed matrix cannot be resumed');
   if(await (await fetch(base+'/site-v13.js?v=16')).text()!==fs.readFileSync(path.join(__dirname,'../site-v13.js'),'utf8'))throw Error('Resume asset version mismatch');
   report.http=prior.http;report.matrix=prior.matrix;report.links=prior.links;
  }else{
  let linkset=new Set();
  const jobs=routes.flatMap(route=>[false,true].flatMap(reduced=>[320,390,768,1440].map(width=>({route,reduced,width}))));
  let nextJob=0;
  await Promise.all(Array.from({length:2},async()=>{
   while(nextJob<jobs.length){
    const {route,reduced,width}=jobs[nextJob++];
    const p=await browser.newPage();await p.setViewport({width,height:900});
    if(reduced)await p.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
    const errors=[];p.on('pageerror',e=>errors.push(e.message));
    let data;const imageRetries=[];
    for(let attempt=0;attempt<2;attempt++){
    await p.goto(base+route,{waitUntil:'networkidle0',timeout:30000});
    await p.waitForSelector('#nav',{timeout:10000});
    await p.evaluate(()=>document.fonts.ready);
    data=await p.evaluate(async()=>{
     for(const img of document.images)img.loading='eager';
     await Promise.all([...document.images].map(img=>Promise.race([img.decode().catch(()=>{}),new Promise(r=>setTimeout(r,8000))])));
     await Promise.all([...document.images].map(img=>new Promise(resolve=>{const start=Date.now();const poll=()=>{if(img.complete&&img.naturalWidth>0)return resolve();if(Date.now()-start>5000)return resolve();setTimeout(poll,50)};poll()})));
     const missing=[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src);
     const links=[...document.querySelectorAll('a[href],link[rel=canonical],link[rel=alternate]')].map(a=>a.href);
     const body=document.body.innerText;
     return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,missing,links,lang:document.documentElement.lang,h1:document.querySelector('h1')?.textContent,visible:document.querySelector('main')?getComputedStyle(document.querySelector('main')).visibility:null,bodyLength:body.length};
    });
    if(!data.missing.length)break;
    imageRetries.push({attempt:attempt+1,missing:[...data.missing]});
    }
    data.imageRetries=imageRetries;
    data.links.forEach(h=>linkset.add(h));delete data.links;
    const ok=data.scrollWidth<=width&&data.missing.length===0&&errors.length===0&&data.bodyLength>100;
    report.matrix.push({route,width,reduced,ok,...data,errors});if(!ok)report.errors.push({route,width,...data,errors});
    await p.close();
   }
  }));
  report.matrix.sort((a,b)=>a.route.localeCompare(b.route)||a.width-b.width||Number(a.reduced)-Number(b.reduced));
  for(const href of [...linkset].sort()){
   const u=new URL(href);if(u.protocol==='mailto:')continue;
   if(![new URL(base).host,'adam-jakubowski.com','www.adam-jakubowski.com'].includes(u.host))continue;
   const local=base+u.pathname+u.search;let r=await fetch(local);const ok=r.ok;report.links.push({href,status:r.status,ok});if(!ok)report.errors.push({href,status:r.status});
  }
  }
  const paths={pl:['formularz-b2c','formularz-b2b','dla-klienta-prywatnego','dla-firm','proces','kontakt'],en:['b2c-form','b2b-form','private-clients','for-companies','process','contact'],de:['b2c-formular','b2b-formular','privatkunden','fuer-unternehmen','arbeitsweise','kontakt']};
  for(const [lang,a] of Object.entries(paths)){
   const p=await browser.newPage();await p.setViewport({width:390,height:844});await p.goto(base+'/'+lang+'/',{waitUntil:'networkidle0'});
   await p.click('.menu');await wait(750);check(lang+' menu opens',await p.$eval('#nav',n=>n.classList.contains('open')&&!n.inert));
   await p.keyboard.press('Escape');check(lang+' Escape closes',await p.$eval('.menu',n=>n.getAttribute('aria-expanded')==='false'));
   await p.click('.menu');await wait(750);await Promise.all([p.waitForNavigation(),p.click('#nav a[href="/'+lang+'/'+a[2]+'"]')]);check(lang+' click home to offer',p.url().endsWith(a[2]));
   for(const f of a.slice(0,2)){
    await p.goto(base+'/'+lang+'/'+f,{waitUntil:'networkidle0'});
    check(lang+' '+f+' mailto only',await p.$eval('form',f=>f.action.startsWith('mailto:')&&f.hasAttribute('data-mailto-form')));
    check(lang+' '+f+' native required validation',await p.$eval('form',f=>!f.checkValidity()));
    // Capture generated mailto via temporary replacement of this one navigation statement; never open mail app or send email.
    const js=fs.readFileSync(path.join(__dirname,'../site-v13.js'),'utf8').split('// Original implementation:')[0].replace('window.location.href=destination.toString();','window.__capturedMailto=destination.toString();');
    await p.evaluate(()=>{const f=document.querySelector('form');const c=f.cloneNode(true);f.replaceWith(c)});
    await p.evaluate(js);
    await p.evaluate(()=>{const f=document.querySelector('form');for(const el of f.elements){if(el.tagName==='BUTTON')continue;if(el.type==='checkbox')el.checked=true;else if(el.tagName==='SELECT')el.selectedIndex=el.options[0].value===''?1:0;else if(el.type==='email')el.value='preview@example.invalid';else if(el.type!=='hidden')el.value='TEST LOCAL';}f.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));});
    const captured=await p.evaluate(()=>window.__capturedMailto||'');check(lang+' '+f+' generated mailto without sending',captured.startsWith('mailto:info@adam-jakubowski.com?')&&captured.includes('body='));
   }
   await p.goto(base+'/'+lang+'/',{waitUntil:'networkidle0'});await p.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
   await p.waitForFunction(()=>matchMedia('(prefers-reduced-motion: reduce)').matches&&document.getAnimations().filter(a=>a.playState==='running').length===0&&getComputedStyle(document.documentElement).scrollBehavior==='auto',{timeout:3000});
   check(lang+' reduced-motion live change',await p.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length===0&&getComputedStyle(document.documentElement).scrollBehavior==='auto'));
   await p.setJavaScriptEnabled(false);await p.reload({waitUntil:'networkidle0'});check(lang+' no JS text and navigation',await p.evaluate(()=>document.querySelector('main').innerText.length>200&&getComputedStyle(document.querySelector('#nav')).display!=='none'));
   await p.setJavaScriptEnabled(true);await p.emulateMediaFeatures([]);await p.close();
  }
  // Screenshots with real approved motion allowed to settle, including scrolled sections.
  for(const [lang,a] of Object.entries(paths))for(const [name,slug] of [['home',''],['b2c',a[2]],['b2b',a[3]],['process',a[4]],['contact',a[5]]])for(const width of [390,1440]){
   const p=await browser.newPage();await p.setViewport({width,height:width===390?844:1000});await p.goto(base+'/'+lang+'/'+slug,{waitUntil:'networkidle0'});
   await p.evaluate(async()=>{for(const img of document.images)img.loading='eager';for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,70))}scrollTo(0,0)});await wait(1500);
   await p.screenshot({path:path.join(root,'screenshots',`${lang}-${name}-${width}.png`),fullPage:true});
   if(name==='home')await p.screenshot({path:path.join(root,'screenshots',`${lang}-home-${width}-viewport.png`)});await p.close();
  }
 }finally{await browser.close();fs.writeFileSync(path.join(root,'reports/browser.json'),JSON.stringify(report,null,2));}
 console.log(JSON.stringify({http:report.http.length,matrix:report.matrix.length,links:report.links.length,interactions:report.interactions.length,failures:report.errors},null,2));if(report.errors.length)process.exitCode=1;
})().catch(e=>{fs.writeFileSync(path.join(root,'reports/browser-partial.json'),JSON.stringify(report,null,2));console.error(e);process.exitCode=1});
