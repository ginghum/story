"""Stage entrances and anonymous roles without changing prose or save indices."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'data/prologue.json';data=json.loads(p.read_text());es=data['entries']
def find(raw):
 hits=[i for i,e in enumerate(es) if e.get('raw')==raw];assert len(hits)==1,(raw,hits);return hits[0]
entrance=find('ランス「おせえよ」')
for e in es[:entrance]:
 if e['scene']==7:e['cast']=[c for c in e.get('cast',[]) if c['id']!='lance']
# The establishing cutin shows the destination before the conversation sprites appear.
for e in es:
 if e['type']=='location' and e['location']=='学生寮そば／能力練習場':
  e['bg']='assets/bg/training.webp';e['cg']=None;e['cast']=[]
def mob(id,name,height):return {'id':id,'name':name,'height':height,'expression':'brown','anonymous':True}
bully=mob('mob-male-broad','不良',182);victim=mob('mob-male-slim','生徒',166)
start=find('その横に、ひとりの生徒が尻をついている。床には汁物が広がり、白いパンが一切れ浮かんでいた。立っている数人のうち、先頭の男が、座り込んだ生徒の前へ片足を出す。')
leave=find('男たちは、呼ばれた係の生徒へ何か話すと、その場を離れていく。さっき床にいた生徒も、拾った鞄を抱えて壁際へ下がっていた。プラスがそちらへ目をやると、相手は一瞬だけ頭を下げた。')
for i in range(start,leave):
 e=es[i];cast=e.get('cast',[]);by_id={c['id']:c for c in cast}
 if 'x' in by_id:
  e['cast']=[c for c in cast if c['id'] in ['plus','x']]+[bully]
 else:
  focus=by_id.get('yuji') if e.get('speaker')=='ユージ' else by_id.get('plus')
  e['cast']=([focus] if focus else [])+[bully,victim]
 if e.get('speaker')=='不良':e['character']=bully['id']
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Staged Lance entrance, training establishing view and cafeteria anonymous roles.')
