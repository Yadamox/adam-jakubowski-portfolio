const fs=require('fs'),path=require('path'),P=require('../node_modules/puppeteer-core');
(async()=>{const b=await P.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',userDataDir:path.join(process.env.TMPDIR,'v16-followup-'+process.pid)});const checks=[],ck=(name,ok)=>checks.push({name,ok:!!ok});const base=(process.env.SITE_URL||'https://adam-jakubowski.com');try{const p=await b.newPage();await p.setViewport({width:390,height:844});
for(const [l,forms,offer,contact] of [['pl',['formularz-b2c','formularz-b2b'],'dla-klienta-prywatnego','kontakt'],['en',['b2c-form','b2b-form'],'private-clients','contact'],['de',['b2c-formular','b2b-formular'],'privatkunden','kontakt']]){
 for(const form of forms)for(const scope of [0,1,2]){
  await p.goto(`${base}/${l}/${form}?scope=${scope}`,{waitUntil:'networkidle0'});
  const initial=await p.$eval('[name=service]',x=>x.selectedIndex);
  for(const target of ['pl','en','de'].filter(x=>x!==l)){
   const href=await p.$eval(`.langs a[hreflang=${target}]`,x=>x.href);await p.goto(href,{waitUntil:'networkidle0'});
   ck(`${l} ${form} scope ${scope} -> ${target}`,await p.$eval('[name=service]',(x,i)=>x.selectedIndex===i,initial));
   await p.goto(`${base}/${l}/${form}?scope=${scope}`,{waitUntil:'networkidle0'});
  }
 }
 for(const form of forms){await p.goto(`${base}/${l}/${form}`,{waitUntil:'networkidle0'});const total=await p.$eval('[name=service]',x=>x.options.length);for(let i=1;i<total;i++){await p.select('[name=service]',await p.$eval('[name=service]',(s,i)=>s.options[i].value,i));const target=l==='en'?'de':'en';const href=await p.$eval(`.langs a[hreflang=${target}]`,x=>x.href);const q=await b.newPage();await q.goto(href,{waitUntil:'networkidle0'});ck(`${l} ${form} manually selected ${i}`,await q.$eval('[name=service]',(s,i)=>s.selectedIndex===i,i));await q.close();}}
 await p.goto(`${base}/${l}/${contact}?scope=2`,{waitUntil:'networkidle0'});ck(l+' contact language retains scope',await p.$$eval('.langs a',as=>as.every(a=>new URL(a.href).searchParams.get('scope')==='2')));
 await p.goto(`${base}/${l}/${offer}`,{waitUntil:'networkidle0'});ck(l+' future conditions distinguished',await p.$eval('.pricing-terms strong',x=>/dopiero|only after|erst nach/.test(x.textContent)&&/anulowanie|cancellation fees|Stornogebühren/.test(x.textContent)));
}
await p.goto(base+'/',{waitUntil:'networkidle0'});ck('root complete home',await p.evaluate(()=>!!document.querySelector('.editorial-hero')&&document.querySelectorAll('.engagement').length===3&&!!document.querySelector('.project-proof')));
}finally{await b.close();fs.writeFileSync(path.join(__dirname,'reports/followup.json'),JSON.stringify(checks,null,2));}console.log(JSON.stringify({checks:checks.length,failures:checks.filter(x=>!x.ok)},null,2));if(checks.some(x=>!x.ok))process.exitCode=1;})().catch(e=>{console.error(e);process.exitCode=1});