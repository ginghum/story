/* Original sound effects. Audio is unlocked only by a user gesture. */
(()=>{
 'use strict';
 const names=['hit','heavy','whoosh','teleport','whip','rustle','chime','camera','door-open','door-close','knock','steps','run','chair','tableware','water','metal','bell','crowd','cloth','ui'];
 let context,master,ready=false,loading,serial=0;
 const buffers=new Map(),voices=new Set();
 function stop(){serial++;for(const voice of voices){try{voice.stop();}catch{}}voices.clear();}
 function volume(config){if(master)master.gain.value=config.seEnabled===false?0:Math.max(0,Math.min(1,Number(config.seVolume)||0))*.65;if(config.seEnabled===false)stop();}
 async function unlock(){
  const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return false;
  try{if(!context){context=new AC();master=context.createGain();master.gain.value=.35;master.connect(context.destination);}await context.resume();ready=context.state==='running';
   if(!loading)loading=Promise.all(names.map(async name=>{try{const r=await fetch('assets/se/'+name+'.wav');if(!r.ok)return;const b=await context.decodeAudioData(await r.arrayBuffer());buffers.set(name,b);}catch{}}));
   return ready;
  }catch{return false;}
 }
 function play(name,config){
  if(!ready||document.hidden||config.seEnabled===false||Number(config.seVolume)<=0||!buffers.has(name))return false;
  volume(config);while(voices.size>=4){const first=voices.values().next().value;try{first.stop();}catch{}voices.delete(first);}
  const source=context.createBufferSource();source.buffer=buffers.get(name);source.connect(master);voices.add(source);source.onended=()=>voices.delete(source);source.start();return true;
 }
 async function preview(name,config){const ticket=serial;if(!await unlock())return false;await loading;if(ticket!==serial)return false;return play(name,config);}
 document.addEventListener('pointerdown',()=>{unlock();},{passive:true});document.addEventListener('keydown',()=>{unlock();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);
 window.storySfx={play,preview,stop,volume};
})();
