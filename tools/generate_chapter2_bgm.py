"""Original chapter-two loops, additive synthesis; no sampled or third-party recordings."""
import numpy as np,json,wave,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];RATE=22050
SPECS={
 'underground':('石の下の静寂',68,[45,46,44,45,41,43,46,45],'ambient'),
 'forest-battle':('木陰を駆ける',144,[50,46,53,48,50,55,46,45],'drive'),
 'festival':('帝国創立記念日',108,[60,55,57,53,60,57,50,55],'festive'),
 'finale':('幸運の檻を越えて',138,[52,48,55,50,52,57,48,47],'drive'),
 'homecoming':('晴れた明日も',88,[60,57,53,55,52,57,50,55],'gentle')}
tracks=json.loads((R/'data/bgm-tracks.json').read_text())['tracks']
for name,(title,bpm,roots,kind) in SPECS.items():
 beat=60/bpm;duration=32*beat;N=round(duration*RATE);out=np.zeros((N+RATE*3,2));rng=np.random.default_rng(sum(map(ord,name)))
 def note(midi,start,length,amp,timbre='bell',pan=0):
  t=np.arange(round((length+1.4)*RATE))/RATE;f=440*2**((midi-69)/12)
  if timbre=='pad':
   sig=(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*1.002*t)+.12*np.sin(2*np.pi*f*2*t));env=np.minimum(t/.25,1)*np.minimum(np.maximum((length+1.4-t)/1.4,0),1)
  else:
   sig=np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*2*t)*np.exp(-t*4)+.05*np.sin(2*np.pi*f*4*t)*np.exp(-t*8);env=(1-np.exp(-t*180))*np.exp(-t*(2 if timbre=='bass' else 3.5))*np.minimum(np.maximum((length+1.4-t)/.5,0),1)
  at=round(start*RATE);end=min(len(out),at+len(t));v=sig[:end-at]*env[:end-at]*amp;out[at:end,0]+=v*np.sqrt((1-pan)/2);out[at:end,1]+=v*np.sqrt((1+pan)/2)
 for bar,root in enumerate(roots):
  start=bar*4*beat;minor=kind in ['ambient','drive'] or (kind=='gentle' and bar in [1,4,5,6]);chord=[root,root+(3 if minor else 4),root+7]
  for k,m in enumerate(chord):note(m,start,4*beat,.04,'pad',(k-1)*.6)
  note(root-12,start,3*beat,.09,'bass',-.1)
  if kind!='ambient':
   for k in range(8):note(chord[[0,2,1,2][k%4]]+12,start+k*.5*beat,.45*beat,.045,'bell',.35)
   for k in range(2):
    melody=[7,4,2,0,4,7,9,7] if kind in ['gentle','festive'] else [0,7,10,7,3,5,7,2]
    note(root+12+melody[(bar*2+k)%8],start+(k*2+.15)*beat,1.7*beat,.08,'bell',-.3)
  else:note(root+19,start+2.5*beat,2*beat,.025,'bell',.4)
  if kind in ['drive','festive']:
   for k in range(4):
    t=np.arange(round(.18*RATE))/RATE;v=(np.sin(2*np.pi*(65*t-60*t*t))*.12 if k%2==0 else rng.normal(0,.025,len(t)))*np.exp(-t*35);at=round((start+k*beat)*RATE);out[at:at+len(t)]+=v[:,None]
 out[:len(out)-N]+=out[N:];out=out[:N];out*=.07/max(np.sqrt(np.mean(out*out)),.001);out=np.tanh(out);wav=R/f'assets/bgm/{name}.wav';mp3=wav.with_suffix('.mp3')
 with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((out*32767).astype('<i2').tobytes())
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-codec:a','libmp3lame','-b:a','96k',str(mp3)],check=True);wav.unlink()
 decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(mp3),'-f','f32le','-ac','2','-ar',str(RATE),'-']),dtype='<f4');assert np.isfinite(decoded).all() and np.sqrt(np.mean(decoded*decoded))>.01
 tracks=[t for t in tracks if t['id']!=name];tracks.append(dict(id=name,title=title,bpm=bpm,duration=duration,file=f'assets/bgm/{name}.mp3',peak=round(float(abs(out).max()),4),composition='Original composition and additive synthesis by tools/generate_chapter2_bgm.py; no third-party recordings.'));print(name,round(duration,2),mp3.stat().st_size)
(R/'data/bgm-tracks.json').write_text(json.dumps(dict(tracks=tracks),ensure_ascii=False,indent=2)+'\n')
