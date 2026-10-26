const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
 const listeners={},sources=[],gains=[],fetched=[];let gate=null;
 const context={currentTime:0,state:'running',destination:{},resume:async()=>{},createGain(){const param={value:1,ramps:[],cancelScheduledValues(){},setValueAtTime(v,t){this.value=v},linearRampToValueAtTime(v,t){this.ramps.push([v,t]);this.value=v}};const gain={gain:param,connect(){},disconnect(){}};gains.push(gain);return gain},decodeAudioData:async x=>({duration:40,id:x.id}),createBufferSource(){const source={starts:[],stops:[],connect(){},disconnect(){},start(...args){this.starts.push(args)},stop(when=0){this.stops.push(when);if(when<=context.currentTime)this.onended?.()}};sources.push(source);return source}};
 const document={hidden:false,addEventListener(k,fn){listeners[k]=fn}};const window={AudioContext:function(){return context},addEventListener(){}};
 const fetch=async(url,{signal}={})=>{fetched.push(url);if(gate&&url.includes('battle'))await new Promise((resolve,reject)=>{gate.release=resolve;signal.addEventListener('abort',()=>reject(Error('aborted')))});return {ok:true,arrayBuffer:async()=>({id:url})}};
 vm.runInNewContext(fs.readFileSync('music.js','utf8'),{window,document,fetch,Map,Set,AbortController});const api=window.storyBgm,cfg={bgmEnabled:true,bgmVolume:.35};
 assert.equal(await api.set('daily',cfg),false);assert.equal(fetched.length,0,'no audio fetching before gesture');assert.equal(await api.preview('daily',cfg),true);api.cancelPreview();assert.equal(sources.length,1);assert.equal(sources[0].loop,true);assert.equal(gains[0].gain.value,.35*.65);
 for(let i=0;i<40;i++)await api.set('daily',cfg);assert.equal(sources.length,1,'same music continues through text');
 await api.set('battle',cfg);assert.equal(sources.length,2);assert(sources[0].stops.includes(1.2));assert(gains[2].gain.ramps.some(([v,t])=>v===1&&t===1.2),'crossfade-in');
 await api.set('tension',cfg);await api.set('daily',cfg);assert.equal(fetched.filter(x=>x.includes('daily')).length,2,'cache is limited to two tracks');
 context.currentTime=9;document.hidden=true;listeners.visibilitychange();document.hidden=false;assert.equal(await api.resume(),true);assert.equal(sources.at(-1).starts[0][1],9,'resume preserves loop position');
 api.volume({...cfg,bgmEnabled:false});assert.equal(gains[0].gain.value,0);const count=sources.length;await api.set('reflection',{...cfg,bgmEnabled:false});assert.equal(sources.length,count,'mute blocks playback');await api.set('reflection',cfg);assert.equal(sources.at(-1).buffer.id,'assets/bgm/reflection.mp3');
 await api.set(null,cfg);assert(sources.at(-1).stops.includes(context.currentTime+1.2),'intentional silence fades out');
 gate={};const stale=api.set('battle',cfg);await api.set('calm',cfg);assert.equal(await stale,false);assert.equal(sources.at(-1).buffer.id,'assets/bgm/calm.mp3','cancelled fetch never starts wrong scene');gate=null;
 assert.equal(await api.preview('training',cfg),true);api.cancelPreview();await api.set('calm',cfg);assert.equal(sources.at(-1).buffer.id,'assets/bgm/calm.mp3','preview returns to assigned scene');api.stop();
 console.log('PASS: gesture gate, continuous loops, crossfade, two-track cache, hidden-tab pause/resume, mute, silence, stale-load cancellation and preview restoration.');
})().catch(e=>{console.error(e);process.exitCode=1});
