"""Validate prose coverage, scene references and actual image decoding for released episodes."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
manifest=json.load(open(ROOT/'data/episodes.json'))['episodes']
assets=set();summary=[]
for meta in manifest:
 story=json.load(open(ROOT/meta['file']));entries=story['entries'];assert story['id']==meta['id']
 if story['id']!='prologue':
  body=(ROOT/'data/source'/f"{story['id']}.txt").read_text();source=[s.strip() for s in body.splitlines() if s.strip() and s.strip()!='＊']
  assert [e['raw'] for e in entries if e.get('raw')]==source,(story['id'],'source coverage')
  assert hashlib.sha256(body.encode()).hexdigest()==story['source_hash']
  assert len(body.split('　　　　　＊'))==story['source_scenes']
  assert all(len(e.get('text',''))<=105 for e in entries)
  reconstructed=[];current=None;parts=[]
  for e in entries:
   if e['type']!='line':continue
   if e.get('raw'):
    if current:reconstructed.append((current,''.join(parts)))
    current=e['raw'];parts=[]
   parts.append(e.get('text',''))
  if current:reconstructed.append((current,''.join(parts)))
  for raw,text in reconstructed:
   assert text==raw or raw.endswith(text),(story['id'],raw,text)
 for e in entries:
  assert 1<=e['scene']<=story['source_scenes']
  assert len(e.get('cast',[]))<=3
  for key in ['bg','cg']:
   if e.get(key):assets.add(e[key])
  for c in e.get('cast',[]):assets.add(f"assets/characters/{c['id']}-{c['expression']}.webp")
 assets.add(meta['image'])
 summary.append(dict(id=story['id'],entries=len(entries),source_lines=story['source_lines'],scenes=story['source_scenes']))
for name in sorted(assets):
 path=ROOT/name;assert path.is_file() and path.stat().st_size>0,name
 with Image.open(path) as im:
  im.load();assert im.width>0 and im.height>0
  if name.startswith('assets/characters/'):
   assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,name
# Entrance, exit, costume and CG staging regressions found during review.
def episode(n):return json.load(open(ROOT/f'data/chapter1-episode{n}.json'))['entries']
e=episode(2);gone=next(i for i,x in enumerate(e) if x.get('raw','').startswith('裾を片手で押さえ、花壇の横を走り'))
assert all(x.get('cg')!='assets/cg/episode02-yuji.webp' and all(c['id']!='yuji' for c in x['cast']) for x in e[gone:] if x['scene']==3)
for n in [4,5]:
 assert all(c['expression'].startswith('bandaged') for x in episode(n) for c in x['cast'] if c['id']=='plus')
assert all(c['expression']=='battle' for x in episode(5) if 5<=x['scene']<=9 for c in x['cast'] if c['id']=='dai')
print(json.dumps({'episodes':summary,'decoded_assets':len(assets),'result':'PASS'},ensure_ascii=False))
