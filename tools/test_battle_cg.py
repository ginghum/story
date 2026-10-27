"""Regression checks for battle-only staging, spoiler boundaries and legacy saves."""
import collections,hashlib,json,subprocess
from pathlib import Path
from PIL import Image
from stage_battle_cg import main
R=Path(__file__).resolve().parents[1]
plan=json.loads((R/'data/battle-cg-plan.json').read_text())['scenes'];allowed=collections.defaultdict(set)
for p in plan:
 d=json.loads((R/'data'/f"{p['episode']}.json").read_text());indices=[i for i,e in enumerate(d['entries']) if e['type']=='line' and e['scene']==p['scene']]
 def at(raw):return next(j for j,i in enumerate(indices) if d['entries'][i].get('raw')==raw)
 lo=at(p['start']) if p.get('start') else 0;hi=at(p['end']) if p.get('end') else len(indices)
 allowed[p['episode']].update(indices[lo:hi])
used=collections.Counter();changed=0;hashes={}
for m in json.loads((R/'data/episodes.json').read_text())['episodes']:
 path=m['file'];d=json.loads((R/path).read_text());old=json.loads(subprocess.check_output(['git','show','HEAD:'+path],cwd=R));assert len(d['entries'])==len(old['entries'])
 for i,(a,b) in enumerate(zip(old['entries'],d['entries'])):
  assert {k:v for k,v in a.items() if k not in ['cg','cgAlt']}=={k:v for k,v in b.items() if k not in ['cg','cgAlt']},(path,i,'nonvisual change')
  if a!=b:assert i in allowed[m['id']],(path,i,'outside battle range');changed+=1
  if a.get('cg')=='assets/cg/episode20-final-fists.webp':assert b['cg']==a['cg']
  if b.get('cg','') and b['cg'].startswith('assets/cg/battle-'):used[b['cg']]+=1
 hashes[path]=hashlib.sha256((R/path).read_bytes()).hexdigest()
assets=sorted((R/'assets/cg').glob('battle-*.webp'));assert len(assets)==18,len(assets)
for p in assets:
 assert used[str(p.relative_to(R))]>0,p
 with Image.open(p) as im:im.load();assert im.width>=1280 and im.width>im.height and im.mode=='RGB'
# New choke/guard image only after the pin actually happens; no final-impact reveal ahead of source.
es=json.loads((R/'data/chapter2-episode21.json').read_text())['entries'];boundary=next(i for i,e in enumerate(es) if e.get('raw')=='首へ、細い指が掛かった。');assert not any(e.get('cg')=='assets/cg/battle-milk-ground-guard.webp' for e in es[:boundary])
main()
for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,(f,'not idempotent')
rep=json.loads((R/'data/battle-cg-report.json').read_text());assert rep['cg_lines']/rep['lines']>.85
print('PASS:',len(assets),'new battle CGs used;',changed,'visual entries updated; all 51 episode prose/cast/audio/save offsets unchanged, outside ranges unchanged, original final fists preserved, pin boundary and idempotence verified.')
