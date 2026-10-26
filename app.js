'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const STORE='kasukou-story-game-v1';
let disk={};try{disk=JSON.parse(localStorage.getItem(STORE)||'{}')||{};}catch{}
if(!disk.episodes)disk.episodes={prologue:{index:disk.index||0,highest:Number.isInteger(disk.highest)?disk.highest:-1,read:!!disk.read}};
const config={speed:25,font:'medium',wait:2.5,seEnabled:true,seVolume:0.55,bgmEnabled:true,bgmVolume:0.35,...disk.config};
let episodeId='prologue',manifest=[],storyCache=new Map(),loadingEpisode=false,loadVersion=0,pendingEpisode=null;
let story=null,index=0,highest=Number.isInteger(disk.highest)?disk.highest:-1,read=!!disk.read,checkpoint=Number.isInteger(disk.index)?disk.index:0;
let typing=null,autoTimer=null,auto=false,skipTimer=null,skipping=false,cutinTimer=null,visibleText='',isTyping=false,activeScreen='title',dialogPaused=false;
let lastSeKey='',suppressSeKey='';
let log=[];const cache=new Map();
let transitioning=false,transitionTimer=null,sceneTransitionVersion=0;
const escapeText=s=>String(s);
function persist(){const episodes={...(disk.episodes||{}),[episodeId]:{index:checkpoint,highest,read}};disk={index:checkpoint,highest,read,config,episodeId,episodes};try{localStorage.setItem(STORE,JSON.stringify(disk));$('#save-state').textContent='保存済み';}catch{$('#save-state').textContent='保存できません';}}
let errorTimer=null;
function clearError(){clearTimeout(errorTimer);errorTimer=null;$('#load-error').hidden=true;}
function error(s,{temporary=false}={}){clearError();$('#error-message').textContent=s;$('#load-error').hidden=false;if(temporary)errorTimer=setTimeout(clearError,6000);}
if(!$('#error-message')||!$('#dismiss-error')){const message=document.createElement('span'),close=document.createElement('button');message.id='error-message';close.id='dismiss-error';close.type='button';close.textContent='×';close.setAttribute('aria-label','案内を閉じる');$('#load-error').replaceChildren(message,close);}
$('#dismiss-error').onclick=clearError;
function screen(id){clearError();window.storySfx?.stop();cancelSceneTransition();if(id!=='game'&&document.fullscreenElement&&document.fullscreenElement!==document.documentElement){try{Promise.resolve(document.exitFullscreen()).catch(()=>{});}catch{}}dialogPaused=false;stopModes();clearTimeout(cutinTimer);clearTyping();activeScreen=id;if(id!=='game')window.storyBgm?.set('daily',config);$$('.screen').forEach(el=>el.classList.toggle('active',el.id===id));$('#stage').classList.remove('ui-hidden');updateBadges();}
function savedEpisode(id){if(disk.episodes?.[id])return disk.episodes[id];if(id==='prologue'&&!disk.episodes)return {index:disk.index||0,highest:Number.isInteger(disk.highest)?disk.highest:-1,read:!!disk.read};return {index:0,highest:-1,read:false};}
function updateBadges(){const saved=savedEpisode(disk.episodeId||'prologue');$('#continue').disabled=loadingEpisode||!manifest.length||saved.highest<0;for(const item of manifest){const badge=document.querySelector(`[data-status="${item.id}"]`);const data=item.id===episodeId?{read,highest}:savedEpisode(item.id);if(badge)badge.textContent=data.read?'読了':data.highest>=0?'途中まで読んだ':'未読';}}
async function loadEpisode(id){const meta=manifest.find(e=>e.id===id);if(!meta)throw Error('episode missing');const version=++loadVersion;loadingEpisode=true;$('#episode-loading').hidden=false;clearError();updateBadges();try{let data=storyCache.get(id);if(!data){const response=await fetch(meta.file+'?v=episode1-order-v2');if(!response.ok)throw Error('HTTP '+response.status);data=await response.json();if(!Array.isArray(data.entries)||!data.entries.length)throw Error('empty story');storyCache.set(id,data);}if(version!==loadVersion)return false;stopModes();clearTyping();cancelSceneTransition();const save=savedEpisode(id);cache.clear();episodeId=id;story=data;index=0;checkpoint=Math.max(0,Math.min(save.index||0,data.entries.length-1));highest=Math.min(Number.isInteger(save.highest)?save.highest:-1,data.entries.length-1);read=!!save.read;return true;}finally{if(version===loadVersion){loadingEpisode=false;$('#episode-loading').hidden=true;updateBadges();}}}
async function chooseEpisode(id,continuing=false){if(loadingEpisode)return;const originScreen=activeScreen;try{if(!await loadEpisode(id)||activeScreen!==originScreen)return;if(continuing){begin(checkpoint);return;}if(highest>=0&&!read){pendingEpisode=id;$('#resume-info').textContent=`${story.title} ／ 保存位置：${story.entries[checkpoint].location}`;$('#resume-dialog').showModal();}else begin(0);}catch{error('この話を読み込めませんでした。通信を確認して、もう一度選択してください。');}}
function renderEpisodeCards(){$('#chapter-summary').textContent=`プロローグ・第1〜${manifest.length-1}話を収録`;const target=$('#episode-list');target.replaceChildren();for(const [i,item] of manifest.entries()){const button=document.createElement('button');button.className='episode-card';button.id=item.id==='prologue'?'play-prologue':'play-'+item.id;const imageWrap=document.createElement('div');imageWrap.className='episode-image';const img=document.createElement('img');img.src=item.image;img.alt=item.imageAlt||'';img.loading='lazy';const tag=document.createElement('span');tag.textContent=i===0?'PROLOGUE':`EPISODE ${String(i).padStart(2,'0')}`;imageWrap.append(img,tag);const content=document.createElement('div');content.className='episode-content';const badge=document.createElement('span');badge.className='status';badge.dataset.status=item.id;if(i===0)badge.id='episode-status';const title=document.createElement('h3');title.textContent=item.title;const desc=document.createElement('p');desc.textContent=item.description;const link=document.createElement('span');link.className='episode-link';link.textContent='物語を読む →';content.append(badge,title,desc,link);button.append(imageWrap,content);button.onclick=()=>chooseEpisode(item.id);target.append(button);}updateBadges();}
function clearTyping(){clearInterval(typing);typing=null;isTyping=false;}
function stopModes(){auto=false;skipping=false;clearTimeout(autoTimer);clearInterval(skipTimer);$('#auto').setAttribute('aria-pressed','false');$('#skip').setAttribute('aria-pressed','false');}
function preload(src){if(!src)return;if(cache.has(src)){const img=cache.get(src);cache.delete(src);cache.set(src,img);return;}const img=new Image();img.src=src;cache.set(src,img);while(cache.size>18)cache.delete(cache.keys().next().value);}
function preloadNear(){for(let j=index;j<Math.min(index+12,story.entries.length);j++){const e=story.entries[j];preload(e.bg);preload(e.cg);for(const c of e.cast||[])preload(`assets/characters/${c.id}-${c.expression}.webp`);}}
function setScene(e){
 window.storyBgm?.set(e.bgm||null,config);
 const bg=$('#backdrop');bg.style.backgroundImage=e.bg?`url("${e.bg}")`:'none';bg.className='backdrop '+(e.tone||'');
 const illustration=e.cg||((e.bgContainsCharacters||/\/cg\//.test(e.bg||''))?e.bg:null);
 const cg=$('#cg-frame');cg.dataset.tone=e.tone||'';cg.hidden=!illustration;if(illustration){$('#cg-image').src=illustration;$('#cg-image').alt=e.cgAlt||'物語の挿絵';cg.style.setProperty('--cg',`url("${illustration}")`);}
 const sprites=$('#sprites');sprites.replaceChildren();const cast=illustration?[]:(e.cast||[]);sprites.className='sprites count-'+cast.length;
 for(let i=0;i<cast.length;i++){const c=cast[i],portrait=document.createElement('div'),im=document.createElement('img');portrait.className=`sprite-portrait slot-${i}`+(c.id===e.character?' speaking':'');portrait.style.top=(11+40*(1-(c.height||175)/184))+'%';im.className='sprite';im.alt=c.name;im.src=`assets/characters/${c.id}-${c.expression}.webp`;im.style.height=(169.1*(c.height||175)/184)+'cqh';im.draggable=false;im.addEventListener('error',()=>{if(!im.isConnected)return;im.hidden=true;error('一部の画像を読み込めませんでした。文章はそのまま読めます。');},{once:true});portrait.append(im);sprites.append(portrait);}
 $('#location-label').textContent=e.location||'';
 if(e.effect&&!matchMedia('(prefers-reduced-motion: reduce)').matches){$('#flash').classList.remove('hit');$('#flash').classList.remove('blink');$('#stage').classList.remove('shake');void $('#flash').offsetWidth;if(e.effect==='teleport')$('#flash').classList.add('blink');else{$('#flash').classList.add('hit');$('#stage').classList.add('shake');}}
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
 const e=story.entries[index];checkpoint=index;highest=Math.max(highest,index);persist();setScene(e);preloadNear();const seKey=episodeId+':'+index;if(e.se&&!skipping&&seKey!==lastSeKey&&seKey!==suppressSeKey)window.storySfx?.play(e.se,config);lastSeKey=seKey;suppressSeKey='';
 $('#ending').hidden=true;$('#dialogue').hidden=e.type==='location'||!!e.illustrationHold;$('#cutin').hidden=e.type!=='location';$('#progress').textContent=`${e.scene} / ${story.source_scenes||10}`;
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
function previous(){if(transitioning)return;if(index<=0||activeScreen!=='game')return;stopModes();index--;suppressSeKey=episodeId+':'+index;log=log.filter(x=>x.index<=index);render();}
function begin(at=0){if(!story)return;screen('game');index=Math.max(0,Math.min(at,story.entries.length-1));lastSeKey='';suppressSeKey=episodeId+':'+index;log=story.entries.slice(0,index).flatMap((e,i)=>e.type==='line'?[{index:i,speaker:e.speaker,text:e.text,location:e.location}]:[]);render();}
function finish(){window.storyBgm?.set('reflection',config);const pos=manifest.findIndex(e=>e.id===episodeId),following=manifest[pos+1];$('#ending-label').textContent=episodeId==='prologue'?'PROLOGUE — COMPLETE':`EPISODE ${pos} — COMPLETE`;$('#ending-title').textContent=story.title;$('#ending-caption').textContent='読了';$('#next-episode').hidden=!following;$('#next-episode').textContent=following?'次の話へ → '+following.title:'';$('#next-episode').onclick=()=>following&&chooseEpisode(following.id);stopModes();clearTyping();read=true;checkpoint=story.entries.length-1;highest=checkpoint;persist();$('#cutin').hidden=true;$('#dialogue').hidden=true;$('#ending').hidden=false;updateBadges();}
function pauseForDialog(){window.storySfx?.stop();dialogPaused=true;clearTimeout(autoTimer);clearTimeout(cutinTimer);clearInterval(skipTimer);}
function resumeFromDialog(){dialogPaused=false;if(activeScreen==='game'){if(!$('#cutin').hidden&&auto)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();if(skipping)startSkipTimer();}}
function showSettings(){pauseForDialog();$('#speed').value=config.speed;$('#font-size').value=config.font;$('#auto-wait').value=config.wait;$('#se-volume').value=Math.round(config.seVolume*100);$('#se-enabled').checked=config.seEnabled;$('#se-test-status').textContent='';if($('#bgm-volume')){$('#bgm-volume').value=Math.round(config.bgmVolume*100);$('#bgm-enabled').checked=config.bgmEnabled;$('#bgm-test-status').textContent='';$('#bgm-stop-preview').disabled=true;}updateSettingsLabels();$('#settings-dialog').showModal();}
function updateSettingsLabels(){$('#speed-label').textContent=config.speed===0?'即時':config.speed<=20?'速い':config.speed>=45?'ゆっくり':'標準';$('#wait-label').textContent=config.wait+' 秒';$('#se-volume-label').textContent=Math.round(config.seVolume*100)+'%';window.storySfx?.volume(config);if($('#bgm-volume-label'))$('#bgm-volume-label').textContent=Math.round(config.bgmVolume*100)+'%';window.storyBgm?.volume(config);document.body.className='font-'+config.font;}
function showLog(){pauseForDialog();const target=$('#log-content');target.replaceChildren();let loc='';for(const entry of log){if(entry.location!==loc){const d=document.createElement('div');d.className='log-location';d.textContent=entry.location;target.append(d);loc=entry.location;}const row=document.createElement('div');row.className='log-entry';if(entry.speaker){const n=document.createElement('strong');n.textContent=entry.speaker;row.append(n);}const p=document.createElement('p');p.textContent=entry.text;row.append(p);target.append(row);}$('#log-dialog').showModal();requestAnimationFrame(()=>target.scrollTop=target.scrollHeight);}
function toggleAuto(){if(auto){stopModes();return;}stopModes();auto=true;$('#auto').setAttribute('aria-pressed','true');if(!$('#cutin').hidden)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();}
let skipLimit=-1;
function startSkipTimer(){clearInterval(skipTimer);skipTimer=setInterval(()=>{if(dialogPaused)return;if(index>=skipLimit){stopModes();return;}if(isTyping)completeText();else next();},90);}
function toggleSkip(){if(skipping){stopModes();return;}const limit=highest;if(index>=limit){$('#save-state').textContent='この先は未読です';return;}stopModes();window.storySfx?.stop();skipLimit=limit;skipping=true;$('#skip').setAttribute('aria-pressed','true');startSkipTimer();}
$('#start').onclick=()=>screen('chapters');$('#continue').onclick=()=>chooseEpisode(disk.episodeId||'prologue',true);$('#chapter-one').onclick=()=>screen('episodes');$('#back-chapters').onclick=()=>screen('chapters');$$('[data-home]').forEach(b=>b.onclick=()=>screen('title'));
$('#game-back').onclick=()=>screen('episodes');$('#end-episodes').onclick=()=>screen('episodes');$('#replay').onclick=()=>begin(0);$('#tap-surface').onclick=()=>{if(transitioning)return;if($('#stage').classList.contains('ui-hidden')){$('#stage').classList.remove('ui-hidden');return;}if(!$('#cutin').hidden){cutinDone();return;}next();};$('#previous').onclick=previous;$('#auto').onclick=toggleAuto;$('#skip').onclick=toggleSkip;$('#hide-ui').onclick=()=>$('#stage').classList.add('ui-hidden');$('#restore-ui').onclick=()=>$('#stage').classList.remove('ui-hidden');
let fullscreenRejected=false;
function canFullscreen(){return !fullscreenRejected&&document.fullscreenEnabled===true&&typeof document.documentElement.requestFullscreen==='function'&&typeof document.exitFullscreen==='function';}
function updateFullscreenButtons(){const enabled=!!document.fullscreenElement;$$('[data-fullscreen]').forEach(button=>{button.hidden=!enabled&&!canFullscreen();button.textContent=enabled?'全画面を解除':'全画面';button.setAttribute('aria-pressed',String(enabled));});}
async function toggleFullscreen(){if(!document.fullscreenElement&&!canFullscreen()){updateFullscreenButtons();return;}try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();clearError();}catch{if(!document.fullscreenElement)fullscreenRejected=true;error('全画面表示を切り替えられませんでした。そのままの画面でお楽しみいただけます。',{temporary:true});}finally{updateFullscreenButtons();}}
$$('[data-fullscreen]').forEach(button=>button.onclick=toggleFullscreen);
document.addEventListener('fullscreenchange',updateFullscreenButtons);
updateFullscreenButtons();
$$('.settings-open').forEach(b=>b.onclick=showSettings);$('#settings-dialog').addEventListener('close',()=>{window.storyBgm?.cancelPreview();persist();resumeFromDialog();});$('#log-open').onclick=showLog;$('#log-close').onclick=()=>$('#log-dialog').close();$('#log-dialog').addEventListener('close',resumeFromDialog);
if($('#bgm-volume')){$('#bgm-volume').oninput=e=>{config.bgmVolume=Number(e.target.value)/100;updateSettingsLabels();persist();};$('#bgm-enabled').onchange=e=>{config.bgmEnabled=e.target.checked;updateSettingsLabels();persist();};$('#bgm-test').onclick=async()=>{$('#bgm-test-status').textContent='BGMを読み込み中…';$('#bgm-test').disabled=true;const ok=await window.storyBgm?.preview($('#bgm-sample').value,config);$('#bgm-test-status').textContent=ok?'BGMを試聴しています':!config.bgmEnabled||config.bgmVolume===0?'BGMがミュートされています':'BGMを準備できませんでした。もう一度お試しください';$('#bgm-stop-preview').disabled=!ok;$('#bgm-test').disabled=false;};$('#bgm-stop-preview').onclick=()=>{window.storyBgm?.cancelPreview();$('#bgm-test-status').textContent='場面のBGMに戻しました';$('#bgm-stop-preview').disabled=true;};}
$('#se-volume').oninput=e=>{config.seVolume=Number(e.target.value)/100;updateSettingsLabels();persist();};$('#se-enabled').onchange=e=>{config.seEnabled=e.target.checked;updateSettingsLabels();persist();};$('#se-test').onclick=async()=>{$('#se-test-status').textContent=await window.storySfx?.preview($('#se-sample').value,config)?'テストSEを再生しました':config.seEnabled&&config.seVolume>0?'音声を準備できませんでした。もう一度お試しください':'SEがミュートされています';};
$('#speed').oninput=e=>{config.speed=Number(e.target.value);updateSettingsLabels();};$('#font-size').onchange=e=>{config.font=e.target.value;updateSettingsLabels();};$('#auto-wait').oninput=e=>{config.wait=Number(e.target.value);updateSettingsLabels();};$('#resume-yes').onclick=()=>{$('#resume-dialog').close();if(pendingEpisode===episodeId)begin(checkpoint);};$('#resume-no').onclick=()=>{$('#resume-dialog').close();if(pendingEpisode===episodeId)begin(0);};$('#resume-cancel').onclick=()=>$('#resume-dialog').close();
document.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]'))return;if(activeScreen!=='game')return;const focused=document.activeElement;if(focused&&['BUTTON','INPUT','SELECT'].includes(focused.tagName))return;if([' ','Enter','ArrowRight'].includes(e.key)){e.preventDefault();$('#tap-surface').click();}else if(e.key==='ArrowLeft'){e.preventDefault();previous();}else if(e.key==='Escape'){$('#stage').classList.remove('ui-hidden');}});
document.addEventListener('click',e=>{if(e.target.closest?.('.title-actions button,#chapter-one,.episode-card,[data-home],#back-chapters,#game-back,#end-episodes,#next-episode,.settings-open,#log-open,#log-close,#resume-yes,#resume-no,#resume-cancel,.close-settings'))window.storySfx?.play('ui',config);});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopModes();persist();}});window.addEventListener('pagehide',persist);
updateSettingsLabels();window.storyBgm?.set('daily',config);$('#continue').disabled=true;
fetch('data/episodes.json?v=chapter1-8').then(r=>{if(!r.ok)throw Error('manifest');return r.json();}).then(async data=>{manifest=data.episodes;renderEpisodeCards();await loadEpisode(manifest.some(e=>e.id===disk.episodeId)?disk.episodeId:'prologue');for(const src of ['assets/bg/campus.webp','assets/characters/plus-smile.webp','assets/characters/yuji-neutral.webp'])preload(src);}).catch(()=>error('物語データを読み込めませんでした。ページを再読み込みしてください。'));
