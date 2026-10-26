"""Source-anchored expressions and period-correct portraits for extras 1–5."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

PALETTES={
 1:{4:{'yuhi':'serious','chick':'worried'},6:{'yuhi':'serious'},7:{'yuhi':'worried','chick':'worried'},8:{'yuhi':'serious'},9:{'chick':'worried'},11:{'yuhi':'serious'}},
 2:{2:{'konke':'serious'},3:{'konke':'reserved'},4:{'konke':'reserved'},6:{'konke':'serious'},7:{'oga':'serious','konke':'serious'},8:{'konke':'serious'},9:{'konke':'serious'},11:{'konke':'serious'}},
 3:{1:{'yaoi':'determined'},2:{'yaoi':'worried'},11:{'yaoi':'determined'},12:{'yaoi':'worried'}},
 4:{1:{'tsukuri':'worried','doma-past':'neutral'},2:{'tsukuri':'worried'},3:{'tsukuri':'worried','doma-past':'worried'},4:{'tsukuri':'worried','doma-past':'angry'},5:{'tsukuri':'worried','doma-past':'angry'},6:{'tsukuri':'worried','doma-past':'worried'},7:{'tsukuri':'worried','doma-past':'neutral'},8:{'tsukuri':'worried','doma-past':'angry'},9:{'tsukuri':'relieved','doma-past':'neutral'},10:{'tsukuri':'worried','doma-past':'worried'},11:{'tsukuri':'determined','doma-past':'worried'},12:{'tsukuri':'determined','doma-past':'angry'},13:{'tsukuri':'relieved','doma-past':'worried','doma':'determined'},14:{'tsukuri':'worried','doma':'worried'},15:{'tsukuri':'worried','doma':'determined'},16:{'tsukuri':'relieved','doma':'neutral'}},
 5:{1:{'lusai':'worried'},3:{'lusai-past':'worried'},4:{'lusai-past':'neutral'},5:{'lusai-past':'worried'},6:{'lusai-past':'neutral'},7:{'lusai-past':'worried'},8:{'lusai-past':'soft'},9:{'lusai-past':'soft'},10:{'lusai-past':'soft'},14:{'lusai':'worried','x-young':'serious'},15:{'lusai':'worried'},17:{'lusai':'worried'},18:{'lusai':'worried'},19:{'lusai':'worried'},21:{'lusai':'worried'},22:{'lusai':'worried'},23:{'lusai':'relieved'},24:{'lusai':'worried'}}
}
CUES={
 1:[(5,'生徒「そこまで興味ない」',{'yuhi':'worried','chick':'worried'})],
 2:[(4,'オーガ「助かった」',{'konke':'neutral'}),(7,'オーガ「飯作ってるところへ来られたら',{'oga':'neutral'}),(11,'グモン「食わねえのか」',{'gumon':'soft'})],
 3:[(8,'オジョー「話しかけていいとは、言っておりません」',{'ojo':'surprised'}),(12,'ヤオイ「全部話さなくても',{'yaoi':'smile'}),(16,'X「何でもない」',{'x':'soft'})],
 4:[(6,'ツクリ「ありがとう」',{'tsukuri':'relieved','doma-past':'neutral'}),
    (8,'ドーマ「お前、そういうの作ってんのか」',{'doma-past':'neutral','tsukuri':'relieved'}),
    (9,'サークルの部長「悪いんだけど。二人とも、退部してもらえないかな」',{'tsukuri':'worried','doma-past':'angry'}),
    (10,'ツクリ「一人で行くつもり、ないよ」',{'tsukuri':'determined'}),
    (12,'ドーマ「こんなんで、入れんのかよ」',{'doma-past':'worried'}),
    (14,'X「入部は認める。ただし',{'tsukuri':'relieved','doma':'determined'}),
    (15,'ツクリは笑った。',{'tsukuri':'relieved'})],
 5:[(4,'ルサイ「分かっている」',{'lusai-past':'angry'}),
    (4,'ゼクサー「……そういうつもりじゃ」',{'x-past':'worried'}),
    (4,'ゼクサー「……僕に勝ちたい、ということでいいのかい」',{'x-past':'serious'}),
    (5,'ゼクサー「ここから、もう一度考えたまえ。',{'x-past':'serious'}),
    (5,'ゼクサー「うん。合っている」',{'x-past':'neutral','lusai-past':'neutral'}),
    (6,'ゼクサー「僕の読み落としだね。すまない」',{'x-past':'worried'}),
    (6,'ゼクサー「そうだよ。だから、今のは君の勝ちだ」',{'x-past':'neutral'}),
    (6,'私は、少しだけ笑った。',{'lusai-past':'soft'}),
    (7,'ゼクサー「どうして、そうなる」',{'x-past':'serious'}),
    (7,'握ると、相手の指が力を返した。',{'lusai-past':'soft','x-past':'neutral'}),
    (15,'ルサイ「Xくん！　私の憧れた君は',{'lusai':'desperate'}),
    (15,'勝者の名が呼ばれた。',{'lusai':'worried'}),
    (18,'ルサイ「……おかえりなさい」',{'lusai':'relieved'}),
    (18,'X「僕は、イトグチさんに鍛えてもらって、強者になったんだ」',{'lusai':'worried'}),
    (19,'私は、笑うことにした。',{'lusai':'neutral'}),
    (20,'X「前のも、悪くなかったよ」',{'x':'soft','lusai':'relieved'}),
    (22,'私も、呼んだ。',{'lusai':'desperate'}),
    (22,'Xが、こちらを見た。',{'lusai':'relieved'}),
    (24,'誰も見ていなかった。',{'lusai':'sad'}),
    (24,'私は顔を拭き、彼の机へ置いた紙を一枚引いた。',{'lusai':'worried'})]
}

def apply(data):
 n=int(data['id'].replace('extra',''));es=data['entries']
 def actor(id,emotion='neutral'):
  base=id.replace('doma-past','doma')
  template=next((c for e in es for c in e['cast'] if c['id']==base),None)
  if template is None and id=='lusai':template={'id':'lusai','name':'ルサイ','height':180,'expression':'neutral'}
  assert template is not None,(data['id'],id)
  return dict(template,id=id,expression=emotion)
 def at(scene,prefix):
  matches=[i for i,e in enumerate(es) if e['scene']==scene and e.get('raw','').startswith(prefix)]
  assert len(matches)==1,(data['id'],scene,prefix,len(matches))
  return matches[0]
 cues={at(sn,text):mood for sn,text,mood in CUES.get(n,[])}
 marks={}
 if n==1:marks['interview']=at(8,'X「用件を、短く」')
 if n==2:marks['meal']=at(11,'グモン「食わねえのか」')
 if n==3:marks['rest']=at(2,'保健委員「じゃあ、しばらく強く動かさないで」')
 if n==4:
  for key,sn,text in [('pen',3,'ドーマが、机の下へ滑ったペンを拾っていた。'),('doma',4,'ドーマ「その手、離せよ」'),('laser',4,'白い光が、走った。'),('x',4,'X「下ろしたまえ」'),('glasses',13,'ドーマは、よく分からない顔をしたまま掛けた。'),('practice',13,'買って帰り、また練習した。'),('off',13,'夜が深くなり、ドーマが眼鏡を外した。'),('on',13,'眼鏡を掛け直した。'),('interview',14,'ドーマ「本日は お時間を いただき ありがとうございます」')]:marks[key]=at(sn,text)
 if n==5:
  for key,sn,text in [('handshake',7,'握ると、相手の指が力を返した。'),('invisible',15,'分かっていて、姿を消した。'),('return',18,'X「僕は、イトグチさんに鍛えてもらって、強者になったんだ」'),('grief',24,'誰も見ていなかった。')]:marks[key]=at(sn,text)
 last=None;mood={}
 for i,e in enumerate(es):
  sn=e['scene']
  if last!=sn:mood=dict(PALETTES.get(n,{}).get(sn,{}));last=sn
  mood.update(cues.get(i,{}))
  if e['type']!='line':continue
  if n==1 and sn==8 and i>=marks['interview']:e['cg']=None
  if n==2 and sn==11 and i>=marks['meal']:e['cg']=None
  if n==3 and sn==2 and i>=marks['rest']:e['cg']=None
  if n==4:
   past=sn<13 or (sn==13 and (i<marks['glasses'] or marks['off']<=i<marks['on']))
   did='doma-past' if past else 'doma'
   if sn in [1,6,7,8,9,10,11,12,13]:e['cast']=[actor('tsukuri'),actor(did)]
   if sn==3:e['cast']=[actor('tsukuri')]+([actor('doma-past')] if i>=marks['pen'] else [])
   if sn==4:
    e['cast']=[actor('tsukuri')]+([actor('doma-past')] if i>=marks['doma'] else [])+([actor('x','stern')] if i>=marks['x'] else [])
    e['cg']='assets/cg/extra4-doma-rescue.webp' if marks['laser']<=i<marks['x'] else None
   if sn==5:e['cast']=[actor('tsukuri'),actor('doma-past'),actor('x','stern')]
   if sn==13:e['cg']='assets/cg/extra4-etiquette-practice.webp' if marks['practice']<=i<marks['off'] else None
   if sn==14 and i>=marks['interview']:e['cg']=None
   if e.get('speaker')=='ドーマ':e['character']=did
  if n==5:
   if sn in [1,21,22,23]:e['cast']=[actor('lusai')]
   if sn==7:e['cg']='assets/cg/extra5-lusai-handshake.webp' if i>=marks['handshake'] else None
   if sn==15 and i>=marks['invisible']:e['cast']=[]
   if sn==18 and i>=marks['return']:e['cg']=None
   if sn==24 and i>=marks['grief']:e['cg']=None
  for c in e['cast']:
   if c['id'] in mood:c['expression']=mood[c['id']]
   assert (ROOT/f"assets/characters/{c['id']}-{c['expression']}.webp").exists(),(data['id'],c)
 return data
