/* Original instrumental BGM. Gesture-gated, two-buffer cache, one crossfade pair. */
(()=>{
 'use strict';
 const titles={daily:'いつもの学園',calm:'頁をひらいて',training:'一歩ずつ、その先へ',battle:'届くまで',tension:'扉の向こう',reflection:'残った言葉'};
 const buffers=new Map(),voices=new Set();let context,master,current=null,wanted=null,override=null,settings={bgmEnabled:true,bgmVolume:.35},paused=false,version=0,pending=null,controller=null,saved=null;
 const effective=()=>override||wanted;
 const enabled=()=>settings.bgmEnabled!==false&&Number(settings.bgmVolume)>0;
 function level(){return Math.max(0,Math.min(1,Number(settings.bgmVolume)||0))*.65;}
 function stopAll(){for(const v of voices){try{v.source.stop();}catch{}v.source.disconnect?.();v.gain.disconnect?.();}voices.clear();current=null;}
 function invalidate(){version++;controller?.abort();controller=null;pending=null;}
 function pause(){if(current&&context)saved={name:current.name,offset:(current.offset+context.currentTime-current.started)%current.buffer.duration};paused=true;invalidate();stopAll();}
 function volume(config){const was=enabled();settings={...config};if(master){master.gain.cancelScheduledValues(context.currentTime);master.gain.setValueAtTime(enabled()?level():0,context.currentTime);}if(!enabled()){if(current)saved={name:current.name,offset:(current.offset+context.currentTime-current.started)%current.buffer.duration};invalidate();stopAll();}else if(!was)ensure();}
 async function unlock(){const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return false;try{if(!context){context=new AC();master=context.createGain();master.gain.value=level();master.connect(context.destination);}await context.resume();if(!document.hidden)paused=false;if(context.state!=='running')return false;ensure();return true;}catch{return false;}}
 function fadeOut(v,seconds=1.2){if(!v)return;const now=context.currentTime;v.gain.gain.cancelScheduledValues(now);v.gain.gain.setValueAtTime(v.gain.gain.value,now);v.gain.gain.linearRampToValueAtTime(0,now+seconds);try{v.source.stop(now+seconds);}catch{}}
 async function ensure(){
  const name=effective();if(paused||document.hidden||!enabled()||!context||context.state!=='running')return false;
  if(!name){invalidate();const old=current;current=null;saved=null;fadeOut(old);return false;}
  if(current?.name===name)return true;if(pending?.name===name)return pending.promise;
  invalidate();const ticket=version;controller=new AbortController();const signal=controller.signal;
  const promise=(async()=>{try{
   let buffer=buffers.get(name);
   if(!buffer){const response=await fetch('assets/bgm/'+name+'.mp3',{signal});if(!response.ok)throw Error('BGM');buffer=await context.decodeAudioData(await response.arrayBuffer());}
   if(ticket!==version||effective()!==name||paused||document.hidden||!enabled())return false;
   buffers.delete(name);buffers.set(name,buffer);while(buffers.size>2)buffers.delete(buffers.keys().next().value);
   // Retire an older fade before starting another, even under rapid skip/back navigation.
   for(const voice of voices)if(voice!==current){try{voice.source.stop();}catch{}voices.delete(voice);voice.source.disconnect?.();voice.gain.disconnect?.();}
   const source=context.createBufferSource(),gain=context.createGain(),now=context.currentTime;source.buffer=buffer;source.loop=true;source.connect(gain);gain.connect(master);gain.gain.setValueAtTime(0,now);gain.gain.linearRampToValueAtTime(1,now+1.2);
   const offset=saved?.name===name?saved.offset:0;saved=null;const voice={name,source,gain,buffer,offset,started:now};const old=current;current=voice;voices.add(voice);source.onended=()=>{voices.delete(voice);source.disconnect?.();gain.disconnect?.();};source.start(0,offset);fadeOut(old);return true;
  }catch{if(ticket===version){const old=current;current=null;fadeOut(old);}return false;}finally{if(ticket===version){pending=null;controller=null;}}})();pending={name,promise};return promise;
 }
 function set(name,config){volume(config);name=titles[name]?name:null;if(wanted!==name){wanted=name;saved=null;invalidate();}return ensure();}
 async function preview(name,config){volume(config);if(!titles[name]||!enabled())return false;override=name;invalidate();paused=false;if(!await unlock())return false;return ensure();}
 function cancelPreview(){if(!override)return;override=null;saved=null;invalidate();ensure();}
 function resume(){paused=false;return ensure();}
 function stop(){wanted=null;override=null;saved=null;invalidate();stopAll();}
 document.addEventListener('pointerdown',()=>{unlock();},{passive:true});document.addEventListener('keydown',()=>{unlock();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();else resume();});window.addEventListener('pagehide',pause);window.addEventListener('pageshow',()=>{if(!document.hidden)resume();});
 window.storyBgm={set,volume,preview,cancelPreview,pause,resume,stop,titles};
})();
