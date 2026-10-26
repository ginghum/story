"""Reviewed chapter-one expressions; never infer emotions from keywords at runtime."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
# Each palette is reset at the source scene boundary. Injury artwork takes priority.
SCENES={
 0:{3:{'plus':'serious'},4:{'plus':'serious'},8:{'plus':'serious'}},
 1:{4:{'plus':'serious'}},
 2:{3:{'plus':'worried'}},
 3:{3:{'plus':'serious'},4:{'plus':'serious'},5:{'plus':'serious'},6:{'plus':'serious'},7:{'plus':'serious','yuji':'worried','lance':'worried'},8:{'yuji':'worried','lance':'worried'},9:{'yuji':'worried'}},
 4:{7:{'yuhi':'serious'},8:{'plus':'serious','yuhi':'serious'},9:{'plus':'serious'}},
 5:{s:{'plus':'serious'} for s in range(5,10)},
 6:{1:{'plus':'worried'},2:{'plus':'worried','lance':'worried'},4:{'yuji':'worried'},5:{'yuji':'worried'},7:{'plus':'serious','lance':'worried'},8:{'plus':'serious'},10:{'plus':'serious'},12:{'lance':'soft'}},
 7:{6:{'yuji':'worried','lance':'worried'},9:{'yuji':'worried','lance':'worried'},14:{'lance':'soft'}},
 8:{7:{'yuhi':'serious'},8:{'yuhi':'serious'},10:{'plus':'serious','yuji':'exasperated'},11:{'plus':'worried','yuji':'worried'},12:{'plus':'worried','yuji':'worried'},13:{'plus':'worried','yuji':'worried'}},
 9:{7:{'yuji':'worried'},10:{'plus':'serious','yuji':'worried','oga':'serious'},11:{'plus':'serious','yuji':'worried'},12:{'plus':'serious'}},
 10:{9:{'yuji':'worried'},11:{'yuji':'worried'},12:{'lance':'soft','gumon':'soft'}},
 11:{2:{'lance':'soft'},3:{'plus':'serious'},12:{'lance':'soft'},13:{'lance':'soft'}},
 12:{2:{'yukimero':'worried','lance':'worried'},3:{'lance':'annoyed'},4:{'plus':'worried','yuji':'worried','konke':'serious'},5:{'plus':'worried','yuji':'worried','konke':'serious'},9:{'plus':'worried','yuji':'worried','konke':'serious'},10:{'plus':'worried','yuji':'worried','yukimero':'worried'}},
 13:{1:{'plus':'worried','yuji':'worried'},2:{'plus':'worried','yuji':'worried','konke':'serious'},3:{'plus':'worried','yukimero':'worried'},4:{'plus':'worried','yuji':'worried','yukimero':'worried'},5:{'plus':'serious','yuji':'worried'},6:{'plus':'worried','yuji':'worried'},7:{'plus':'worried','yuji':'worried'},8:{'plus':'serious'},10:{'plus':'serious'}},
 14:{1:{'plus':'worried','yuji':'worried'},2:{'plus':'serious'},3:{'plus':'serious'},4:{'yukimero':'worried'},9:{'yuji':'worried','konke':'serious','yukimero':'worried'},11:{'plus':'worried','lance':'worried'},12:{'plus':'serious','lance':'worried'},13:{'yukimero':'worried','lance':'worried'},14:{'lance':'soft'},15:{'lance':'soft'},16:{'lance':'soft'}},
 15:{3:{'tsukuri':'relieved'},5:{'lance':'soft'}},
 16:{4:{'plus':'worried','doma':'worried','tsukuri':'worried','lusai':'worried'},5:{'lusai':'worried','plus':'worried','tsukuri':'worried'},6:{'plus':'worried','lance':'worried'},7:{'lusai':'worried','doma':'worried'}},
 17:{3:{'tsukuri':'worried','plus':'worried'},4:{'lusai':'worried','doma':'determined'},5:{'plus':'serious'},6:{'plus':'serious','lusai':'worried'}},
 18:{1:{'lusai':'worried','plus':'serious'},2:{'lusai':'worried','plus':'serious'},4:{'konke':'serious'},8:{'yuji':'worried','lance':'worried'},9:{'yuji':'worried','lance':'worried'},11:{'yuji':'worried','lance':'worried'}},
 19:{1:{'plus':'serious'},2:{'lusai':'worried','tsukuri':'worried','doma':'worried','yuji':'worried','lance':'worried','konke':'serious'},3:{'judge':'serious','plus':'serious'},5:{'lusai':'worried','tsukuri':'worried','doma':'worried'},9:{'lusai':'worried'}},
 20:{1:{'lusai':'desperate'},2:{'lusai':'worried','judge':'serious'},4:{'lusai':'worried'},6:{'lusai':'worried','tsukuri':'worried','doma':'worried'},12:{'lusai':'worried','tsukuri':'worried','doma':'worried','konke':'serious','yuji':'worried','lance':'worried'},15:{'yuji':'worried','lance':'worried','konke':'serious'}},
 21:{2:{'plus':'serious','judge':'serious'},3:{'plus':'worried'},4:{'plus':'serious'},5:{'plus':'serious'},6:{'plus':'serious'},7:{'judge':'serious'},8:{'plus':'serious','judge':'serious'},10:{'lusai':'relieved','tsukuri':'relieved','doma':'determined'},11:{'lance':'soft'},12:{'lance':'soft'}}
}
# Explicit original-prose anchors. No new source entries, text or save offsets.
CUES={
 14:[('ランス「……わかった」',{'yukimero':'neutral','lance':'soft'})],
 16:[('ドーマ「確認の計算も あります」',{'doma':'determined'}),('ツクリ「そうですか。よかった」',{'tsukuri':'relieved'})],
 20:[('ルサイ「Xくん！　私の憧れた君は',{'lusai':'desperate'}),
     ('ルサイ「……おかえりなさい」',{'lusai':'relieved'}),
     ('ルサイ「……座ろう、Xくん」',{'lusai':'worried'}),
     ('ルサイ「Xくん！」',{'lusai':'desperate'}),
     ('ドーマ「部長 私は まだ 何度も 間違えます」',{'lusai':'worried','doma':'determined'}),
     ('ツクリ「私は、部長、怖いです！」',{'tsukuri':'determined'}),
     ('ルサイ「君が負けた日のことを、僕は忘れていない」',{'lusai':'worried','tsukuri':'worried'}),
     ('ルサイは、その動きを見て、ようやく柵から手を離した。',{'lusai':'relieved','tsukuri':'relieved','doma':'determined'})],
 21:[('X「僕は、断ると答えたね」',{'x':'soft'}),
     ('ツクリ「……しばらく、か」',{'lusai':'worried','tsukuri':'worried','doma':'worried'}),
     ('ルサイ「……プラスくん。ありがとうございます」',{'lusai':'relieved','tsukuri':'relieved','doma':'determined'})]
}

def apply(data):
 if data['id'] in ['extra1','extra2','extra3','extra4','extra5']:
  from extra_expressions import apply as apply_extra
  return apply_extra(data)
 if data['id']!='prologue' and not data['id'].startswith('chapter1-'):return data
 n=0 if data['id']=='prologue' else int(data['id'].split('episode')[-1])
 es=data['entries'];last=None;active={};seen=set();reaction=False
 lusai=next((c.copy() for e in es for c in e['cast'] if c['id']=='lusai'),None)
 for e in es:
  sn=e['scene'];raw=e.get('raw','')
  if sn!=last:active=dict(SCENES.get(n,{}).get(sn,{}));last=sn;reaction=False
  for j,(anchor,emotions) in enumerate(CUES.get(n,[])):
   if raw.startswith(anchor) and (n!=14 or sn==13):
    assert j not in seen,(data['id'],anchor,'ambiguous');seen.add(j);active.update(emotions)
  # Preserve the CG for the establishing shot; move to portraits for the appeal.
  if n==20 and sn==1 and raw.startswith('ルサイ「Xくん！　私の憧れた君は'):reaction=True
  if n==20 and sn==1 and reaction:e['cg']=None;e['cast']=[dict(lusai,expression='desperate')]
  if n==20 and sn==6 and raw=='ルサイ「Xくん！」':reaction=True
  if n==20 and sn==6 and reaction:e['cg']=None
  # The repeated council CG gives way to faces for disclosure and the reply.
  if n==21 and ((3<=sn<=6) or (sn==7 and not e.get('cg','') in ['assets/cg/episode21-handshake.webp','assets/cg/episode21-c.webp'])):
   if e.get('cg')=='assets/cg/episode21-a.webp':e['cg']=None
  for c in e['cast']:
   mood=active.get(c['id'])
   if not mood:continue
   old=c['expression']
   if old in ['hurt','pain','battle-hurt','shaken','reserved']:continue
   if old.startswith('bandaged'):
    if mood in ['serious','worried']:c['expression']='bandaged-serious'
    continue
   c['expression']=mood
   assert (ROOT/f"assets/characters/{c['id']}-{mood}.webp").exists(),(c['id'],mood)
 assert len(seen)==len(CUES.get(n,[])),(data['id'],'missing anchors',set(range(len(CUES.get(n,[]))))-seen)
 return data

def main():
 counts={};pending=[]
 for meta in json.loads((ROOT/'data/episodes.json').read_text())['episodes']:
  if meta['id']!='prologue' and not meta['id'].startswith('chapter1-') and meta['id'] not in ['extra1','extra2','extra3','extra4','extra5']:continue
  p=ROOT/meta['file'];old=p.read_text();data=apply(json.loads(old));new=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
  if new!=old:pending.append((p,new))
  counts[meta['id']]=sum(c['expression'] not in ['neutral','smile','stern'] for e in data['entries'] for c in e['cast'])
 for p,new in pending:p.write_text(new)
 print(json.dumps(counts))

if __name__=='__main__':main()
