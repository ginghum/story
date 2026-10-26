"""Deterministic original synthesized effects; no third-party recordings."""
import wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'assets/se';out.mkdir(exist_ok=True)
rng=np.random.default_rng(521);rate=22050
for name,seconds in [('hit',.16),('heavy',.36),('whoosh',.28),('teleport',.38),('whip',.24),('rustle',.22),('chime',.65),('camera',.14),('door-open',.55),('door-close',.3),('knock',.48),('steps',.85),('run',.72),('chair',.4),('tableware',.3),('water',.85),('metal',.5),('bell',1.3),('crowd',1.1),('cloth',.35),('ui',.075)]:
 t=np.arange(int(rate*seconds))/rate;noise=rng.normal(0,1,len(t));env=np.minimum(t/.008,1)*(1-t/seconds)**2
 if name=='hit':y=(noise*.35+np.sin(2*np.pi*(100*t-90*t*t))*.6)*np.exp(-t*22)
 elif name=='heavy':y=(noise*.2+np.sin(2*np.pi*(85*t-65*t*t))*.7)*np.exp(-t*12)
 elif name in ['whoosh','whip']:y=np.diff(np.r_[0,noise])*.15*np.sin(np.pi*t/seconds)**3+(noise*.22*np.exp(-((t-seconds*.75)/.012)**2) if name=='whip' else 0)
 elif name=='teleport':y=(np.sin(2*np.pi*(420*t+1700*t*t))*.3+noise*.12)*np.sin(np.pi*t/seconds)**2
 elif name=='rustle':y=noise*.16*(.6+.4*np.sin(t*95))
 elif name=='chime':y=sum(np.sin(2*np.pi*f*t)*np.exp(-t*6) for f in [660,880,1320])*.18
 elif name=='camera':y=noise*.3*(np.exp(-t*70)+np.exp(-((t-.055)/.008)**2))
 elif name=='door-open':y=(np.sin(2*np.pi*(135*t+35*np.sin(t*9)))*.1+np.convolve(noise,np.ones(9)/9,'same')*.15)*np.sin(np.pi*t/seconds)
 elif name=='door-close':y=(np.sin(2*np.pi*95*t)*.45+noise*.13)*np.exp(-t*27)
 elif name in ['knock','steps','run']:
  y=np.zeros_like(t);times={'knock':[.03,.19],'steps':[.03,.32,.62],'run':[.03,.17,.31,.45,.59]}[name]
  for onset in times:
   u=np.maximum(t-onset,0);gate=(t>=onset);y+=(np.sin(2*np.pi*(155 if name=='knock' else 90)*u)*.3+noise*.12)*np.exp(-u*45)*gate
 elif name=='chair':y=(np.sin(2*np.pi*(180*t+55*t*t))*.075+np.convolve(noise,np.ones(7)/7,'same')*.23)*np.sin(np.pi*t/seconds)**2
 elif name in ['tableware','metal','bell']:
  freqs={'tableware':[1840,2630,3900],'metal':[430,710,1190,1900],'bell':[523.25,1046.5,1569.8,2630]}[name]
  y=sum(np.sin(2*np.pi*f*t)*np.exp(-t*(5+i*2)) for i,f in enumerate(freqs))*(.065 if name=='tableware' else .09)
 elif name=='water':y=np.convolve(noise,np.ones(5)/5,'same')*.2*(.65+.35*np.sin(t*36))+np.sin(2*np.pi*(1100*t+50*np.sin(t*14)))*.02
 elif name=='crowd':
  y=np.zeros_like(t)
  for onset in np.arange(.02,seconds-.05,.047):
   u=np.maximum(t-onset,0);y+=noise*.1*np.exp(-u*80)*(t>=onset)
 elif name=='cloth':y=np.convolve(noise,np.ones(5)/5,'same')*.22*np.sin(np.pi*t/seconds)**2
 elif name=='ui':y=np.sin(2*np.pi*960*t)*.12*np.exp(-t*45)
 else:raise ValueError(name)
 y*=env;y=np.clip(y,-.9,.9);p=out/(name+'.wav')
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((y*32767).astype('<i2').tobytes())
 print(name,len(y),round(float(np.max(np.abs(y))),3))
