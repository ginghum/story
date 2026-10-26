"""Compile subsequent episodes with paragraph-internal staging cues and exact prose coverage."""
import json,re,hashlib
from pathlib import Path
import compile_chapter1 as c
ROOT=Path(__file__).resolve().parents[1]
scene,cue=c.scene,c.cue
D=['プラス','ランス'];P=['プラス','ユージ'];T=c.TRIO;NEWS=['プラス','ユーヒ','バルー','チック','モルペウス','ダイ']
c.CHAR.update({'オーガ':('oga',197,'neutral'),'グモン':('gumon',189,'neutral'),'ヤオイ':('yaoi',155,'neutral'),'オジョー':('ojo',154,'neutral'),'不良':('mob-male-broad',182,'brown'),'生徒':('mob-male-slim',173,'brown')})
PLANS={}
PLANS[7]=[
 (scene('学生寮／三人の部屋・朝','dorm-morning',D),[]),
 (scene('保健室／朝の見舞い','infirmary-day',cg='episode06-a-r3'),[
  cue('プラスも立ち上がった。',cast=D,cg=None),
  cue('窓の外では、同じようなローブを着た生徒たちが、',location='学園／教室への道',bg='campus',cut=True)]),
 (scene('校舎／午前の授業','classroom',D),[
  cue('午前の授業が終わると、',location='学園／食事と委員会への移動',bg='cafeteria',cut=True),
  cue('通路には、対戦の申し込みをする生徒が並んでいた。',location='決闘委員会／契約相談窓口',bg='arena-reception',cut=True)]),
 (scene('保健室／契約変更案の確認','infirmary-day',cg='episode06-c'),[]),
 (scene('学園／午後の中庭','courtyard',D),[
  cue('ヒカルは、二人が声をかけるより先に気づいた。',cast=['プラス','ヒカル','ランス']),
  cue('プラスはランスと中庭を出た。',cast=D)]),
 (scene('決闘委員会／承認と準備','arena-reception',D),[
  cue('準備のための時間に、二人は空いた場所へ入った。',location='闘技場／選手控え区画',cut=True),
  cue('プラスは左手で受け取った。',cg='episode07-sword-ready'),
  cue('通路の方に、ユージが現れた。',cast=T,cg=None),
  cue('ランスとユージが、客席へ向かう。',cast=['プラス'])]),
 (scene('闘技場／武器あり競技面','arena-floor',['プラス','ヒカル']),[
  cue('プラスは剣を立てた。',cg='episode07-sword-ready'),
  cue('審判のサニーが、二人の間に立つ。',cast=['プラス','ヒカル','サニー']),
  cue('サニーが二人を離れさせる。',cast=['プラス','ヒカル']),
  cue('左腕を前へ運び、投げた。',cg=None)]),
 (scene('闘技場／ヒカルの鞭','arena-floor',['プラス','ヒカル'],cg='episode07-a-r3'),[
  cue('サニー「プラス、続けられる？」',cg=None,cast=['プラス','ヒカル','サニー']),
  cue('床を押して立つ。',cast=['プラス','ヒカル'],cg='episode07-a-r3')]),
 (scene('闘技場／観客席','arena',['ランス','ユージ']),[
  cue('プラスの左拳が、また外れた。',location='闘技場／競技面・腕の変化',bg='arena-floor',cast=['プラス','ヒカル'],cg='episode07-a-r3',cut=True)]),
 (scene('闘技場／左腕の軽量化','arena-floor',['プラス','ヒカル'],cg='episode07-a-r3'),[]),
 (scene('闘技場／決着への一歩','arena-floor',['プラス','ヒカル'],cg='episode07-a-r3'),[
  cue('届く瞬間、左拳を重くした。',cg='episode07-left-impact'),
  cue('ヒカルが後ろへ二歩下がり、片膝をついた。',cg=None),
  cue('サニー「止め！」',cast=['プラス','ヒカル','サニー'])]),
 (scene('闘技場／観客席・決着後','arena',['ランス','ユージ']),[
  cue('通路へ向かう。',location='闘技場／競技面への通路',bg='arena-reception',cut=True),
  cue('プラスがいる。',location='闘技場／決着後の競技面',bg='arena-floor',cast=T,cut=True),
  cue('ランスがプラスの横へしゃがんだ。',cg='episode07-b-r3')]),
 (scene('闘技場／処置と契約確認','arena-reception',T),[
  cue('そのあと、契約変更の確認が行われた。',cg='episode07-c'),
  cue('ヒカルは、処置を終えてからも不機嫌だった。',cast=['プラス','ユージ','ヒカル'],cg=None),
  cue('ヒカルが去ったあと、',cast=T)]),
 (scene('闘技場／出口への通路','arena-reception',T),[]),
 (scene('闘技場／客席の二人','arena',cast=[],cg='episode07-d'),[])
]
PLANS[8]=[
 (scene('保健室／治療完了の確認','infirmary-day',P),[]),
 (scene('学園／朝の通学路','campus',P),[
  cue('教室では、先に来ていたランスが二人を見た。',location='校舎／教室',bg='classroom',cast=T,cut=True)]),
 (scene('校舎脇／昼の休憩場所','courtyard',['プラス']),[
  cue('その片方に、コンケが座っていた。',cast=['プラス','コンケ']),
  cue('コンケは何も言わず、そのまま校舎の角を曲がった。',cast=['プラス'])]),
 (scene('学園／食堂','cafeteria',P,cg='episode08-c'),[]),
 (scene('新聞部／編集部前','corridor',['プラス']),[
  cue('中へ入ると、',location='新聞部／夕陽新聞編集部',bg='newsroom',cast=NEWS,cut=True)]),
 (scene('新聞部／決闘のインタビュー','newsroom',NEWS,cg='episode08-d'),[]),
 (scene('新聞部／グモンの過去の記事','newsroom',NEWS),[]),
 (scene('新聞部／最近の不良サークル','newsroom',NEWS),[]),
 (scene('新聞部／退出','newsroom',['プラス']),[
  cue('廊下へ出ると、ユージがいた。',location='校舎／新聞部前の廊下',bg='corridor',cast=P,cut=True),
  cue('歩きながら、プラスは新聞部の話を伝えた。',location='学園／中央購買への道',bg='campus',cut=True)]),
 (scene('中央購買／パンを奪うコンケ','shop',P),[
  cue('コンケがいた。',cast=['プラス','ユージ','コンケ']),
  cue('袋が、コンケの手へ移った。',cg='episode08-bread-theft'),
  cue('取り巻きはついていかなかった。',cg=None,cast=P)]),
 (scene('学園／コンケを追う道','campus',P),[
  cue('道の先に、旧校舎が現れた。',location='不良サークル／旧校舎の外',bg='old-school-exterior',cut=True)]),
 (scene('旧校舎／脇の出入口','old-school-exterior',P),[
  cue('二人は中へ入った。',location='旧校舎／廊下',bg='old-school-corridor',cut=True)]),
 (scene('旧校舎／階段と上階の廊下','old-school-corridor',P),[
  cue('廊下の先には、少し大きな扉があった。',location='旧校舎／部長室前',cut=True),
  cue('大きな身体があった。',cg='episode08-e'),
  cue('オーガ「……お前ら、何してる」',cast=['プラス','ユージ','オーガ'])])
]
PLANS[9]=[
 (scene('旧校舎／部長室前','old-school-corridor',['コンケ']),[
  cue('コンケは扉を開け、少し頭を下げて中へ入った。',location='旧校舎／グモンの部長室',bg='gumon-office',cast=['コンケ','グモン'],cut=True),
  cue('パンを出す。',cg='episode09-c')]),
 (scene('旧校舎／グモンを思うコンケ','gumon-office',cg='episode09-c'),[]),
 (scene('回想／コンケが変わる前','corridor',['コンケ']),[
  cue('ユージとランスが騒いでいると、',location='回想／以前の学生寮',bg='dorm',cast=['コンケ','ユージ','ランス'],cut=True),
  cue('最初に呼び止められたときも、',location='回想／学園の通路',bg='corridor',cast=['コンケ','不良'],cut=True),
  cue('ローブの胸元をつかまれた。',expressions={'konke_hurt':True}),
  cue('グモン「……邪魔だ」',cast=['コンケ','不良','グモン']),
  cue('ありがとうと言うより先に、角の向こうへ消えた。',cast=['コンケ'])]),
 (scene('回想／不良サークルに入った頃','old-school-corridor',['コンケ','不良']),[
  cue('夜、寮へ戻ると、',location='回想／学生寮',bg='dorm-night',cast=['コンケ','ユージ'],cut=True),
  cue('初めて勝ったケンカは、',location='回想／不良サークル・最初の反抗',bg='old-school-corridor',cast=['コンケ','不良'],cut=True),
  cue('それを見たとき、コンケは口元を抑えられなかった。',expressions={'konke_confident':True})]),
 (scene('回想／勝者として増える星','arena-floor',['コンケ']),[
  cue('住む場所も変わった。',location='回想／グレードが上がった寮',bg='dorm',cut=True),
  cue('前なら避けていた相手へ、',location='回想／学園の道',bg='campus',cast=['コンケ','生徒'],cut=True),
  cue('プラスには、負けた。',location='回想／プラスとの夜の練習',bg='training-night',cast=['コンケ','プラス'],cut=True)]),
 (scene('旧校舎／現在の部長室','gumon-office',cg='episode09-c'),[]),
 (scene('旧校舎／部長室前の廊下','old-school-corridor',['プラス','ユージ','オーガ']),[
  cue('オーガは、横の教室へ顎を向けた。',location='旧校舎／オーガの談話室',bg='clubroom',cut=True)]),
 (scene('旧校舎／色とりどりの紅茶','clubroom',cg='episode09-a'),[]),
 (scene('旧校舎／グモンへの相談','clubroom',cg='episode09-a'),[
  cue('オーガが、立ち上がった。',cast=['プラス','ユージ','オーガ'],cg=None)]),
 (scene('旧校舎／談話室の騒ぎ','clubroom',['プラス','ユージ','オーガ']),[
  cue('短い金髪が見えた。',cast=['プラス','ユージ','ヒカル']),
  cue('その前へ、オーガが立った。',cast=['ヒカル','オーガ']),
  cue('オーガの手が、鞭の柄へ伸びた。',cg='episode09-b-faceless'),
  cue('争いが、廊下へ移った。',location='旧校舎／談話室前の廊下',bg='old-school-corridor',cut=True)]),
 (scene('旧校舎／談話室・机の陰','clubroom',P),[
  cue('プラスは立った。',cast=['プラス']),
  cue('入口へ向かう。',location='旧校舎／部長室への廊下',bg='old-school-corridor',cut=True)]),
 (scene('旧校舎／グモンの部長室','gumon-office',cg='episode09-c'),[
  cue('グモン「何だ、あいつら」',cg=None,cast=['グモン','コンケ']),
  cue('プラスが顔を出した。',cast=['プラス','コンケ','グモン'])])
]

