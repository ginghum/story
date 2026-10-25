'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const STORE='kasukou-story-game-v1';
let disk={};try{disk=JSON.parse(localStorage.getItem(STORE)||'{}')||{};}catch{}
const config={speed:25,font:'medium',wait:2.5,...disk.config};
let story=null,index=0,highest=Number.isInteger(disk.highest)?disk.highest:-1,read=!!disk.read,checkpoint=Number.isInteger(disk.index)?disk.index:0;
let typing=null,autoTimer=null,auto=false,skipTimer=null,skipping=false,cutinTimer=null,visibleText='',isTyping=false,activeScreen='title',dialogPaused=false;
let log=[];const cache=new Map();
let transitioning=false,transitionTimer=null,sceneTransitionVersion=0;
const escapeText=s=>String(s);
function persist(){disk={index:checkpoint,highest,read,config};try{localStorage.setItem(STORE,JSON.stringify(disk));$('#save-state').textContent='保存済み';}catch{$('#save-state').textContent='保存できません';}}
function error(s){$('#load-error').textContent=s;$('#load-error').hidden=false;}
function screen(id){cancelSceneTransition();if(id!=='game'&&document.fullscreenElement&&document.fullscreenElement!==document.documentElement){try{Promise.resolve(document.exitFullscreen()).catch(()=>{});}catch{}}dialogPaused=false;stopModes();clearTimeout(cutinTimer);clearTyping();activeScreen=id;$$('.screen').forEach(el=>el.classList.toggle('active',el.id===id));$('#stage').classList.remove('ui-hidden');updateBadges();}
function updateBadges(){$('#continue').disabled=!story||highest<0;$('#episode-status').textContent=read?'読了':highest>=0?'途中まで読んだ':'未読';}
function clearTyping(){clearInterval(typing);typing=null;isTyping=false;}
function stopModes(){auto=false;skipping=false;clearTimeout(autoTimer);clearInterval(skipTimer);$('#auto').setAttribute('aria-pressed','false');$('#skip').setAttribute('aria-pressed','false');}
function preload(src){if(!src||cache.has(src))return;const img=new Image();img.src=src;cache.set(src,img);}
function preloadNear(){for(let j=index;j<Math.min(index+12,story.entries.length);j++){const e=story.entries[j];preload(e.bg);preload(e.cg);for(const c of e.cast||[])preload(`assets/characters/${c.id}-${c.expression}.webp`);}}
function setScene(e){
 const bg=$('#backdrop');bg.style.backgroundImage=e.bg?`url("${e.bg}")`:'none';bg.className='backdrop '+(e.tone||'');
 const illustration=e.cg||((e.bgContainsCharacters||/\/cg\//.test(e.bg||''))?e.bg:null);
 const cg=$('#cg-frame');cg.dataset.tone=e.tone||'';cg.hidden=!illustration;if(illustration){$('#cg-image').src=illustration;$('#cg-image').alt=e.cgAlt||'物語の挿絵';cg.style.setProperty('--cg',`url("${illustration}")`);}
 const sprites=$('#sprites');sprites.replaceChildren();const cast=illustration?[]:(e.cast||[]);sprites.className='sprites count-'+cast.length;
 for(let i=0;i<cast.length;i++){const c=cast[i],portrait=document.createElement('div'),im=document.createElement('img');portrait.className=`sprite-portrait slot-${i}`+(c.id===e.character?' speaking':'');portrait.style.top=(11+40*(1-(c.height||175)/184))+'%';im.className='sprite';im.alt=c.name;im.src=`assets/characters/${c.id}-${c.expression}.webp`;im.style.height=(169.1*(c.height||175)/184)+'cqh';im.draggable=false;im.addEventListener('error',()=>{if(!im.isConnected)return;im.hidden=true;error('一部の画像を読み込めませんでした。文章はそのまま読めます。');},{once:true});portrait.append(im);sprites.append(portrait);}
 $('#location-label').textContent=e.location||'';
 if(e.effect&&!matchMedia('(prefers-reduced-motion: reduce)').matches){$('#flash').classList.remove('hit');$('#stage').classList.remove('shake');void $('#flash').offsetWidth;$('#flash').classList.add('hit');$('#stage').classList.add('shake');}
}
function cutinDone(){if(transitioning)return;clearTimeout(cutinTimer);$('#cutin').hidden=true;next();}
function cancelSceneTransition(){sceneTransitionVersion++;clearTimeout(transitionTimer);transitionTimer=null;transitioning=false;const overlay=$('#scene-transition');overlay.hidden=true;overlay.className='scene-transition';}
async function waitForSceneVisuals(entry){
 await Promise.all([...new Set([entry.bg,entry.cg].filter(Boolean))].map(async src=>{
  if(cache.get(src)?.complete&&cache.get(src)?.naturalWidth===0)cache.delete(src);
  preload(src);const img=cache.get(src);if(img.complete&&img.naturalWidth>0)return;
  if(typeof img.decode!=='function')return;
  let deadline;
  try{await Promise.race([img.decode(),new Promise(resolve=>{deadline=setTimeout(resolve,6000);})]);}catch{}finally{clearTimeout(deadline);}
 }));
}
function render(){
 const e=story?.entries[index];
 if(e?.type!=='location'||skipping||matchMedia('(prefers-reduced-motion: reduce)').matches){renderEntry();return;}
 cancelSceneTransition();const version=sceneTransitionVersion,visualsReady=waitForSceneVisuals(e);clearTyping();clearTimeout(autoTimer);clearTimeout(cutinTimer);
 const overlay=$('#scene-transition');transitioning=true;overlay.hidden=false;void overlay.offsetWidth;overlay.className='scene-transition blackout';
 transitionTimer=setTimeout(async()=>{await visualsReady;if(version!==sceneTransitionVersion)return;if(activeScreen!=='game'){cancelSceneTransition();return;}renderEntry();overlay.className='scene-transition reveal';transitionTimer=setTimeout(cancelSceneTransition,360);},300);
}
function renderEntry(){
 if(!story)return;clearTyping();clearTimeout(autoTimer);clearTimeout(cutinTimer);
 if(index>=story.entries.length){finish();return;}
 const e=story.entries[index];checkpoint=index;highest=Math.max(highest,index);persist();setScene(e);preloadNear();
 $('#ending').hidden=true;$('#dialogue').hidden=e.type==='location'||!!e.illustrationHold;$('#cutin').hidden=e.type!=='location';$('#progress').textContent=`${e.scene} / 10`;
 if(e.type==='location'){
  $('#cutin-place').textContent=e.location;$('#dialogue-text').textContent='';
  if(auto)cutinTimer=setTimeout(cutinDone,1700);
  return;
 }
 $('#speaker').textContent=e.speaker||'―';visibleText=e.text;$('#dialogue-text').textContent='';
 if(!log.some(x=>x.index===index))log.push({index,speaker:e.speaker,text:e.text,location:e.location});
 if(config.speed===0||skipping){completeText();return;}
 let n=0;const chars=Array.from(e.text);isTyping=true;
 typing=setInterval(()=>{n++;$('#dialogue-text').textContent=chars.slice(0,n).join('');if(n>=chars.length)completeText();},config.speed);
}
function completeText(){clearTyping();$('#dialogue-text').textContent=visibleText;scheduleAuto();}
function scheduleAuto(){clearTimeout(autoTimer);if(auto&&!dialogPaused&&activeScreen==='game')autoTimer=setTimeout(()=>next(),config.wait*1000+Math.min(visibleText.length*18,2800));}
function next(){if(transitioning)return;if(activeScreen!=='game'||dialogPaused||!$('#ending').hidden)return;if(isTyping){completeText();return;}index++;render();}
function previous(){if(transitioning)return;if(index<=0||activeScreen!=='game')return;stopModes();index--;log=log.filter(x=>x.index<=index);render();}
function begin(at=0){if(!story)return;screen('game');index=Math.max(0,Math.min(at,story.entries.length-1));log=story.entries.slice(0,index).flatMap((e,i)=>e.type==='line'?[{index:i,speaker:e.speaker,text:e.text,location:e.location}]:[]);render();}
function finish(){stopModes();clearTyping();read=true;checkpoint=story.entries.length-1;highest=checkpoint;persist();$('#cutin').hidden=true;$('#dialogue').hidden=true;$('#ending').hidden=false;updateBadges();}
function choosePrologue(){if(!story)return;if(highest>=0&&!read){$('#resume-info').textContent=`保存位置：${story.entries[Math.min(checkpoint,story.entries.length-1)].location}`;$('#resume-dialog').showModal();}else begin(0);}
function pauseForDialog(){dialogPaused=true;clearTimeout(autoTimer);clearTimeout(cutinTimer);clearInterval(skipTimer);}
function resumeFromDialog(){dialogPaused=false;if(activeScreen==='game'){if(!$('#cutin').hidden&&auto)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();if(skipping)startSkipTimer();}}
function showSettings(){pauseForDialog();$('#speed').value=config.speed;$('#font-size').value=config.font;$('#auto-wait').value=config.wait;updateSettingsLabels();$('#settings-dialog').showModal();}
function updateSettingsLabels(){$('#speed-label').textContent=config.speed===0?'即時':config.speed<=20?'速い':config.speed>=45?'ゆっくり':'標準';$('#wait-label').textContent=config.wait+' 秒';document.body.className='font-'+config.font;}
function showLog(){pauseForDialog();const target=$('#log-content');target.replaceChildren();let loc='';for(const entry of log){if(entry.location!==loc){const d=document.createElement('div');d.className='log-location';d.textContent=entry.location;target.append(d);loc=entry.location;}const row=document.createElement('div');row.className='log-entry';if(entry.speaker){const n=document.createElement('strong');n.textContent=entry.speaker;row.append(n);}const p=document.createElement('p');p.textContent=entry.text;row.append(p);target.append(row);}$('#log-dialog').showModal();requestAnimationFrame(()=>target.scrollTop=target.scrollHeight);}
function toggleAuto(){if(auto){stopModes();return;}stopModes();auto=true;$('#auto').setAttribute('aria-pressed','true');if(!$('#cutin').hidden)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();}
let skipLimit=-1;
function startSkipTimer(){clearInterval(skipTimer);skipTimer=setInterval(()=>{if(dialogPaused)return;if(index>=skipLimit){stopModes();return;}if(isTyping)completeText();else next();},90);}
function toggleSkip(){if(skipping){stopModes();return;}const limit=highest;if(index>=limit){$('#save-state').textContent='この先は未読です';return;}stopModes();skipLimit=limit;skipping=true;$('#skip').setAttribute('aria-pressed','true');startSkipTimer();}
$('#start').onclick=()=>screen('chapters');$('#continue').onclick=()=>begin(checkpoint);$('#chapter-one').onclick=()=>screen('episodes');$('#back-chapters').onclick=()=>screen('chapters');$$('[data-home]').forEach(b=>b.onclick=()=>screen('title'));$('#play-prologue').onclick=choosePrologue;
$('#game-back').onclick=()=>screen('episodes');$('#end-episodes').onclick=()=>screen('episodes');$('#replay').onclick=()=>begin(0);$('#tap-surface').onclick=()=>{if(transitioning)return;if($('#stage').classList.contains('ui-hidden')){$('#stage').classList.remove('ui-hidden');return;}if(!$('#cutin').hidden){cutinDone();return;}next();};$('#previous').onclick=previous;$('#auto').onclick=toggleAuto;$('#skip').onclick=toggleSkip;$('#hide-ui').onclick=()=>$('#stage').classList.add('ui-hidden');$('#restore-ui').onclick=()=>$('#stage').classList.remove('ui-hidden');
function updateFullscreenButtons(){const enabled=!!document.fullscreenElement;$$('[data-fullscreen]').forEach(button=>{button.textContent=enabled?'全画面を解除':'全画面';button.setAttribute('aria-pressed',String(enabled));});}
async function toggleFullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{error('このブラウザは全画面表示に対応していません。横向き表示でお楽しみください。');}finally{updateFullscreenButtons();}}
$$('[data-fullscreen]').forEach(button=>button.onclick=toggleFullscreen);
document.addEventListener('fullscreenchange',updateFullscreenButtons);
updateFullscreenButtons();
$$('.settings-open').forEach(b=>b.onclick=showSettings);$('#settings-dialog').addEventListener('close',()=>{persist();resumeFromDialog();});$('#log-open').onclick=showLog;$('#log-close').onclick=()=>$('#log-dialog').close();$('#log-dialog').addEventListener('close',resumeFromDialog);
$('#speed').oninput=e=>{config.speed=Number(e.target.value);updateSettingsLabels();};$('#font-size').onchange=e=>{config.font=e.target.value;updateSettingsLabels();};$('#auto-wait').oninput=e=>{config.wait=Number(e.target.value);updateSettingsLabels();};$('#resume-yes').onclick=()=>{$('#resume-dialog').close();begin(checkpoint);};$('#resume-no').onclick=()=>{$('#resume-dialog').close();begin(0);};$('#resume-cancel').onclick=()=>$('#resume-dialog').close();
document.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]'))return;if(activeScreen!=='game')return;const focused=document.activeElement;if(focused&&['BUTTON','INPUT','SELECT'].includes(focused.tagName))return;if([' ','Enter','ArrowRight'].includes(e.key)){e.preventDefault();$('#tap-surface').click();}else if(e.key==='ArrowLeft'){e.preventDefault();previous();}else if(e.key==='Escape'){$('#stage').classList.remove('ui-hidden');}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopModes();persist();}});window.addEventListener('pagehide',persist);
updateSettingsLabels();$('#play-prologue').disabled=true;$('#continue').disabled=true;
fetch('data/prologue.json?v=cast-7').then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json();}).then(data=>{if(!Array.isArray(data.entries)||!data.entries.length)throw Error('empty story');story=data;checkpoint=Math.min(Math.max(checkpoint,0),story.entries.length-1);highest=Math.min(highest,story.entries.length-1);$('#play-prologue').disabled=false;updateBadges();for(const src of ['assets/bg/campus.webp','assets/characters/plus-smile.webp','assets/characters/yuji-neutral.webp'])preload(src);}).catch(()=>{error('物語データを読み込めませんでした。ページを再読み込みしてください。');});
