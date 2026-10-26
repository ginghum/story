"""Check scene assignments and decode original music files."""
import json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];tracks=json.loads((ROOT/'data/bgm-tracks.json').read_text())['tracks'];names={t['id'] for t in tracks};assert len(names)==6
for track in tracks:
 data=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(ROOT/track['file']),'-f','f32le','-ac','2','-ar','22050','-']);samples=np.frombuffer(data,dtype='<f4').reshape(-1,2)
 assert abs(len(samples)/22050-track['duration'])<.1 and np.isfinite(samples).all(),track['id']
 assert .05<float(np.sqrt(np.mean(samples**2)))<.15 and float(np.max(np.abs(samples)))<1,track['id']
manifest=json.loads((ROOT/'data/episodes.json').read_text())['episodes'];review=json.loads((ROOT/'data/bgm-scenes.json').read_text())['episodes'];scene_count=0
for ep in manifest:
 d=json.loads((ROOT/ep['file']).read_text());scene_count+=d['source_scenes'];transitions=[]
 for i,e in enumerate(d['entries']):
  assert 'bgm' in e and (e['bgm'] is None or e['bgm'] in names),(ep['id'],i)
  if i==0 or e['bgm']!=d['entries'][i-1]['bgm']:transitions.append(dict(entry=i,scene=e['scene'],location=e['location'],track=e['bgm']))
 assert transitions==review[ep['id']]['transitions'],ep['id']
assert json.loads((ROOT/'data/chapter1-episode3.json').read_text())['entries'][435]['bgm'] is None
assert json.loads((ROOT/'data/chapter1-episode11.json').read_text())['entries'][-1]['bgm'] is None
print(f'PASS: 6 original MP3 loops decoded; all {len(manifest)} episodes / {scene_count} scenes assigned, including intentional silence.')
