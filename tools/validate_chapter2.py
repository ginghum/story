"""Check exact prose coverage, all local assets, CG anchors and chapter navigation metadata."""
import json,hashlib,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'data/episodes.json').read_text())['episodes'];tracks={t['id'] for t in json.loads((R/'data/bgm-tracks.json').read_text())['tracks']};total=0;images=set();cg=set()
for n in range(1,25):
 id=f'chapter2-episode{n}';d=json.loads((R/f'data/{id}.json').read_text());body=(R/f'data/source/{id}.txt').read_text();assert hashlib.sha256(body.encode()).hexdigest()==d['source_hash']
 expected=[l.strip() for l in body.splitlines() if l.strip() and l.strip()!='＊'];actual=[e['raw'] for e in d['entries'] if e.get('raw')];assert actual==expected,(id,'prose mismatch')
 assert len(expected)==d['source_lines'];assert d['source_scenes']==len(body.split('　　　　　＊'))
 for e in d['entries']:
  assert e['bgm'] in tracks,(id,'BGM',e['bgm']);assert not re.search(r'^[a-z]+[-_]',e['location']),(id,e['location'])
  assert len(e['cast'])<=3;assert len({c['id'] for c in e['cast']})==len(e['cast'])
  images.add(e['bg']);
  if e.get('cg'):cg.add(e['cg'])
  for c in e['cast']:images.add(f"assets/characters/{c['id']}-{c['expression']}.webp")
  if e.get('se'):assert (R/f"assets/se/{e['se']}.wav").exists()
  if e['type']=='line':assert len(e['text'])<=110,(id,len(e['text']))
 total+=len(d['entries']);assert sum(x['id']==id for x in manifest)==1
for path in images:
 p=R/path;assert p.exists(),path
 with Image.open(p) as im:
  im.verify()
 if '/characters/' in path:
  with Image.open(p) as im:assert im.mode=='RGBA' and im.getextrema()[-1][0]==0,path
assert len(cg)==102,(len(cg),'illustration was lost')
print(f'PASS: all 24 episodes, {total} entries, exact prose coverage, {len(cg)} CG anchors, {len(images)} decoded local assets, BGM/SE and Japanese locations.')