PLANS[10]=[
 (scene('旧校舎／部長室・突然の攻撃','gumon-office',['プラス','コンケ']),[]),
 (scene('旧校舎／話すための拳','gumon-office',['プラス','コンケ']),[
  cue('プラス「ちゃんと、相手する」',cg='episode10-a')]),
 (scene('旧校舎／毒と拳の応酬','gumon-office',['プラス','コンケ'],cg='episode10-a'),[]),
 (scene('旧校舎／見守るグモン','gumon-office',['グモン']),[
  cue('プラス「コンケ。お前、なんでここに入ったんだ」',cast=['プラス','コンケ','グモン'])]),
 (scene('旧校舎／コンケが憧れた強さ','gumon-office',['プラス','コンケ']),[]),
 (scene('旧校舎／割れた鏡','gumon-office',['プラス','コンケ']),[
  cue('そこに、男が映っていた。',cg='episode10-konke-mirror'),
  cue('コンケは、顔を背けた。',cg=None),
  cue('グモン「……おい」',cast=['プラス','コンケ','グモン'])]),
 (scene('旧校舎／スリングショット・パンチ','gumon-office',['プラス','コンケ']),[
  cue('プラス「——スリングショット、パンチ！」',cg='episode10-a'),
  cue('三歩目で膝が折れ、棚の前へ倒れた。',cg=None,cast=['プラス'])]),
 (scene('旧校舎／立ち上がるグモン','gumon-office',['プラス','グモン']),[
  cue('扉へ向かう。',cast=['プラス']),
  cue('少しだけ足をずらし、扉を開けた。',cast=['プラス'])]),
 (scene('旧校舎／廊下の争い','old-school-corridor',['ヒカル','オーガ'],cg='episode09-b-faceless'),[
  cue('グモン「てめえら、俺の部室の前で何やってんだ！」',cast=['グモン','ヒカル','オーガ'],cg=None),
  cue('机の陰から、ユージが顔を上げた。',location='旧校舎／談話室・ユージのもと',bg='clubroom',cast=['ユージ','グモン','ヒカル'],cut=True),
  cue('身体が、持ち上がった。',cast=['ヒカル','ユージ'],cg='episode10-yuji-carry'),
  cue('ヒカルは、廊下を歩き出した。',location='旧校舎／出口への廊下',bg='old-school-corridor',cut=True),
  cue('扉の向こうへ、二人の姿が消えた。',cast=['グモン','オーガ'],cg=None)]),
 (scene('旧校舎／負けた二人の手','gumon-office',['プラス']),[
  cue('隣で、コンケが目を開けた。',cast=['プラス','コンケ']),
  cue('外から、オーガが戻ってきた。',cast=['プラス','コンケ','オーガ']),
  cue('その後ろに、グモンがいた。',cast=['プラス','コンケ','オーガ','グモン'])]),
 (scene('旧校舎／入口の外','old-school-exterior',['ユージ','ヒカル']),[
  cue('ヒカルの靴音が、遠ざかった。',cast=['ユージ']),
  cue('プラスは、コンケと並んで座っていた。',location='旧校舎／救護を待つ部長室',bg='gumon-office',cast=['プラス','コンケ','ユージ','オーガ','グモン'],cut=True)]),
 (scene('数日後／学園の中庭','courtyard',['プラス']),[
  cue('ランス「なんで、あそこで名前まで叫べたんだよ」',location='回想／朝の能力練習場',bg='training',cast=['プラス','ランス','ユージ'],cut=True),
  cue('プラスは、思い出して少し笑った。',location='学園／昼の中庭',bg='courtyard',cast=['プラス'],cut=True),
  cue('グモン「貸した奴の名前、言ってみろ」',cast=['プラス','グモン','不良の男子']),
  cue('その横に、コンケがいた。',cast=['プラス','グモン','コンケ']),
  cue('グモンは、二人の顔を見比べた。',cast=['プラス','コンケ']),
  cue('コンケは、今度こそ前を向いた。',cast=['プラス'])]),
 (scene('中庭／大きな木の下','courtyard-tree',['グモン','コンケ']),[
  cue('コンケは、硬貨を握った。',cast=['グモン']),
  cue('マイナスは、隣の木陰へゆっくり腰を下ろした。',cg='episode10-tree-faceless')])
]


