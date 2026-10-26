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
# Episode 6: hospital scenes must not show an upright, healthy Yuji sprite;
# flashbacks must not inherit the injured Plus or current-time Lance.
if any(m['id']=='chapter1-episode6' for m in manifest):
 e=episode(6)
 assert all(c['id']!='yuji' for x in e if x['scene'] in [1,2,3,6,7,8,9,10,11,12] for c in x['cast'])
 assert all(c['id']!='plus' for x in e if x['scene'] in [4,5] for c in x['cast'])
 assert all(c['id']!='lance' for x in e if x['scene']==4 for c in x['cast'])
 assert all(c['id']!='lance' for x in e if x['scene']==2 and x['type']=='line' and e.index(x)<next(i for i,y in enumerate(e) if y.get('raw')=='ランス「ユージは」') for c in x['cast'])
 assert all(c['expression'].startswith('bandaged') for x in e for c in x['cast'] if c['id']=='plus')
 assert all(not x.get('cg') for x in e if x['scene'] in [10,11,12]), 'Do not carry the stick CG into rest or unarmed training'
 print('PASS: episode 6 bed continuity, flashback isolation, Lance entrance, protected right arm and practice-stick exit.')
# Later episodes cross a treatment boundary, change locations mid-paragraph,
# and revisit the same characters in flashbacks.
if any(m['id']=='chapter1-episode10' for m in manifest):
 e7,e8,e9,e10=[episode(n) for n in [7,8,9,10]]
 assert all(c['expression'].startswith('bandaged') for x in e7 for c in x['cast'] if c['id']=='plus')
 assert all(not c['expression'].startswith('bandaged') for seq in [e8,e9,e10] for x in seq for c in x['cast'] if c['id']=='plus')
 assert all(c['id']!='yuji' for x in e8 if 5<=x['scene']<=8 for c in x['cast']), 'Yuji is away at his own club during the interview'
 assert all(c['id']!='plus' for x in e9 if 1<=x['scene']<=4 or x['scene']==6 for c in x['cast']), 'Current Plus must not leak into Konke flashbacks'
 assert all(not x.get('cg') or x['cg']!='assets/cg/episode09-b-faceless.webp' for x in e9 if x['scene']>=11), 'Do not carry corridor combat into the office'
 assert all(c['id']=='plus' for x in e10 if x['scene']==7 and x.get('raw','').startswith('返事はなかった。') for c in x['cast']), 'Konke is down after the finish'
 assert any(x.get('cg')=='assets/cg/episode10-konke-mirror.webp' for x in e10 if x['scene']==6)
 assert all(not x.get('cg') or x['cg']!='assets/cg/episode10-tree-faceless.webp' for x in e10 if x['scene']!=13), 'Do not reveal Minus before the final scene'
 print('PASS: episode 7–10 healing boundary, interview attendance, flashbacks, combat exits, mirror CG and final cameo timing.')
if any(m['id']=='chapter1-episode14' for m in manifest):
 e12,e13,e14=[episode(n) for n in [12,13,14]]
 assert all(c['expression']=='hurt' for x in e13 for c in x['cast'] if c['id']=='lance')
 assert all(c['expression']=='hurt' for x in e14 if x['scene']==1 for c in x['cast'] if c['id']=='lance')
 assert all(c['expression']!='hurt' for x in e14 if x['scene']>=5 for c in x['cast'] if c['id']=='lance')
 assert all(not c['expression'].startswith('bandaged') for es in [e12,e13,e14] for x in es for c in x['cast'] if c['id']=='plus')
 trap=next(i for i,x in enumerate(e12) if x.get('raw')=='コバルの足元で、銀色が跳ねた。')
 assert e12[trap]['cg']=='assets/cg/episode12-folded-spear.webp'
 assert all(x.get('cg')!='assets/cg/episode12-folded-spear.webp' for x in e12[:trap])
 release=next(i for i,x in enumerate(e14) if x.get('raw')=='プラスは、すぐに手を離した。')
 assert all(x.get('cg')!='assets/cg/episode14-ground-control-r2.webp' for x in e14[release:])
 assert all('night' in x['bg'] for x in e14 if 6<=x['scene']<=10)
 assert all(x.get('cg')!='assets/cg/episode13-a.webp' for x in e13), 'Do not use the original incorrect sling CG'
 print('PASS: episode 12–14 injury/treatment boundary, trap reveal, pin release and nighttime staging.')
