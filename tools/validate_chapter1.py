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
if any(m['id']=='chapter1-episode17' for m in manifest):
 e15,e16,e17=[episode(n) for n in [15,16,17]]
 for es in [e15,e16,e17]:
  assert all(not c['expression'].startswith('bandaged') and not (c['id']=='lance' and c['expression']=='hurt') for x in es for c in x['cast'])
  assert all(not x['cast'] and not x.get('cg') for x in es if x['location'].startswith(('Xの記憶','夢／'))), 'Keep memories faceless and separate from current-time portraits'
 assert all(not x['cast'] for x in e15 if x.get('cg')=='assets/cg/episode15-d-v5.webp')
 leave=next(i for i,x in enumerate(e17) if x.get('raw','').startswith('四人で同じ道を歩く時間が終わり、'))
 assert all(c['id'] not in ['lance','yuji','konke'] for x in e17[leave:] for c in x['cast']), 'Plus visits the club alone'
 practice=next(i for i,x in enumerate(e17) if x.get('raw')=='プラスは、金属片を元の質量へ戻して置いた。')
 assert all(x.get('cg')!='assets/cg/episode17-morning-practice.webp' for x in e17[practice:])
 exit=next(i for i,x in enumerate(e17) if x.get('raw')=='扉へ向かう。')
 assert all(c['id']!='x' for x in e17[exit:] for c in x['cast'])
 assert all(x.get('bgm')!='battle' for x in e17 if x['scene']==6), 'The challenge is a negotiation; combat has not begun'
 assert any(c['id']=='x' and c['expression']=='shaken' for x in e16 for c in x['cast'])
 print('PASS: episode 15–17 healing, faceless memories, council viewpoint, solo club visit, practice prop exit, X exit and challenge staging.')

if any(m['id']=='chapter1-episode21' for m in manifest):
 e18,e19,e20,e21=[episode(n) for n in [18,19,20,21]]
 assert all(c['expression']!='battle-hurt' for e in e18 if e['scene']<8 or e['scene']>=10 for c in e['cast'])
 assert all(c['id']!='plus' for es,lo,hi in [(e19,7,10),(e20,1,4)] for e in es if lo<=e['scene']<=hi for c in e['cast'])
 invisible=next(i for i,e in enumerate(e20) if e.get('raw')=='ルサイは、姿を消した。')
 assert all(c['id']!='lusai' for e in e20[invisible:] if e['scene']==2 for c in e['cast'])
 impact=next(i for i,e in enumerate(e20) if e.get('raw')=='ぶつかった。')
 fallen=next(i for i,e in enumerate(e20) if e.get('raw')=='Xが、倒れた。')
 assert all((e.get('cg')=='assets/cg/episode20-final-fists.webp')==(impact<=i<fallen) for i,e in enumerate(e20))
 assert all(c['id']!='x' for e in e20[fallen:] for c in e['cast'])
 assert all(e['scene'] in [13,14] for e in e20 if e.get('cg')=='assets/cg/episode20-gurney-friends.webp')
 assert all(c['expression']!='battle-hurt' for e in e21 for c in e['cast'])
 assert all(c['id']!='x' and e.get('cg') not in ['assets/cg/episode21-a.webp','assets/cg/episode21-c.webp','assets/cg/episode21-handshake.webp'] for e in e21[507:] for c in e['cast'])
 assert all(not e['cast'] and e.get('cg')=='assets/cg/episode21-b.webp' for e in e21 if e['scene']==13)
 assert e21[-1]['raw']=='第一章　完'
 print('PASS: finale healing, past/current separation, invisibility, fist impact/exit, gurney attendance, dream and chapter ending.')

if any(m['id']=='chapter1-episode21' for m in manifest):
 e13,e18,e19=[episode(n) for n in [13,18,19]]
 metal=next(i for i,e in enumerate(e13) if e.get('raw')=='胸元を掴む前に、ランスの掌から小さな金属板が生まれた。')
 stop=next(i for i,e in enumerate(e13) if e.get('raw')=='プラスは、靴で土を削って止まった。')
 assert all((e.get('cg')=='assets/cg/episode13-hand-deflection-v4.webp')==(metal<=i<stop) for i,e in enumerate(e13))
 night=next(i for i,e in enumerate(e18) if e.get('raw')=='練習場の明かりがつく。')
 assert all(e.get('cg')!='assets/cg/episode18-training-clear-lane-v3.webp' for e in e18[night:])
 fall=next(i for i,e in enumerate(e19) if e.get('raw')=='床へ、背中が落ちた。')
 stand=next(i for i,e in enumerate(e19) if i>fall and e.get('raw')=='立った。')
 assert all(not e.get('cg') and not e['cast'] for e in e19[fall:stand])
 print('PASS: corrected metal-plate timing, nighttime CG, wrist-control landing and portrait restoration.')