def compile_episode(n,body,title):
 parts=body.split('　　　　　＊');assert len(parts)==len(PLANS[n]);entries=[];reports=[]
 for sn,(part,(initial,cues)) in enumerate(zip(parts,PLANS[n]),1):
  st=dict(initial);expr={};camera=st['cast'][:3];seen=set();start=len(entries)
  def portrait(name):
   emotion=expr.get(name,c.CHAR[name][2])
   if name=='プラス':
    if n==7:return {'smile':'bandaged-smile','surprised':'bandaged-surprised','serious':'bandaged-serious'}.get(emotion,'bandaged')
    if n==9 and sn>=10:return 'serious'
   if name=='コンケ':
    if n==9 and sn==3:return 'hurt' if expr.get('konke_hurt') else 'reserved'
    if n==9 and sn==4 and not expr.get('konke_confident'):return 'reserved'
    if (n==8 and sn==3) or (n==9 and sn==12) or (n==10 and sn<=6):return 'reserved'
    if n==10 and sn in [7,10,11]:return 'hurt'
   if name=='プラス' and n==10 and sn<=11:return 'pain' if sn!=1 else 'serious'
   return emotion
  def state():return dict(scene=sn,location=st['location'],bg=st['bg'],tone=st['tone'],cg=st['cg'],cgAlt='物語の挿絵',cast=[dict(id=c.CHAR[name][0],name=name,height=c.CHAR[name][1],expression=portrait(name)) for name in camera])
  def loc():
   data=state();data['cast']=[];entries.append(dict(type='location',**data))
  if not entries or entries[-1]['location']!=st['location'] or entries[-1]['bg']!=st['bg']:loc()
  for raw in part.splitlines():
   line=raw.strip()
   if not line:continue
   matches=[]
   for ci,q in enumerate(cues):
    at=line.find(q['match'])
    if at>=0:
     assert ci not in seen,(n,sn,q['match']);seen.add(ci);matches.append((at,ci,q))
   positions=sorted(set([0]+[at for at,_,_ in matches]+[len(line)]));raw_pending=True
   for a,b in zip(positions,positions[1:]):
    for at,ci,q in matches:
     if at!=a:continue
     for key in ['location','bg','tone','cast','cg']:
      if key in q:st[key]=q[key]
     if 'cast' in q:camera=st['cast'][:3]
     expr.update(q.get('expressions',{}))
     if q['cut']:loc()
    segment=line[a:b];m=re.match(r'^([^「『]{1,16})([「『].*)$',segment);name=m.group(1) if m and (m.group(1) in c.CHAR or m.group(1) in ['担当者','保健委員','先生']) else '';text=m.group(2) if name else segment
    if name in st['cast'] and name not in camera:
     keep=[x for x in camera if x not in ['プラス',name]];camera=(['プラス'] if 'プラス' in st['cast'] else [])+keep[-1:]+[name]
    if name in c.CHAR:
     emotion=c.default_expression(name,text)
     if n==7 and name=='プラス' and sn in [3,5,6,7,8,9,10,11]:emotion='serious'
     expr[name]=emotion
    for chunk in c.chunks(text):
     entries.append(dict(type='line',speaker=name,character=c.CHAR.get(name,(None,))[0],text=chunk,raw=line if raw_pending else '',effect=segment in ['音がした。','鞭が床を打つ。','横腹へ蹴りが入った。'],**state()));raw_pending=False
  assert len(seen)==len(cues),(n,sn,'unmatched',[q['match'] for i,q in enumerate(cues) if i not in seen])
  reports.append(dict(scene=sn,start=start,end=len(entries)-1,location=initial['location'],source_lines=len([l for l in part.splitlines() if l.strip()]),reviewed=False))
 data=dict(id=f'chapter1-episode{n}',title=title,entries=entries,source_lines=sum(bool(l.strip()) and l.strip()!='＊' for l in body.splitlines()),source_scenes=len(parts),source_hash=hashlib.sha256(body.encode()).hexdigest());(ROOT/'data'/f'chapter1-episode{n}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return reports

def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('episodes',nargs='*',type=int);args=parser.parse_args();ns=args.episodes or sorted(PLANS)
 source_path=ROOT.parent/'source-current.json'
 titles={7:'その笑顔は、誰のもの',8:'ちょっと様子を、見に来ただけ',9:'あの人の前では、格好つけたい',10:'放っておけと、言われても'}
 source=json.loads(source_path.read_text()) if source_path.exists() else {'chapters':[{'id':f'chapter1-episode{n}','title':f'第1章　第{n}話　{titles[n]}','body':(ROOT/f'data/source/chapter1-episode{n}.txt').read_text()} for n in ns]}
 manifest=json.loads((ROOT/'data/episodes.json').read_text());review=json.loads((ROOT/'data/chapter1-scene-review.json').read_text())
 desc={7:'友達が断れる明日のために。プラスは星七つと契約変更を賭け、ヒカルへ挑む。',8:'治療を終えた朝、コンケの知らない顔を見つける。新聞部への取材と旧校舎への尾行。',9:'コンケが憧れた背中。色とりどりの紅茶の席に、ヒカルが現れる。',10:'割れた鏡に映る顔。コンケとの殴り合いの先で、グモンが部屋を出る。'}
 images={7:'episode07-a-r3',8:'episode08-d',9:'episode09-a',10:'episode10-tree-faceless'}
 for n in ns:
  id=f'chapter1-episode{n}';ch=next(ch for ch in source['chapters'] if ch['id']==id);report=compile_episode(n,ch['body'],ch['title']);review['episodes'][id]=report;manifest['episodes']=[ep for ep in manifest['episodes'] if ep['id']!=id];manifest['episodes'].append(dict(id=id,title=ch['title'],file=f'data/{id}.json',image=c.CG(images[n]),description=desc[n]));print(id,len(report),'scenes')
 manifest['episodes'].sort(key=lambda ep:0 if ep['id']=='prologue' else int(ep['id'].split('episode')[-1]));(ROOT/'data/episodes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(ROOT/'data/chapter1-scene-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
