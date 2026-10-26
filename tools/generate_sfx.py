"""Deterministic original synthesized effects; no third-party recordings."""
import wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'assets/se';out.mkdir(exist_ok=True)
rng=np.random.default_rng(521);rate=22050
for name,seconds in [('hit',.16),('heavy',.36),('whoosh',.28),('teleport',.38),('whip',.24),('rustle',.22),('chime',.65),('camera',.14)]:
 t=np.arange(int(rate*seconds))/rate;noise=rng.normal(0,1,len(t));env=np.minimum(t/.008,1)*(1-t/seconds)**2
 if name=='hit':y=(noise*.35+np.sin(2*np.pi*(100*t-90*t*t))*.6)*np.exp(-t*22)
 elif name=='heavy':y=(noise*.2+np.sin(2*np.pi*(85*t-65*t*t))*.7)*np.exp(-t*12)
 elif name in ['whoosh','whip']:y=np.diff(np.r_[0,noise])*.15*np.sin(np.pi*t/seconds)**3+(noise*.22*np.exp(-((t-seconds*.75)/.012)**2) if name=='whip' else 0)
 elif name=='teleport':y=(np.sin(2*np.pi*(420*t+1700*t*t))*.3+noise*.12)*np.sin(np.pi*t/seconds)**2
 elif name=='rustle':y=noise*.16*(.6+.4*np.sin(t*95))
 elif name=='chime':y=sum(np.sin(2*np.pi*f*t)*np.exp(-t*6) for f in [660,880,1320])*.18
 else:y=noise*.3*(np.exp(-t*70)+np.exp(-((t-.055)/.008)**2))
 y*=env;y=np.clip(y,-.9,.9);p=out/(name+'.wav')
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((y*32767).astype('<i2').tobytes())
 print(name,len(y),round(float(np.max(np.abs(y))),3))
