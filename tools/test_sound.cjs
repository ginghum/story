const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
 let started=0,stopped=0,decode=0,gain;const handlers={};
 const context={state:'running',destination:{},resume:async()=>{},createGain:()=>gain={gain:{value:0},connect(){}},decodeAudioData:async()=>{decode++;return {};},createBufferSource:()=>({connect(){},start(){started++;},stop(){stopped++;}})};
 const document={hidden:false,addEventListener(k,fn){handlers[k]=fn;}};
 const window={AudioContext:function(){return context;},addEventListener(){}};
 const sandbox={window,document,Map,Set,fetch:async()=>({ok:true,arrayBuffer:async()=>new ArrayBuffer(1)})};vm.runInNewContext(fs.readFileSync('sound.js','utf8'),sandbox);
 const api=window.storySfx,config={seEnabled:true,seVolume:.5};
 assert.equal(api.play('hit',config),false,'no playback before user gesture');
 assert.equal(await api.preview('hit',config),true);assert.equal(decode,21);assert.equal(gain.gain.value,.325);
 for(let i=0;i<8;i++)api.play('heavy',config);assert.equal(started,9);assert.equal(stopped,5,'four voice cap');
 api.volume({...config,seEnabled:false});assert.equal(stopped,9);assert.equal(gain.gain.value,0);
 assert.equal(api.play('hit',{...config,seEnabled:false}),false);assert.equal(api.play('hit',{...config,seVolume:0}),false);
 document.hidden=true;assert.equal(api.play('hit',config),false);handlers.visibilitychange();
 console.log('PASS: gesture gate, 21 cached buffers, volume, mute, four-voice cap, hidden-page suppression.');
})();
