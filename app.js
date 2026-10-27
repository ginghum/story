'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const STORE='kasukou-story-game-v1';
let disk={};try{disk=JSON.parse(localStorage.getItem(STORE)||'{}')||{};}catch{}
if(!disk.episodes)disk.episodes={prologue:{index:disk.index||0,highest:Number.isInteger(disk.highest)?disk.highest:-1,read:!!disk.read}};
const config={speed:25,font:'medium',wait:2.5,seEnabled:true,seVolume:0.55,bgmEnabled:true,bgmVolume:0.35,...disk.config};
let activeCollection='main';
const collectionFor=id=>id.startsWith('extra')?'extras':id.startsWith('chapter2-')?'chapter2':'main';
const collectionEpisodes=collection=>manifest.filter(e=>collectionFor(e.id)===collection);
let episodeId='prologue',manifest=[],storyCache=new Map(),loadingEpisode=false,loadVersion=0,pendingEpisode=null;
let story=null,index=0,highest=Number.isInteger(disk.highest)?disk.highest:-1,read=!!disk.read,checkpoint=Number.isInteger(disk.index)?disk.index:0;
let typing=null,autoTimer=null,auto=false,skipTimer=null,skipping=false,cutinTimer=null,visibleText='',isTyping=false,activeScreen='title',dialogPaused=false;
let holdTimer=null,holdPointer=null,holdSkipping=false,suppressHoldClick=false;
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
async function loadEpisode(id){const meta=manifest.find(e=>e.id===id);if(!meta)throw Error('episode missing');const version=++loadVersion;loadingEpisode=true;$('#episode-loading').hidden=false;clearError();updateBadges();try{let data=storyCache.get(id);if(!data){const response=await fetch(meta.file+'?v=hood-cold-v1');if(!response.ok)throw Error('HTTP '+response.status);data=await response.json();if(!Array.isArray(data.entries)||!data.entries.length)throw Error('empty story');storyCache.set(id,data);}if(version!==loadVersion)return false;stopModes();clearTyping();cancelSceneTransition();const save=savedEpisode(id);cache.clear();episodeId=id;story=data;index=0;checkpoint=Math.max(0,Math.min(save.index||0,data.entries.length-1));highest=Math.min(Number.isInteger(save.highest)?save.highest:-1,data.entries.length-1);read=!!save.read;return true;}finally{if(version===loadVersion){loadingEpisode=false;$('#episode-loading').hidden=true;updateBadges();}}}
async function chooseEpisode(id,continuing=false){if(loadingEpisode)return;const originScreen=activeScreen;try{if(!await loadEpisode(id)||activeScreen!==originScreen)return;if(continuing){begin(checkpoint);return;}if(highest>=0&&!read){pendingEpisode=id;$('#resume-info').textContent=`${story.title} ／ 保存位置：${story.entries[checkpoint].location}`;$('#resume-dialog').showModal();}else begin(0);}catch{error('この話を読み込めませんでした。通信を確認して、もう一度選択してください。');}}
function renderEpisodeCards(){document.querySelector('#episodes .eyebrow').textContent=activeCollection==='extras'?'EXTRA STORIES':activeCollection==='chapter2'?'MAIN STORY / CHAPTER 02':'MAIN STORY / CHAPTER 01';document.querySelector('#episodes h2').textContent=activeCollection==='extras'?'おまけ':activeCollection==='chapter2'?'第2章':'第1章';$('#chapter-summary').textContent='プロローグ・第1〜21話／第1章完結';const target=$('#episode-list');target.replaceChildren();for(const [i,item] of collectionEpisodes(activeCollection).entries()){const button=document.createElement('button');button.className='episode-card';button.id=item.id==='prologue'?'play-prologue':'play-'+item.id;const imageWrap=document.createElement('div');imageWrap.className='episode-image';const img=document.createElement('img');img.src=item.image;img.alt=item.imageAlt||'';img.loading='lazy';const tag=document.createElement('span');tag.textContent=item.id.startsWith('extra')?'EXTRA '+item.id.slice(5):item.id==='prologue'?'PROLOGUE':`EPISODE ${String(Number(item.id.split('episode').at(-1))).padStart(2,'0')}`;imageWrap.append(img,tag);const content=document.createElement('div');content.className='episode-content';const badge=document.createElement('span');badge.className='status';badge.dataset.status=item.id;if(i===0)badge.id='episode-status';const title=document.createElement('h3');title.textContent=item.title;const desc=document.createElement('p');desc.textContent=item.description;const link=document.createElement('span');link.className='episode-link';link.textContent='物語を読む →';content.append(badge,title,desc,link);button.append(imageWrap,content);button.onclick=()=>chooseEpisode(item.id);target.append(button);}document.querySelector('#episodes .archive-header>span').textContent=activeCollection==='extras'?'EXTRA STORIES':activeCollection==='chapter2'?'CHAPTER 02':'CHAPTER 01';$('.more-coming').textContent=activeCollection==='extras'?'本編の向こうにある、五つの物語。':activeCollection==='chapter2'?'第2章 全24話を収録。':'第1章 全21話・プロローグを収録。';updateBadges();}
function clearTyping(){clearInterval(typing);typing=null;isTyping=false;}
function cancelHold(){clearTimeout(holdTimer);holdTimer=null;holdPointer=null;holdSkipping=false;}
function stopModes(){cancelHold();auto=false;skipping=false;clearTimeout(autoTimer);clearInterval(skipTimer);$('#auto').setAttribute('aria-pressed','false');$('#skip').setAttribute('aria-pressed','false');}
function characterImage(c){return `assets/characters/${c.id}-${c.expression}.webp`+(c.id==='minus-masked'?'?v=hood-round-mask-v2':'')+(c.id==='yuhi'&&['serious','worried'].includes(c.expression)?'?v=black-eyes-v1':'');}
function preload(src){if(!src)return;if(cache.has(src)){const img=cache.get(src);cache.delete(src);cache.set(src,img);return;}const img=new Image();img.src=src;cache.set(src,img);while(cache.size>18)cache.delete(cache.keys().next().value);}
function preloadNear(){for(let j=index;j<Math.min(index+12,story.entries.length);j++){const e=story.entries[j];preload(e.bg);preload(e.cg);for(const c of e.cast||[])preload(characterImage(c));}}
function setScene(e){
 window.storyBgm?.set(e.bgm||null,config);
 const bg=$('#backdrop');bg.style.backgroundImage=e.bg?`url("${e.bg}")`:'none';bg.className='backdrop '+(e.tone||'');
 const illustration=e.cg||((e.bgContainsCharacters||/\/cg\//.test(e.bg||''))?e.bg:null);
 const cg=$('#cg-frame');cg.dataset.tone=e.tone||'';cg.hidden=!illustration;if(illustration){$('#cg-image').src=illustration;$('#cg-image').alt=e.cgAlt||'物語の挿絵';cg.style.setProperty('--cg',`url("${illustration}")`);}
 const sprites=$('#sprites');sprites.replaceChildren();const cast=illustration?[]:(e.cast||[]);sprites.className='sprites count-'+cast.length;
 for(let i=0;i<cast.length;i++){const c=cast[i],portrait=document.createElement('div'),im=document.createElement('img');portrait.className=`sprite-portrait slot-${i}`+(c.id===e.character?' speaking':'');portrait.style.top=(11+40*(1-(c.height||175)/184))+'%';im.className='sprite';im.alt=c.name;im.src=characterImage(c);im.style.height=(169.1*(c.height||175)/184)+'cqh';im.draggable=false;im.addEventListener('error',()=>{if(!im.isConnected)return;im.hidden=true;error('一部の画像を読み込めませんでした。文章はそのまま読めます。');},{once:true});portrait.append(im);sprites.append(portrait);}
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
// Keep saved entry offsets stable: minor location markers remain in the script,
// but playback passes over them in either direction without pausing the prose.
function locationArea(e){
 const place=e.location||'',bg=e.bg||'';
 for(const [pattern,area] of [[/勉強サークル/,'study'],[/能力練習場|早朝の練習場|寮裏の練習場/,'training'],[/旧校舎|不良サークル/,'old-school'],[/学生寮/,'dorm'],[/保健室|保健委員会|保健の窓口/,'clinic'],[/新聞部/,'newsroom'],[/闘技場|決闘委員会/,'arena'],[/図書館/,'library'],[/オタクサークル|離れ校舎/,'club']])if(pattern.test(place))return area;
 if(/校舎|学園/.test(place)&&/classroom|corridor|campus/.test(bg))return 'classrooms';
 if(/中庭/.test(place))return 'courtyard';
 if(/購買/.test(place))return 'shop';
 return bg;
}
function locationTime(e){
 const place=e.location||'';
 if(/深夜|消灯|就寝/.test(place))return 'bedtime';
 if(/夜/.test(place))return 'night';
 if(/夕方|夕食/.test(place))return 'evening';
 if(/早朝|朝|午前/.test(place))return 'morning';
 if(/午後|昼/.test(place))return 'day';
 return '';
}
function showLocationCutin(at){
 if(at===0)return true;
 const e=story.entries[at],previous=story.entries[at-1];
 if(e.transition==='inline')return false;if(e.transition==='major')return true;
 if(!previous||!e.bg||!previous.bg)return true;
 if(/^(回想|夢|Xの記憶)/.test(e.location)!==/^(回想|夢|Xの記憶)/.test(previous.location)||/翌|数日後|消灯後/.test(e.location))return true;
 const time=locationTime(e),before=locationTime(previous);
 if(time&&before&&time!==before)return true;
 // A corridor, doorway or the nearby stands do not interrupt an ongoing scene.
 if(e.bg===previous.bg||locationArea(e)===locationArea(previous))return false;
 // Brief passing shots lead straight into the next location in the same scene.
 {
  let lines=0;
  for(let i=at+1;i<story.entries.length&&lines<=5;i++){
   const next=story.entries[i];
   if(next.type==='location')return next.scene!==e.scene||/翌|数日後|回想/.test(next.location);
   if(next.type==='line')lines++;
  }
 }
 return true;
}
function render(direction=1){
 while(story?.entries[index]?.type==='location'&&!showLocationCutin(index))index+=direction;
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
function previous(){if(transitioning)return;if(index<=0||activeScreen!=='game')return;stopModes();index--;while(story.entries[index]?.type==='location'&&!showLocationCutin(index))index--;suppressSeKey=episodeId+':'+index;log=log.filter(x=>x.index<=index);render(-1);}
function begin(at=0){if(!story)return;screen('game');index=Math.max(0,Math.min(at,story.entries.length-1));lastSeKey='';suppressSeKey=episodeId+':'+index;log=story.entries.slice(0,index).flatMap((e,i)=>e.type==='line'?[{index:i,speaker:e.speaker,text:e.text,location:e.location}]:[]);render();}
function finish(){window.storyBgm?.set('reflection',config);const list=collectionEpisodes(collectionFor(episodeId)),pos=list.findIndex(e=>e.id===episodeId),following=list[pos+1]||(episodeId==='chapter1-episode21'?collectionEpisodes('chapter2')[0]:null);$('#ending-label').textContent=episodeId==='prologue'?'PROLOGUE — COMPLETE':episodeId.startsWith('extra')?`EXTRA ${episodeId.slice(5)} — COMPLETE`:`EPISODE ${Number(episodeId.split('episode').at(-1))} — COMPLETE`;$('#ending-title').textContent=story.title;$('#ending-caption').textContent=episodeId==='chapter1-episode21'?'第1章 完':episodeId==='chapter2-episode24'?'第2章 完':'読了';$('#next-episode').hidden=!following;$('#next-episode').textContent=following?'次の話へ → '+following.title:'';$('#next-episode').onclick=()=>following&&chooseEpisode(following.id);stopModes();clearTyping();read=true;checkpoint=story.entries.length-1;highest=checkpoint;persist();$('#cutin').hidden=true;$('#dialogue').hidden=true;$('#ending').hidden=false;updateBadges();}
function pauseForDialog(){if(holdSkipping)stopModes();else cancelHold();window.storySfx?.stop();dialogPaused=true;clearTimeout(autoTimer);clearTimeout(cutinTimer);clearInterval(skipTimer);}
function resumeFromDialog(){dialogPaused=false;if(activeScreen==='game'){if(!$('#cutin').hidden&&auto)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();if(skipping)startSkipTimer();}}
function showSettings(){pauseForDialog();$('#speed').value=config.speed;$('#font-size').value=config.font;$('#auto-wait').value=config.wait;$('#se-volume').value=Math.round(config.seVolume*100);$('#se-enabled').checked=config.seEnabled;$('#se-test-status').textContent='';if($('#bgm-volume')){$('#bgm-volume').value=Math.round(config.bgmVolume*100);$('#bgm-enabled').checked=config.bgmEnabled;$('#bgm-test-status').textContent='';$('#bgm-stop-preview').disabled=true;}updateSettingsLabels();$('#settings-dialog').showModal();}
function updateSettingsLabels(){$('#speed-label').textContent=config.speed===0?'即時':config.speed<=20?'速い':config.speed>=45?'ゆっくり':'標準';$('#wait-label').textContent=config.wait+' 秒';$('#se-volume-label').textContent=Math.round(config.seVolume*100)+'%';window.storySfx?.volume(config);if($('#bgm-volume-label'))$('#bgm-volume-label').textContent=Math.round(config.bgmVolume*100)+'%';window.storyBgm?.volume(config);document.body.className='font-'+config.font;}
function showLog(){pauseForDialog();const target=$('#log-content');target.replaceChildren();let loc='';for(const entry of log){if(entry.location!==loc){const d=document.createElement('div');d.className='log-location';d.textContent=entry.location;target.append(d);loc=entry.location;}const row=document.createElement('div');row.className='log-entry';if(entry.speaker){const n=document.createElement('strong');n.textContent=entry.speaker;row.append(n);}const p=document.createElement('p');p.textContent=entry.text;row.append(p);target.append(row);}$('#log-dialog').showModal();requestAnimationFrame(()=>target.scrollTop=target.scrollHeight);}
function toggleAuto(){if(auto){stopModes();return;}stopModes();auto=true;$('#auto').setAttribute('aria-pressed','true');if(!$('#cutin').hidden)cutinTimer=setTimeout(cutinDone,1700);else if(!isTyping)scheduleAuto();}
let skipLimit=-1;
function startSkipTimer(){clearInterval(skipTimer);skipTimer=setInterval(()=>{if(dialogPaused)return;if(index>=skipLimit){stopModes();return;}if(isTyping)completeText();else next();},90);}
function toggleSkip(){if(skipping){stopModes();return;}const limit=highest;if(index>=limit){$('#save-state').textContent='この先は未読です';return;}stopModes();window.storySfx?.stop();skipLimit=limit;skipping=true;$('#skip').setAttribute('aria-pressed','true');startSkipTimer();}
// Long press is momentary and may cross the unread boundary; the Skip button keeps its read-only limit.
function endHold(e){if(e&&e.pointerId!==holdPointer)return;if(holdSkipping)stopModes();else cancelHold();}
const tapSurface=$('#tap-surface');
tapSurface.onpointerdown=e=>{
 if(e.isPrimary===false||e.button!==0||activeScreen!=='game'||dialogPaused||!$('#ending').hidden)return;
 cancelHold();suppressHoldClick=false;holdPointer=e.pointerId;
 tapSurface.setPointerCapture?.(e.pointerId);
 holdTimer=setTimeout(()=>{
  holdTimer=null;
  if(holdPointer!==e.pointerId||activeScreen!=='game'||dialogPaused)return;
  const pointer=holdPointer;stopModes();holdPointer=pointer;holdSkipping=true;suppressHoldClick=true;
  $('#stage').classList.remove('ui-hidden');window.storySfx?.stop();skipLimit=Infinity;skipping=true;
  $('#skip').setAttribute('aria-pressed','true');startSkipTimer();
 },450);
};
tapSurface.onpointerup=endHold;tapSurface.onpointercancel=endHold;tapSurface.onlostpointercapture=endHold;
tapSurface.oncontextmenu=e=>e.preventDefault();
window.addEventListener('blur',()=>{if(holdSkipping)stopModes();else cancelHold();});
$('#start').onclick=()=>screen('chapters');$('#continue').onclick=()=>chooseEpisode(disk.episodeId||'prologue',true);$('#chapter-one').onclick=()=>{activeCollection='main';renderEpisodeCards();screen('episodes')};$('#chapter-two').onclick=()=>{activeCollection='chapter2';renderEpisodeCards();screen('episodes')};$('#extra-stories').onclick=()=>{activeCollection='extras';renderEpisodeCards();screen('episodes')};$('#back-chapters').onclick=()=>screen('chapters');$$('[data-home]').forEach(b=>b.onclick=()=>screen('title'));
$('#game-back').onclick=()=>screen('episodes');$('#end-episodes').onclick=()=>screen('episodes');$('#replay').onclick=()=>begin(0);$('#tap-surface').onclick=()=>{if(suppressHoldClick){suppressHoldClick=false;return;}if(transitioning)return;if($('#stage').classList.contains('ui-hidden')){$('#stage').classList.remove('ui-hidden');return;}if(!$('#cutin').hidden){cutinDone();return;}next();};$('#previous').onclick=previous;$('#auto').onclick=toggleAuto;$('#skip').onclick=toggleSkip;$('#hide-ui').onclick=()=>$('#stage').classList.add('ui-hidden');$('#restore-ui').onclick=()=>$('#stage').classList.remove('ui-hidden');
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
document.addEventListener('click',e=>{if(e.target.closest?.('.title-actions button,#chapter-one,#chapter-two,#extra-stories,.episode-card,[data-home],#back-chapters,#game-back,#end-episodes,#next-episode,.settings-open,#log-open,#log-close,#resume-yes,#resume-no,#resume-cancel,.close-settings'))window.storySfx?.play('ui',config);});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopModes();persist();}});window.addEventListener('pagehide',persist);
updateSettingsLabels();window.storyBgm?.set('daily',config);$('#continue').disabled=true;
fetch('data/episodes.json?v=chapter2-v1').then(r=>{if(!r.ok)throw Error('manifest');return r.json();}).then(async data=>{manifest=data.episodes;renderEpisodeCards();await loadEpisode(manifest.some(e=>e.id===disk.episodeId)?disk.episodeId:'prologue');for(const src of ['assets/bg/campus.webp','assets/characters/plus-smile.webp','assets/characters/yuji-neutral.webp'])preload(src);}).catch(()=>error('物語データを読み込めませんでした。ページを再読み込みしてください。'));
