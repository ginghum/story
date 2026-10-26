"""Verify source continuity, injury priority and period-specific expression staging."""
import copy,json,subprocess
from pathlib import Path
from assign_expressions import apply
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/expression-assets.json').read_text())['assets']
used=set();changed=0
for meta in json.loads((ROOT/'data/episodes.json').read_text())['episodes']:
 p=meta['file'];data=json.loads((ROOT/p).read_text())
 old=json.loads(subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT))
 assert len(old['entries'])==len(data['entries'])
 assert apply(copy.deepcopy(data))==data,('not idempotent',p)
 for before,after in zip(old['entries'],data['entries']):
  ignored={'cast','cg'}|({'character'} if data['id']=='extra4' and after.get('speaker')=='ドーマ' else set())
  assert {k:v for k,v in before.items() if k not in ignored}=={k:v for k,v in after.items() if k not in ignored},(p,after.get('raw'))
  changed+=before!=after
  for c in after['cast']:used.add(c['id']+'-'+c['expression'])
  for c in before['cast']:
   if c['expression'] in ['hurt','pain','battle-hurt','shaken'] or c['expression'].startswith('bandaged'):
    same=next((a for a in after['cast'] if a['id']==c['id']),None)
    assert same and (same['expression']==c['expression'] or c['expression'].startswith('bandaged') and same['expression'].startswith('bandaged'))
  if data['id']=='chapter1-episode20' and after['scene']==11:assert before.get('cg')==after.get('cg')
 if data['id']=='extra4':
  for e in data['entries']:
   if e['scene']<13:assert all(c['id']!='doma' for c in e['cast'])
  s=[e for e in data['entries'] if e['scene']==13 and e['type']=='line']
  glasses=False
  for e in s:
   if e['raw'].startswith('ドーマは、よく分からない顔をしたまま掛けた。'):glasses=True
   if e['raw'].startswith('夜が深くなり、ドーマが眼鏡を外した。'):glasses=False
   if e['raw'].startswith('眼鏡を掛け直した。'):glasses=True
   assert any(c['id']==('doma' if glasses else 'doma-past') for c in e['cast'])
 if data['id']=='extra5':
  invisible=False
  for e in data['entries']:
   if e['scene']==15 and e.get('raw','').startswith('分かっていて、姿を消した。'):invisible=True
   if e['scene']==15 and invisible:assert not e['cast']
   ids=[c['id'] for c in e['cast']];assert len(ids)==len(set(ids))
assert all(x['id'] in used for x in catalog),used
print(f'Expressions: {len(catalog)} assets used; {changed} staged entries; prose/audio/save offsets and finale CG preserved; glasses and invisibility verified.')
