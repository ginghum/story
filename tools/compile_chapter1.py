"""Compile reviewed scene directions without changing or summarizing original prose."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'chapter-work'
SOURCE=ROOT.parent/'chapter-source-latest.json'
CHAR={
 'プラス':('plus',184,'smile'),'ユージ':('yuji',175,'neutral'),'ランス':('lance',169,'neutral'),
 'ツクリ':('tsukuri',157,'neutral'),'ドーマ':('doma',160,'neutral'),'X':('x',180,'stern'),
 'ルサイ':('lusai',176,'neutral'),'バルー':('baroo',151,'neutral'),'ヒカル':('hikaru',184,'neutral'),
 'ゆきめろ':('yukimero',146,'neutral'),'コンケ':('konke',178,'neutral'),
 'ユーヒ':('yuhi',170,'neutral'),'ダイ':('dai',182,'neutral'),'モルペウス':('morpheus',165,'neutral'),'チック':('chick',176,'neutral'),'サニー':('sunny',159,'neutral'),
 '親衛隊の男子':('mob-male-broad',180,'brown'),'不良の男子':('mob-male-broad',182,'brown')}
BG=lambda x:'assets/bg/'+x+'.webp' if x else None
CG=lambda x:'assets/cg/'+x+'.webp' if x else None
TRIO=['プラス','ユージ','ランス']
def scene(loc,bg,cast=(),tone='',cg=None):return dict(location=loc,bg=BG(bg),cast=list(cast),tone=tone,cg=CG(cg),cgAlt='')
def cue(match,*,location=None,bg=None,cast=None,cg='KEEP',tone=None,expressions=None,cut=False):
 d={'match':match,'cut':cut}
 for k,v in [('location',location),('cast',cast),('tone',tone),('expressions',expressions)]:
  if v is not None:d[k]=v
 if bg is not None:d['bg']=BG(bg)
 if cg!='KEEP':d['cg']=CG(cg)
 return d
PLANS={1:[
 (scene('？？？',None,tone='dream'),[
  cue('目を開くと、天井があった。',location='学生寮／三人の部屋・朝',bg='dorm-morning',cast=TRIO,tone='',cut=True,expressions={'プラス':'pain'}),
  cue('ユージは起き上がり、部屋の時計を見た。',expressions={'プラス':'smile'})]),
 (scene('学生寮／台所・朝','dorm-morning',TRIO,cg='episode01-d'),[
  cue('プラスは最後のパンを口へ入れ、ローブを羽織った。',cg=None),
  cue('隣の部屋の扉にあった名札が、',location='学生寮／廊下',bg='corridor',cg=None,cut=True)]),
 (scene('学園敷地内／通学路','campus',TRIO),[
  cue('プラス「寮って、普通、学校の近くにねえの！」',cg='episode01-a'),
  cue('校舎の入口で、靴底が石を擦った。',cg=None),
  cue('昨日と同じ教室へ滑り込む。',location='校舎／教室',bg='classroom',cut=True)]),
 (scene('校舎／教室・授業','classroom',TRIO,cg='episode01-c'),[]),
 (scene('校舎／教室・休み時間','classroom',TRIO),[
  cue('午前の授業を終え、三人で廊下へ出た時、',location='校舎／廊下',bg='corridor',cut=True),
  cue('ツクリ「ドーマちゃん、こっち向かなくていいから！',cast=['プラス','ツクリ','ドーマ']),
  cue('プラスは一番外側の束を受け取った。',cg='episode01-b-v2')]),
 (scene('学園／食堂・昼','cafeteria',TRIO),[
  cue('ランス「席取っとく。遅えと食う時間なくなるぞ」',cast=['プラス','ユージ']),
  cue('席へ戻ると、ランスが空いた椅子を足で引いた。',cast=TRIO)]),
 (scene('学園敷地内／食堂前','campus',TRIO),[
  cue('ユージの返事は、朝より少し短かった。',cast=['プラス']),
  cue('図書館へは、ツクリとドーマが途中まで案内してくれた。',cast=['プラス','ツクリ','ドーマ']),
  cue('角を曲がると、図書館が見えた。',location='図書館／入口',bg='library-entrance',cut=True)])
]}

PLANS[2]=[
 (scene('図書館／勉強サークル','library',['プラス','ツクリ','ドーマ']),[
  cue('プラス「……あれ。今、そこにいた？」',cast=['プラス','ルサイ']),
  cue('奥の机に、Xがいた。',cast=['プラス','X','ルサイ']),
  cue('ドーマ「こちらの答えと、結果が合いません」',cast=['プラス','ツクリ','ドーマ']),
  cue('Xは受け取った用紙を、速い手つきで見ていった。',cast=['プラス','X','ルサイ'],cg='episode02-a'),
  cue('しばらくすると、ルサイが小皿を机の端に置いた。',cg=None),
  cue('ドーマ「休憩の開始時刻を確認してもよろしいでしょうか」',cast=['プラス','ツクリ','ドーマ']),
  cue('ルサイ「ありがとうございます。フィナンシェです」',cast=['プラス','ルサイ','X']),
  cue('ドーマ「部長のお皿は、毎回空になります」',cast=['プラス','ドーマ','X']),
  cue('プラスは、ふたりがここで仲良くしている理由を',cast=['プラス','ツクリ','ドーマ']),
  cue('X「来るなら、今日指摘したことは覚えておくように」',cast=['プラス','X','ルサイ']),
  cue('図書館の扉を出ると、遠くで人の笑う声がした。',location='図書館／入口',bg='library-entrance',cast=['プラス'],cut=True)]),
 (scene('学園敷地内／午後の通り','campus',['プラス'],tone='evening'),[
  cue('小さな購買が、校舎の脇にあった。',location='学園／購買通り',bg='shop',cut=True),
  cue('バルー「やっほ〜☆　新聞買ってね〜！」',cast=['プラス','バルー']),
  cue('プラス「新聞？」',cg='episode02-c')]),
 (scene('中央購買／店内','shop',['プラス']),[
  cue('外に出ると、少し離れた中庭から、声が聞こえた。',location='学園／中庭',bg='courtyard',cut=True),
  cue('衣装の色が、先に見えた。',cg='episode02-yuji'),
  cue('裾を片手で押さえ、花壇の横を走り、建物の角へ消えた。',cg=None,cast=['プラス']),
  cue('ヒカル「どこへ行くんだい？」',cast=['プラス','ヒカル'])]),
 (scene('学園敷地内／離れ校舎への道','campus',['プラス'],tone='evening'),[
  cue('離れ校舎は、通りの賑わいから少し外れていた。',location='離れ校舎／オタクサークル前',bg='club-corridor',cut=True),
  cue('ゆきめろ「……そうだよぉ。めろに、何か用？」',cast=['プラス','ゆきめろ']),
  cue('親衛隊の男子「おい！」',cast=['プラス','ゆきめろ','親衛隊の男子']),
  cue('ランス「てめえ、ゆきめろちゃんに――」',cast=['プラス','ランス','ゆきめろ']),
  cue('ランス「こいつ、俺の同居人。帰れ。もういい」',cg='episode02-b'),
  cue('少女は小さく手を振り、扉の向こうへ戻った。',cg=None,cast=['プラス','ランス'])]),
 (scene('学園敷地内／夕方の帰り道','campus',['プラス'],tone='evening'),[
  cue('扉を開けると、ユージがいた。',location='学生寮／三人の部屋・夕方',bg='dorm',cast=['プラス','ユージ'],tone='',cut=True),
  cue('机の前には、ランスもいた。',cast=TRIO)])
]

PLANS[3]=[
 (scene('学生寮／三人の部屋・夕食','dorm-night',TRIO),[]),
 (scene('学生寮／三人の部屋・夜','dorm-night',TRIO),[
  cue('三人で扉を出る。',location='学生寮／廊下・夜',bg='corridor',tone='night',cut=True),
  cue('練習場までの道は、学校までより短い。',location='学生寮そば／能力練習場・夜',bg='training-night',tone='',cut=True),
  cue('コンケ「んん〜？　弱そうな奴がいるな！',cast=['プラス','コンケ','ユージ']),
  cue('プラス「俺、プラス。昨日来たんだ」',cg='episode03-d'),
  cue('不良の男子「お前ら、まだ1？」',cg=None,cast=['プラス','コンケ','不良の男子']),
  cue('ランス「……ずいぶん変わったな」',cast=['プラス','コンケ','ランス'])]),
 (scene('能力練習場／試合区画','training-night',TRIO),[
  cue('コンケは、少し離れたところで手帳を開いた。',cast=['プラス','コンケ','ランス'])]),
 (scene('能力練習場／試合区画','training-night',['プラス','コンケ','ランス']),[cue('肩へ拳が当たった。',expressions={'プラス':'pain'})]),
 (scene('能力練習場／試合区画','training-night',['プラス','コンケ','ランス']),[
  cue('ユージ「プラス、やめてもいいんだぞ！」',cast=TRIO),
  cue('コンケ「何だよ。相談会？',cast=['プラス','コンケ','ランス'])]),
 (scene('能力練習場／試合区画','training-night',['プラス','コンケ','ランス']),[
  cue('鈍い音がした。',cg='episode03-impact-night'),
  cue('ランス「終わり」',cg=None,expressions={'コンケ':'hurt'}),
  cue('プラスも、自分の手帳を閉じた。',cast=TRIO)]),
 (scene('能力練習場／試合区画','training-night',TRIO),[
  cue('コンケは、離れたところでまだこちらを見ていた。',cast=['プラス','コンケ','ユージ']),
  cue('コンケは背を向けた。',cast=TRIO)]),
 (scene('学園／保健の窓口','infirmary',TRIO),[
  cue('答えながら、ようやく、自分がどれだけ無理をしたのかを知った。',cg='episode03-c'),
  cue('外へ出た時には、空がすっかり暗くなっていた。',location='学園敷地内／夜の帰り道',bg='campus-night',cg=None,cut=True,expressions={'プラス':'bandaged'}),
  cue('寮の入口へ着いた。',location='学生寮／入口',cut=True)]),
 (scene('学生寮／三人の部屋・就寝前','dorm-night',TRIO),[
  cue('電気が消えた。',cast=[],tone='dark')]),
 (scene('？？？',None,tone='dream'),[
  cue('歌が、聞こえた。',cg='episode03-b')]),
 (scene('学生寮／三人の部屋・深夜','dorm-night',tone='dark'),[])
]

NEWS=['プラス','ユーヒ','バルー','チック','モルペウス','ダイ']
PLANS[4]=[
 (scene('学生寮／三人の部屋・朝','dorm-morning',['プラス','ランス']),[
  cue('ユージ「……何、喋ってんの」',cast=TRIO)]),
 (scene('学生寮／三人の部屋・朝','dorm-morning',TRIO),[
  cue('朝の練習場は、昨夜より広く見えた。',location='学生寮そば／能力練習場・朝',bg='training',cut=True),
  cue('ランスが手帳を開いた。',cg='episode04-practice-staff')]),
 (scene('学園敷地内／朝の通学路','campus',TRIO),[
  cue('授業は相変わらず難しかった。',location='校舎／教室',bg='classroom',cut=True),
  cue('三人で教室を出た。',location='校舎／廊下',bg='corridor',cut=True)]),
 (scene('学園／食堂前','campus',TRIO),[
  cue('ユーヒ「プラスくんっすね！」',cast=['プラス','ユーヒ','バルー']),
  cue('バルー「やっほ〜。今日も会えたね」',cg='episode04-d')]),
 (scene('学園／食堂前・午後','campus',['プラス','バルー']),[
  cue('扉の前には、夕陽新聞編集部、と書かれた表示があった。',location='校舎／新聞部前の廊下',bg='corridor',cut=True),
  cue('広い部屋ではなかった。',location='新聞部／夕陽新聞編集部',bg='newsroom',cut=True),
  cue('ダイ「いらっしゃいませ。見学の方ですね。',cast=['プラス','ダイ','バルー']),
  cue('モルペウス「……ここ、座れるよ。',cast=['プラス','ダイ','モルペウス']),
  cue('チック「そこまでしなくて大丈夫ですよ。',cast=['プラス','チック','モルペウス']),
  cue('ユーヒ「ようこそ、夕陽新聞編集部へ！」',cast=NEWS)]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS,cg='episode04-b-r3'),[
  cue('チック「見出しにする前に、本人の感想を聞いてください」',cg=None)]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS),[
  cue('取材の途中で、モルペウスが新しい紙を持ってきた。',cast=['プラス','ユーヒ','チック','モルペウス','ダイ']),
  cue('バルーが扉を閉めて戻ってきた。',cast=NEWS)]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS),[]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS),[
  cue('プラス「今日、夢で、昔のことかもしれねえのを見たんだよ」',cg='episode04-c'),
  cue('バルー「モルペウス、夢を見せる能力なんだよ」',cg=None)]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS),[]),
 (scene('新聞部／夕陽新聞編集部','newsroom',NEWS),[
  cue('プラスは扉の外へ出て、もう一度中を見た。',location='校舎／新聞部前の廊下',bg='corridor',cast=['プラス'],cut=True),
  cue('校舎の外へ出ると、プラスは日差しの中で目を細めた。',location='学園敷地内／中庭への道',bg='campus',cut=True)])
]
PLANS[5]=[
 (scene('学園／中庭の大きな木','courtyard-tree',['プラス']),[]),
 (scene('学園敷地内／闘技場への道','campus',['プラス']),[
  cue('中へ入ると、遠くから歓声がした。',location='闘技場／通路',bg='arena-reception',cut=True),
  cue('プラスは、近くの観客席へ向かった。',location='闘技場／観客席',bg='arena',cut=True),
  cue('競技面では、一人が相手の周りを回っていた。',cg='episode05-observed-duel'),
  cue('プラスは、手すりへ左手を置いた。',cg=None)]),
 (scene('闘技場／通路','arena-reception',['プラス']),[
  cue('ダイ「プラスさん」',cast=['プラス','ダイ']),
  cue('プラス「おお。さっきぶり」',cg='episode05-d')]),
 (scene('闘技場／決闘委員会受付','arena-reception',['プラス','ダイ']),[
  cue('サニー「こんにちは。対戦のお申し込みですか？」',cast=['プラス','ダイ','サニー']),
  cue('サニーは、ふたりの手帳を確認した。',cg='episode05-c-handbook-v2'),
  cue('ダイが、少し離れた席へ腰を下ろす。',cg=None,cast=['プラス'])]),
 (scene('闘技場／武器なし競技面','arena-floor',['プラス','ダイ','サニー']),[]),
 (scene('闘技場／武器なし競技面','arena-floor',['プラス','ダイ']),[
  cue('そこへ左拳を出す。',cg='episode05-a-r3')]),
 (scene('闘技場／武器なし競技面','arena-floor',['プラス','ダイ']),[
  cue('プラス「――そこ！」',cg='episode05-a-r3'),
  cue('ダイは、ゆっくり歩いた。',cg=None)]),
 (scene('闘技場／武器なし競技面','arena-floor',['プラス','ダイ']),[
  cue('身体が傾いた。',cg='episode05-hold'),
  cue('サニー「そこまで！',cg=None,cast=['プラス','ダイ','サニー'])]),
 (scene('闘技場／武器なし競技面','arena-floor',['プラス','ダイ','サニー'],cg='episode05-b-r3'),[
  cue('サニーが、手帳の確認へふたりを呼んだ。',location='闘技場／競技面脇の確認場所',bg='arena-reception',cg=None,cut=True)]),
 (scene('闘技場／通路','arena-reception',['プラス','ダイ']),[
  cue('ダイは自然に頭を下げ、通路の先へ歩いた。',cast=['プラス'])]),
 (scene('闘技場／案内板前','arena-reception',['プラス']),[
  cue('遠くから、歓声がした。',location='闘技場／武器あり競技面の観客席',bg='arena',cut=True),
  cue('向かいに、ヒカルがいた。',cg='episode05-yuji-battle-v3')])
]

def default_expression(name,text):
 if name=='プラス':
  if any(w in text for w in ['痛え','ぐ……','おっも','……降参','本当に、減る','……ありがと']):return 'pain'
  if any(w in text for w in ['？','すげ','うわ','……あれ','何','でけえ']):return 'surprised'
  if any(w in text for w in ['やる。','分かった。勉強','不合格']):return 'serious'
  return 'smile'
 if name=='ツクリ':return 'worried' if any(w in text for w in ['！','……部長','Xさん']) else 'neutral'
 if name=='ヒカル':return 'cold' if any(w in text for w in ['不合格','美しく','価値','時間は','着せたい']) else 'neutral'
 if name=='ユージ':
  if any(w in text for w in ['！','ねえだろ','見るな','ほんとに']):return 'exasperated'
  if any(w in text for w in ['何これ','……マジ','記憶']):return 'surprised'
  return 'neutral'
 if name=='ランス':
  if any(w in text for w in ['！','何して','うるせ','出てねえ','触るな']):return 'annoyed'
  if any(w in text for w in ['夢','前のこと','誰も']):return 'surprised'
  return 'neutral'
 return CHAR.get(name,('',0,'neutral'))[2]

def portrait_expression(n,sn,name,expr,st):
 emotion=expr.get(name,CHAR[name][2])
 if n==3 and name=='コンケ' and (sn>=7 or (sn==6 and emotion=='hurt')):return 'hurt'
 if n==5 and name=='ダイ' and 5<=sn<=9:return 'battle'
 if name=='プラス':
  injured=n>=4 or (n==3 and (sn>=9 or (sn==8 and st['location']!='学園／保健の窓口')))
  if injured:
   if n==5 and 5<=sn<=8:emotion='serious'
   return {'smile':'bandaged-smile','surprised':'bandaged-surprised','serious':'bandaged-serious'}.get(emotion,'bandaged')
  if n==3 and (5<=sn<=8 or (sn==4 and emotion=='pain')):return 'pain'
  if n==3 and sn==4:return 'serious'
 return emotion

def chunks(text,limit=105):
 out=[];buf=''
 for sentence in re.findall(r'.*?[。！？](?:[」』])?|.+$',text):
  if len(buf)+len(sentence)>limit and buf:out.append(buf);buf=''
  while len(sentence)>limit:
   if buf:out.append(buf);buf=''
   split=max(sentence.rfind('、',0,limit),sentence.rfind('。',0,limit))
   split=split+1 if split>=limit//2 else limit
   out.append(sentence[:split]);sentence=sentence[split:]
  buf+=sentence
 if buf:out.append(buf)
 assert ''.join(out)==text
 return out

def compile_episode(n,source):
 id=f'chapter1-episode{n}';ch=next(c for c in source['chapters'] if c['id']==id)
 parts=ch['body'].split('　　　　　＊');plans=PLANS[n];assert len(parts)==len(plans)
 entries=[];raws=[];reviews=[]
 for sn,(part,(initial,cues)) in enumerate(zip(parts,plans),1):
  st=dict(initial);expr={};seen=set();start=len(entries);camera=st['cast'][:3]
  def state():
   cast=[dict(id=CHAR[name][0],name=name,height=CHAR[name][1],expression=portrait_expression(n,sn,name,expr,st)) for name in camera]
   assert len(cast)<=3
   return dict(scene=sn,location=st['location'],bg=st['bg'],tone=st['tone'],cg=st['cg'],cgAlt=st.get('cgAlt') or '物語の挿絵',cast=cast)
  # Establish the place before characters enter the shot.
  loc=state();loc['cast']=[]
  if not entries or entries[-1]['location']!=loc['location'] or entries[-1]['bg']!=loc['bg']:entries.append(dict(type='location',**loc))
  for raw in part.splitlines():
   line=raw.strip()
   if not line:continue
   raws.append(line)
   for ci,c in enumerate(cues):
    if line.startswith(c['match']):
     assert ci not in seen,(n,sn,c['match']);seen.add(ci)
     for key in ['location','bg','cast','tone','cg']:
      if key in c:st[key]=c[key]
     if 'cast' in c:camera=st['cast'][:3]
     expr.update(c.get('expressions',{}))
     if c['cut']:
      loc=state();loc['cast']=[];entries.append(dict(type='location',**loc))
   m=re.match(r'^([^「『]{1,16})([「『].*)$',line)
   # Only standalone speaker labels; never interpret quoted narrative as a speaker.
   name=m.group(1) if m and not any(w in m.group(1) for w in ['の','、','は','を','が']) else ''
   # Role labels legitimately containing の are allowed explicitly.
   if m and (m.group(1) in CHAR or m.group(1) in ['先生','不良の男子','親衛隊の男子']):name=m.group(1)
   text=m.group(2) if name else line
   if name in st['cast'] and name not in camera:
    keep=[x for x in camera if x not in ['プラス',name]]
    camera=(['プラス'] if 'プラス' in st['cast'] else [])+keep[-1:]+[name]
   if name in CHAR and not (name=='コンケ' and expr.get(name)=='hurt'):expr[name]=default_expression(name,text)
   for i,chunk in enumerate(chunks(text)):
    entries.append(dict(type='line',text=chunk,speaker=name,character=CHAR.get(name,(None,))[0],raw=line if i==0 else '',effect=('teleport' if n==5 and sn in [6,7,8] and line in ['ダイは、消えた。','ダイが消えた。','消えた。'] else line in ['鈍い音がした。','横腹へ蹴りが入った。','音がした。']),**state()))
  assert len(seen)==len(cues),('unmatched cues',n,sn,[c['match'] for i,c in enumerate(cues) if i not in seen])
  reviews.append(dict(scene=sn,start=start,end=len(entries)-1,location=initial['location'],source_lines=len([l for l in part.splitlines() if l.strip()]),locations=list(dict.fromkeys(e['location'] for e in entries[start:])),reviewed=True))
 assert [e['raw'] for e in entries if e.get('raw')]==raws
 data=dict(id=id,title=ch['title'],entries=entries,source_lines=len(raws),source_scenes=len(parts),source_hash=hashlib.sha256(ch['body'].encode()).hexdigest())
 (ROOT/'data'/f'{id}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 return reviews

EPISODE_TITLES={'chapter1-episode1': '第1章\u3000第1話\u3000この学園で、友達になろう', 'chapter1-episode2': '第1章\u3000第2話\u3000知ってるあいつは、知らない顔をする', 'chapter1-episode3': '第1章\u3000第3話\u3000今夜はまだ、眠るには早い', 'chapter1-episode4': '第1章\u3000第4話\u3000俺のことも、載っていますか', 'chapter1-episode5': '第1章\u3000第5話\u3000次の相手は、誰だろう'}

EPISODE_TITLES['chapter1-episode6']='第1章　第6話　いつも通りが、うまくできない'

def main():
 source=json.load(open(SOURCE)) if SOURCE.exists() else {'chapters':[{'id':p.stem,'title':EPISODE_TITLES[p.stem],'body':p.read_text()} for p in (ROOT/'data/source').glob('*.txt') if p.stem in EPISODE_TITLES]};reports={};episodes=[dict(id='prologue',title='プロローグ',file='data/prologue.json',image='assets/cg/prologue-a.webp',description='海の向こうの学園へ。プラスの、新しい一日が始まる。')]
 for n in sorted(PLANS):
  reports[f'chapter1-episode{n}']=compile_episode(n,source);id=f'chapter1-episode{n}';ch=next(c for c in source['chapters'] if c['id']==id)
  image={1:'episode01-a',2:'episode02-a',3:'episode03-d',4:'episode04-d',5:'episode05-d'}[n]
  desc=['初めての朝、初めての授業。仲間と歩いて、この学園を知っていく。','図書館、新聞、中庭、離れ校舎。友達の知らない顔に出会う午後。','今夜の練習相手は、ふたりの元同居人。重さを変える力で、何ができるのか。','夕陽新聞編集部での取材。名前と能力が、過去を探す手がかりになる。','会いたい人を探す午後、初めての正式な決闘。そして、闘技場で見た友達の姿。'][n-1]
  episodes.append(dict(id=id,title=ch['title'],file=f'data/{id}.json',image=CG(image),description=desc))
 (ROOT/'data/episodes.json').write_text(json.dumps(dict(episodes=episodes),ensure_ascii=False,indent=2)+'\n')
 (ROOT/'data/chapter1-scene-review.json').write_text(json.dumps(dict(episodes=reports),ensure_ascii=False,indent=2)+'\n')
 print({id:len(report) for id,report in reports.items()})
if __name__=='__main__':
 main()
 if (ROOT/'data/source/chapter1-episode6.txt').exists():
  import compile_episode6
  compile_episode6.main()
  compile_episode6.c.default_expression=compile_episode6.original_expression
  compile_episode6.c.CHAR['プラス']=('plus',184,'smile')
 if (ROOT/'data/source/chapter1-episode10.txt').exists():
  import compile_continuation
  compile_continuation.main()

 from enhance_battles_audio import enhance
 enhance()
if __name__=='__main__':
  from assign_expressions import main as assign_expressions
  assign_expressions()

if __name__=="__main__":
 from enhance_visual_audit import main as enhance_visual_audit
 enhance_visual_audit()

if __name__ == "__main__":
 from stage_all_mobs import main as stage_all_mobs
 stage_all_mobs()
