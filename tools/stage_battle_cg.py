"""Hold authored battle shots through continuous action, with explicit cuts and exact anchors."""
import collections,copy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 plan=json.loads((R/'data/battle-cg-plan.json').read_text())['scenes'];docs={};before={};rows=[]
 for p in plan:
  id=p['episode']
  if id not in docs:docs[id]=json.loads((R/'data'/f'{id}.json').read_text());before[id]=copy.deepcopy(docs[id])
  es=[e for e in docs[id]['entries'] if e['type']=='line' and e['scene']==p['scene']]
  def position(anchor):
   found=[i for i,e in enumerate(es) if e.get('raw')==anchor];assert len(found)==1,(id,p['scene'],anchor,len(found));return found[0]
  start=position(p['start']) if p.get('start') else 0;end=position(p['end']) if p.get('end') else len(es)
  cues={}
  for c in p['cues']:
   i=position(c['anchor']);assert start<=i<end,(id,p['scene'],i);cues[i]=c
  src=p.get('intro');alt='戦闘中の攻防';covered=0
  for i in range(start,end):
   if i in cues:src=cues[i]['src'];alt=cues[i]['alt'] or '戦闘中の攻防'
   if src:
    if not src.startswith('https://'):assert (R/src).is_file(),src
    es[i]['cg']=src;es[i]['cgAlt']=alt;covered+=1
   else:es[i].pop('cg',None);es[i].pop('cgAlt',None)
  rows.append(dict(episode=id,scene=p['scene'],lines=end-start,cg_lines=covered))
 changed=0
 for id,d in docs.items():
  a=before[id];assert len(a['entries'])==len(d['entries'])
  for x,y in zip(a['entries'],d['entries']):
   assert {k:v for k,v in x.items() if k not in ['cg','cgAlt']}=={k:v for k,v in y.items() if k not in ['cg','cgAlt']}
   changed+=x!=y
  if a!=d:(R/'data'/f'{id}.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
 report=dict(scene_ranges=len(rows),lines=sum(x['lines'] for x in rows),cg_lines=sum(x['cg_lines'] for x in rows),scenes=rows)
 (R/'data/battle-cg-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('Battle CG:',report['scene_ranges'],'ranges;',report['cg_lines'],'/',report['lines'],'lines;',changed,'changed')
if __name__=='__main__':main()
