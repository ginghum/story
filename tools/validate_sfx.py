"""Validate complete coverage, cue targets and every published sound asset."""
import json,re,wave,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
names=re.search(r'const names=(\[.*?\]);',(ROOT/'sound.js').read_text()).group(1)
names=json.loads(names.replace("'",'"'));assert len(names)==len(set(names))==21
for name in names:
 with wave.open(str(ROOT/'assets/se'/f'{name}.wav')) as w:
  assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,22050),name
  samples=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
  assert .05<=len(samples)/22050<=1.5 and 100<max(map(abs,samples))<=29500,name
  assert abs(samples[0])<100 and abs(samples[-1])<100,(name,'edge clicks')
manifest=json.loads((ROOT/'data/episodes.json').read_text())['episodes'];review=json.loads((ROOT/'data/se-review.json').read_text())['episodes'];total=0
for ep in manifest:
 es=json.loads((ROOT/ep['file']).read_text())['entries'];actual=[(i,e['se']) for i,e in enumerate(es) if e.get('se')]
 assert actual and [(x['entry'],x['sound']) for x in review[ep['id']]]==actual,ep['id']
 for i,name in actual:assert name in names and es[i]['type']=='line',(ep['id'],i,name)
 total+=len(actual)
print(f'PASS: {len(manifest)} episodes, {total} SE cues; {len(names)} PCM WAVs, amplitudes and fade edges verified.')
