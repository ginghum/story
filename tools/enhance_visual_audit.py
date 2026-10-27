"""Visual audit follow-up: speaker visibility, scene-specific expressions and two held CG shots.
Only visual fields change; prose, ordering and legacy save offsets stay intact.
"""
import json,re,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SHOTS=[('chapter1-episode17','ルサイは、空いた椅子を少し引いた。','assets/cg/audit-study-terms.webp','用語集を挟み、プラスの話を静かに聞くルサイ',18),('chapter2-episode3','丸い塊が、小さくなっていた。','assets/cg/audit-hammer-discovery.webp','小さくなった鉄槌の先を確かめるプラスとランス',16)]
def main():
 metas=json.loads((R/'data/episodes.json').read_text())['episodes'];docs={m['id']:json.loads((R/m['file']).read_text()) for m in metas};actors={}
 for d in docs.values():
  for e in d['entries']:
   for c in e.get('cast',[]):actors.setdefault(c['id'],copy.deepcopy(c))
 fixed=0;expr=0;changes=[]
 for m in metas:
  d=docs[m['id']];before=copy.deepcopy(d['entries']);id=m['id'];n=int(id.split('episode')[-1]) if id.startswith('chapter2-episode') else 0
  for e in d['entries']:
   char=e.get('character');cast=e.get('cast',[])
   # Explicit voice-only speakers never enter the on-screen camera.
   if e['type']=='line' and char and char in actors and not char.startswith('mob-') and not e.get('cg') and '声' not in e.get('speaker','') and char not in [a['id'] for a in cast]:
    actor=copy.deepcopy(actors[char]);actor['name']=e['speaker'];actor['expression']='neutral' if (R/f'assets/characters/{char}-neutral.webp').exists() else actor['expression'];e['cast']=cast[:2]+[actor] if len(cast)>=3 else cast+[actor];fixed+=1
   for c in e.get('cast',[]):
    desired=None;sn=e.get('scene',0)
    if n:
     if c['id']=='minus' and n==5 and sn in [2,4,6,7]:desired='worried'
     if c['id']=='wan' and ((n==7 and sn>=8) or n in [8,9,12]):desired='hurt'
     if c['id']=='ruto' and ((n==7 and sn>=7) or n in [8,9,12]):desired='hurt'
     if c['id']=='milk' and c['expression']=='neutral' and ((n==18 and sn>=5) or (n==19 and sn==6) or (n==20 and sn>=8) or 21<=n<=23):desired='determined'
     if c['id']=='plus' and c['expression']=='smile' and 3<=n<=8 and e.get('bgm') in ['underground','tension','forest-battle','battle']:desired='serious'
    if desired and (R/f"assets/characters/{c['id']}-{desired}.webp").exists() and c['expression']!=desired:c['expression']=desired;expr+=1
  for target,anchor,file,alt,hold in SHOTS:
   if id!=target or not (R/file).exists():continue
   matches=[i for i,e in enumerate(d['entries']) if anchor in e.get('raw','')];assert len(matches)==1,(target,anchor)
   start=matches[0];scene=d['entries'][start]['scene'];count=0
   for e in d['entries'][start:]:
    if e['type']!='line' or e['scene']!=scene or count>=hold:break
    if e.get('cg') and e['cg']!=file:break
    e['cg']=file;e['cgAlt']=alt;count+=1
  for a,b in zip(before,d['entries']):assert {k:v for k,v in a.items() if k not in ['cast','cg','cgAlt']}=={k:v for k,v in b.items() if k not in ['cast','cg','cgAlt']}
  if before!=d['entries']:
   path=R/m['file'];path.write_text(json.dumps(d,ensure_ascii=False,indent=None if n else 2,separators=(',',':') if n else None)+'\n');changes.append(id)
 (R/'data/visual-audit-report.json').write_text(json.dumps(dict(episodes_checked=len(metas),speaker_lines_fixed=fixed,expression_entries_added=expr,updated_episodes=changes,shots=[dict(episode=t,anchor=a,file=f,alt=alt,hold=h) for t,a,f,alt,h in SHOTS],notes=['Text, entry order and save offsets are unchanged.','Voice-only speakers are excluded from portrait fallback.','Broad visual audit with targeted improvements, not a manual screenshot review of every line.']),ensure_ascii=False,indent=2)+'\n')
 from enhance_character_expressions import main as enhance_character_expressions
 enhance_character_expressions()
 print('Visual audit:',len(metas),'episodes;',fixed,'speaker lines;',expr,'expression entries;',len(changes),'updated episodes')
if __name__=='__main__':main()
