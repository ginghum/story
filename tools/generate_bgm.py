"""Six original instrumental loops, composed and synthesized without external recordings."""
import json,subprocess,wave,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/bgm';OUT.mkdir(exist_ok=True)
RATE=22050
SPECS={
 'daily':('いつもの学園',96,[60,57,53,55,52,57,50,55],[0,2,4,7,9,7,4,2],False),
 'calm':('頁をひらいて',80,[53,60,50,57,58,53,55,60],[4,2,0,7,5,4,2,0],False),
 'training':('一歩ずつ、その先へ',112,[50,58,53,60,55,58,57,57],[0,3,7,10,7,5,3,2],True),
 'battle':('届くまで',132,[52,60,55,50,57,60,59,59],[0,7,10,7,3,5,7,2],True),
 'tension':('扉の向こう',88,[50,51,49,50,58,55,57,50],[0,1,7,3,0,8,7,1],True),
 'reflection':('残った言葉',72,[57,53,60,55,50,57,53,52],[7,4,2,0,4,7,5,2],True),
}
meta=[]
for name,(title,bpm,roots,melody,minor) in SPECS.items():
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 rng=np.random.default_rng(1700+sum(map(ord,name)));beat=60/bpm;duration=64*beat;N=round(duration*RATE);audio=np.zeros((N+RATE*3,2))
 def note(midi,start,length,amp,kind='keys',pan=0):
  count=round((length+(1.1 if kind=='pad' else .5))*RATE);t=np.arange(count)/RATE;freq=440*2**((midi-69)/12)
  if kind=='pad':
   env=np.minimum(t/.35,1)*np.minimum(np.maximum((length+1.1-t)/1.1,0),1);sig=sum(np.sin(2*np.pi*freq*(1+d)*t+p) for d,p in [(-.001,0),(.001,.6)])*.4+np.sin(2*np.pi*freq*2*t)*.08
  elif kind=='bass':env=(1-np.exp(-t*70))*np.exp(-t*2.5)*np.minimum(np.maximum((length+.5-t)/.4,0),1);sig=np.sin(2*np.pi*freq*t)+.16*np.sin(2*np.pi*freq*2*t)
  else:env=(1-np.exp(-t*220))*np.exp(-t*(2.7 if kind=='keys' else 5));sig=np.sin(2*np.pi*freq*t)+.28*np.sin(2*np.pi*freq*2*t)*np.exp(-t*4)+.1*np.sin(2*np.pi*freq*3*t)*np.exp(-t*7)
  sig*=env*amp;at=round(start*RATE);end=min(at+count,len(audio));sig=sig[:end-at];audio[at:end,0]+=sig*np.sqrt((1-pan)/2);audio[at:end,1]+=sig*np.sqrt((1+pan)/2)
 def drum(start,strong=False):
  t=np.arange(round(.2*RATE))/RATE;sig=(np.sin(2*np.pi*(75*t-70*t*t))*.26 if strong else rng.normal(0,.06,len(t)))*np.exp(-t*(25 if strong else 50));at=round(start*RATE);audio[at:at+len(t)]+=sig[:,None]
 for bar in range(16):
  root=roots[bar%8];minor_bars={'daily':[1,4,5,6],'calm':[2,3,6],'training':[0,4],'battle':[0,4],'tension':[0,3,5,7],'reflection':[0,4,5]}[name];third=3 if bar%8 in minor_bars else 4;chord=[root,root+third,root+7];start=bar*4*beat
  for k,m in enumerate(chord):note(m,start,4*beat,.055 if name!='tension' else .07,'pad',pan=(k-1)*.55)
  note(root-12,start,2.7*beat,.105,'bass',-.1)
  if name in ['daily','training','battle']:note(root-12,start+2*beat,1.6*beat,.07,'bass',-.1)
  steps=8 if name in ['daily','training','battle'] else 4
  for k in range(steps):note(chord[[0,1,2,1][k%4]]+12,start+k*4/steps*beat,beat*.9,.065 if name!='tension' else .035,'pluck',.3)
  if name!='tension':
   for k in range(2):note(root+12+melody[(bar*2+k)%8],start+(k*2+.25)*beat,beat*1.6,.095 if name!='reflection' else .085,'keys',-.25)
  else:note(root+19,start+beat*2.5,beat*1.8,.04,'keys',-.3)
  if name in ['training','battle']:
   for k in range(4):drum(start+k*beat,k%2==0)
 # Wrap release tails for a continuous loop, and match perceived level across cues.
 audio[:len(audio)-N]+=audio[N:];audio=audio[:N];rms=np.sqrt(np.mean(audio**2));audio*=.085/max(rms,.001);audio=np.tanh(audio);peak=float(np.max(np.abs(audio)))
 path=OUT/f'{name}.wav'
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((audio*32767).astype('<i2').tobytes())
 dest=OUT/f'{name}.mp3'
 for attempt in range(2):
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),'-codec:a','libmp3lame','-b:a','128k',str(dest)],check=True)
  decoded=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(dest),'-f','f32le','-ac','2','-ar',str(RATE),'-']);values=np.frombuffer(decoded,dtype='<f4')
  if abs(len(values)/2/RATE-duration)<.1 and np.isfinite(values).all():break
 else:raise ValueError('Music encoding validation failed: '+name)
 path.unlink()
 meta.append(dict(id=name,title=title,bpm=bpm,duration=duration,file=f'assets/bgm/{name}.mp3',peak=round(peak,4),composition='Original 16-bar composition and synthesis by tools/generate_bgm.py; no third-party recordings.'))
 print(name,round(duration,2),dest.stat().st_size)
if len(sys.argv)>1:
 prior=json.loads((ROOT/'data/bgm-tracks.json').read_text())['tracks'];meta=[next((new for new in meta if new['id']==old['id']),old) for old in prior]
(ROOT/'data/bgm-tracks.json').write_text(json.dumps(dict(tracks=meta),ensure_ascii=False,indent=2)+'\n')
