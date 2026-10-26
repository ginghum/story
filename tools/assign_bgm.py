"""Reviewed mood assignments for each source scene; dialogue and visuals stay intact."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# d=daily, c=calm, p=practice, b=battle, t=tension, r=reflection.
KEYS=dict(d='daily',c='calm',p='training',b='battle',t='tension',r='reflection')
PLANS={0:'c d c d d p d p r t',1:'t d d c d d c',2:'c d d d r',3:'d d t b b b r r c r r',4:'r p d d c c c t t c d',5:'c p d c t b b b r d t',6:'r r r r t r r r p c p r',7:'r c c r t t t b b b b r r d c',8:'c d c d c c t t d t t t t',9:'t r r t t r t d c b t t',10:'b b b t t t b r b r r d r',11:'d p c p d d c d d d d c r r r',12:'t r t t t b b b b r',13:'r r r r t r r c p c p r',14:'r c r c t b b b t b r r r d d d'}
CUES={12:[(9,'サニー「終了！　勝者、ランス！」','reflection'),(10,'ランスの後ろで、声がした。',None)],13:[(5,'最後に、寮の方へ足を向けた。','reflection')],14:[(10,'ユージ「終わり。もう、やらない」','reflection'),(12,'ランス「だから、何もしなかったら、そこにいていいのか、わかんなくなった」',None),(12,'プラス「……俺、教えてくれたの、嬉しかったよ」','reflection'),(16,'誰も星を出さずに、その夜は続いていた。','reflection')],0:[(4,'食器の音とは違う、乾いた音がした。','battle'),(4,'青年は必要な確認を済ませると、','reflection')],3:[(6,'鈍い音がした。',None),(6,'コンケは、一歩下がった。','tension'),(6,'ランス「終わり」','reflection')],5:[(11,'鞭が床から浮く。','battle')],7:[(7,'左腕を前へ運び、投げた。','battle')],10:[(9,'グモンは、扉の前に立っていた。','reflection')],11:[(15,'ポケットの上で、ランスの手が止まった。',None)]}
LOCATIONS={(0,'学生寮／三人の部屋・消灯後'):'reflection',(1,'学生寮／三人の部屋・朝'):'daily',(2,'学園／中庭'):'tension',(3,'学生寮そば／能力練習場・夜'):'tension',(6,'回想／ヒカルとの決闘'):'tension',(6,'能力練習場／夜'):'training',(10,'回想／朝の能力練習場'):'training',(10,'学園／昼の中庭'):'daily'}
def assign():
 report={};count=0
 for n,plan in PLANS.items():
  id='prologue' if n==0 else f'chapter1-episode{n}';path=ROOT/'data'/f'{id}.json';d=json.loads(path.read_text());moods=[KEYS[x] for x in plan.split()];assert len(moods)==d['source_scenes'];seen=set();last_scene=None;last_location=None;active=None;transitions=[]
  for i,e in enumerate(d['entries']):
   if e['scene']!=last_scene:active=moods[e['scene']-1];last_scene=e['scene'];last_location=None
   if e['location']!=last_location:
    last_location=e['location']
    if (n,last_location) in LOCATIONS:active=LOCATIONS[n,last_location]
   for ci,(sn,match,track) in enumerate(CUES.get(n,[])):
    if sn==e['scene'] and match in e.get('raw',''):
     assert ci not in seen;seen.add(ci);active=track
   e['bgm']=active
   if i==0 or active!=d['entries'][i-1]['bgm']:transitions.append(dict(entry=i,scene=e['scene'],location=e['location'],track=active))
  assert len(seen)==len(CUES.get(n,[])),(id,'missing cues',seen)
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');report[id]=dict(source_scenes=d['source_scenes'],scenes=[dict(scene=i+1,track=track) for i,track in enumerate(moods)],transitions=transitions);count+=d['source_scenes']
 (ROOT/'data/bgm-scenes.json').write_text(json.dumps(dict(episodes=report),ensure_ascii=False,indent=2)+'\n');print('BGM:',len(report),'episodes,',count,'source scenes')
if __name__=='__main__':assign()
