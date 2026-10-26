"""Attach reviewed SE to display chunks without changing story prose or staging."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def battle_sound(n,e):
 raw=e.get('raw','')
 if not raw:return
 if (e.get('effect')=='teleport' or re.search(r'^(ダイ[はが]、?消えた。|消えた。|届く前に、ダイが消えた。)$',raw)):e['se']='teleport'
 elif raw in ['鈍い音がした。','横腹へ蹴りが入った。','鞭が床を打つ。'] or re.search(r'拳[がを].*(当たった|当たる|入った)。',raw):e['se']='heavy' if '鈍い' in raw else 'whip' if '鞭' in raw else 'hit'
 elif raw in ['そこへ、反対の拳が短く入った。','背中の斜め後ろから、軽く肩を打たれた。','プラスは顔を引き、腕で受けた。']:e['se']='hit'
 elif raw in ['拳だけが、届かなかった場所を通った。','プラスの拳は、空いた場所を通った。']:e['se']='whoosh'
 elif re.search(r'(表紙が閉じた。|手帳を閉じた。)$',raw) and not e.get('speaker'):e['se']='rustle'
 elif raw.startswith(('サニー「始め','サニー「そこまで','サニー「止め')):e['se']='chime'
 elif raw in ['鞭が、そこへ来た。','もう一度、鞭が来た。','跳ばずに、小さく足を引いた。鞭が床を打つ。','鞭に腕の横を打たれ、痛みで考えが途切れる。','廊下では、ヒカルの鞭が壁を打った。']:e['se']='whip'
 elif raw in ['ユージが床へ落ちた。','重い音が、客席まで響いた。','廊下で、大きな音がした。']:e['se']='heavy'
 elif raw=='音がした。' and n in [5,7]:e['se']='whip' if n==5 else 'heavy'
 elif n==11 and raw=='もう一枚。今度は、こっちを向いて。':e['se']='camera'

def annotate():
 specs=json.loads((ROOT/'data/se-cues.json').read_text())['episodes'];report={}
 for id,cues in specs.items():
  path=ROOT/'data'/f'{id}.json';d=json.loads(path.read_text());entries=d['entries'];n=0 if id=='prologue' else int(id.split('episode')[-1])
  for e in entries:e.pop('se',None);battle_sound(n,e)
  groups=[]
  for i,e in enumerate(entries):
   if e.get('raw'):
    j=i+1
    while j<len(entries) and entries[j]['type']=='line' and not entries[j].get('raw'):j+=1
    groups.append((i,j,e['raw']))
  for cue in cues:
   matches=[g for g in groups if cue['match'] in g[2] and not entries[g[0]].get('speaker')]
   expected=cue.get('occurrences',1)
   assert len(matches)==expected,(id,cue,len(matches))
   assert (ROOT/'assets/se'/f"{cue['sound']}.wav").is_file(),cue
   for first,end,raw in matches:
    text=''.join(e['text'] for e in entries[first:end]);pos=text.find(cue['match']);assert pos>=0,(id,cue,'not in display text')
    offset=0
    for at in range(first,end):
     if offset+len(entries[at]['text'])>pos:
      assert not entries[at].get('se') or entries[at]['se']==cue['sound'],(id,cue,'conflicting SE')
      entries[at]['se']=cue['sound'];break
     offset+=len(entries[at]['text'])
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  report[id]=[dict(entry=i,scene=e['scene'],sound=e['se'],text=e['text']) for i,e in enumerate(entries) if e.get('se')]
 out=ROOT/'data/se-review.json';out.write_text(json.dumps(dict(episodes=report),ensure_ascii=False,indent=2)+'\n')
 print('SE:',{id:len(es) for id,es in report.items()})
 from assign_bgm import assign
 assign()
if __name__=='__main__':annotate()
