"""Scene-directed expression additions. Never changes prose or save positions."""
import collections,copy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def choose(who,n,s,text):
 if who=='beret':
  if n==23:
   if s==1:return 'shocked'
   if s in [3,5,12]:return 'smug'
   if s in [14,15]:return 'angry'
  if n==24:return 'angry'
  if n==17 and s==6:return 'serious'
  if (n==15 and s in [5,6]) or (n==16 and s==7) or n in [17,18,21,22]:return 'smug'
  return 'neutral'
 if who=='kagachi':
  if '許せない' in text:return 'angry'
  if n==10:return 'smile' if s<=13 else 'serious'
  if n==12:
   if any(x in text for x in ['冗談だよ','ご馳走したのに','おいしいもの','そうだろう','店は、好き','返事もいらない','食べてはいけない','飯を食べて']):return 'smile'
   return 'serious'
  return 'smile'
 if who=='jend':
  if any(x in text for x in ['止まらなくていい','早く行こう','騒ぐなら']):return 'angry'
  if any(x in text for x in ['グレード0だから','ここへ来た','下だよ','いらっしゃった','駄目だよ','持ってこなくていい','聞いてなかった','必要ないよ','大人しく']):return 'serious'
  return 'smug' if '♪' in text or '管理担当' in text else 'neutral'
def main():
 counts=collections.Counter();changed=[]
 for m in json.loads((R/'data/episodes.json').read_text())['episodes']:
  if not m['id'].startswith('chapter2-episode'):continue
  n=int(m['id'].split('episode')[-1]);p=R/m['file'];d=json.loads(p.read_text());before=copy.deepcopy(d);state={};scene=None
  for e in d['entries']:
   if scene!=e.get('scene'):state={};scene=e.get('scene')
   who=e.get('character')
   if who in ['beret','kagachi','jend']:state[who]=choose(who,n,scene,e.get('raw') or e.get('text',''))
   for c in e.get('cast',[]):
    if c['id'] in ['beret','kagachi','jend']:
     expr=state.get(c['id']) or choose(c['id'],n,scene,'')
     assert (R/f"assets/characters/{c['id']}-{expr}.webp").is_file(),(c['id'],expr)
     c['expression']=expr;counts[c['id']+'-'+expr]+=1
  assert len(before['entries'])==len(d['entries'])
  for a,b in zip(before['entries'],d['entries']):assert {k:v for k,v in a.items() if k!='cast'}=={k:v for k,v in b.items() if k!='cast'}
  if before!=d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n');changed.append(m['id'])
 print('Character expressions:',dict(counts),'updated:',len(changed))
 return dict(usage=dict(counts),episodes_changed=changed)
if __name__=='__main__':main()
