"""Compile subsequent episodes with paragraph-internal staging cues and exact prose coverage."""
import json,re,hashlib
from pathlib import Path
import compile_chapter1 as c
ROOT=Path(__file__).resolve().parents[1]
scene,cue=c.scene,c.cue
D=['プラス','ランス'];P=['プラス','ユージ'];T=c.TRIO;NEWS=['プラス','ユーヒ','バルー','チック','モルペウス','ダイ']
c.CHAR.update({'コバル':('kobal',176,'neutral'),'オーガ':('oga',197,'neutral'),'グモン':('gumon',189,'neutral'),'ヤオイ':('yaoi',155,'neutral'),'オジョー':('ojo',154,'neutral'),'不良':('mob-male-broad',182,'brown'),'生徒':('mob-male-slim',173,'brown')})
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


PLANS[11]=[
 (scene('学生寮／いつもの朝','dorm-morning',T,cg='episode11-d'),[]),
 (scene('早朝の練習場／軽い脚の制御','training',D),[]),
 (scene('早朝の練習場／能力と想像','training',D),[]),
 (scene('早朝の練習場／身体が覚える動き','training',D),[]),
 (scene('学生寮／今日の衣装選び','dorm-morning',T),[
  cue('朝飯を済ませ、三人で寮を出た。',location='学園／三人の通学路',bg='campus',cut=True)]),
 (scene('校舎／戻ってきたクラスメイト','classroom',['プラス','ユージ','コンケ']),[
  cue('ランスは、自分の席へ向かいながら一度だけコンケを見た。',cast=['プラス','ランス','コンケ']),
  cue('プラスは、近くへ行った。',cast=['プラス','コンケ']),
  cue('プラスは、自分の席へ戻った。',cg='episode11-a')]),
 (scene('校舎／頭の修行','classroom',P),[
  cue('少し後ろで、教材が捲られた。',cast=['プラス','ユージ','コンケ']),
  cue('休憩の合間に、プラスは教師へ近づいた。',cast=['プラス','ランス'])]),
 (scene('校舎／四人で昼食へ','classroom',['プラス','ランス','ユージ','コンケ']),[
  cue('廊下を歩いている間、誰も昔の寮の話をしなかった。',location='校舎／食堂への廊下',bg='corridor',cut=True)]),
 (scene('食堂／四つ並んだ青いスープ','cafeteria',['プラス','ユージ','ランス','コンケ']),[
  cue('四人は、空いていた長い席へ並んだ。',cg='episode11-e-blue-soup')]),
 (scene('食堂／それぞれの午後','cafeteria',cg='episode11-e-blue-soup'),[
  cue('器を返し、四人で食堂を出た。',location='学園／食堂前の分かれ道',bg='campus',cast=['プラス','ユージ','ランス','コンケ'],cg=None,cut=True)]),
 (scene('オタクサークル／上映の準備','club-corridor',['ランス']),[
  cue('部屋では、上映の準備が進んでいた。',location='オタクサークル／上映前の部室',bg='clubroom',cut=True),
  cue('照明が落ちた。',tone='night')]),
 (scene('オタクサークル／見逃した台詞','clubroom',['ランス'],tone='night'),[
  cue('終わりの音楽が流れると、',tone='')]),
 (scene('オタクサークル／受け取る人の言葉','clubroom',['ランス']),[]),
 (scene('オタクサークル／撮影と感想会','clubroom',['ランス']),[
  cue('立つ場所が空けられた。',cg='episode11-b')]),
 (scene('オタクサークル／片づけの時間','clubroom',['ランス'],cg='episode11-c'),[
  cue('戻ってきても、ランスはその声を思い返していた。',cg='episode11-quiet-talk-kobal-v2')])
]


PLANS[12]=[
 (scene('オタクサークル／片づけの後','clubroom',['ランス','コバル'],cg='episode11-quiet-talk-kobal-v2'),[
  cue('ランスの掌に、硬い感触が生まれた。',cg=None)]),
 (scene('離れ校舎／夕方の入口','campus',['ランス','ゆきめろ'],cg='episode12-outside-corrected'),[]),
 (scene('決闘委員会／星二十個と契約','arena-reception',['ランス','コバル'],cg='episode12-c-v2'),[]),
 (scene('中央購買／ランスの名前','shop',['プラス']),[
  cue('ユージを探すと、',location='コスプレサークル／準備場所の前',bg='courtyard',cast=P,cut=True),
  cue('闘技場へ向かう途中、コンケも追いついた。',location='学園／闘技場への道',bg='campus',cast=['プラス','ユージ','コンケ'],cut=True)]),
 (scene('闘技場／部員たちの観客席','arena',['プラス','ユージ','コンケ']),[
  cue('中央に立ったのは、サニーだった。',location='闘技場／武器なし競技面',bg='arena-floor',cast=['ランス','コバル','サニー'],cut=True)]),
 (scene('闘技場／金属生成とチャージパンチ','arena-floor',['ランス','コバル'],cg='episode12-a'),[]),
 (scene('闘技場／拳を溜める間にも','arena-floor',['ランス','コバル'],cg='episode12-a'),[]),
 (scene('闘技場／砂の下へ残したもの','arena-floor',['ランス','コバル'],cg='episode12-a'),[
  cue('掌を床へつく。',cg='episode12-low-guard')]),
 (scene('闘技場／最後の返事を待つ間','arena',['プラス','ユージ','コンケ']),[
  cue('ランスは、また退いた。',location='闘技場／競技面・仕掛けの決着',bg='arena-floor',cast=['ランス','コバル'],cut=True),
  cue('コバルの足元で、銀色が跳ねた。',cg='episode12-folded-spear'),
  cue('サニーが、二人の間へ入った。',cast=['ランス','コバル','サニー'],cg=None)]),
 (scene('闘技場／勝者の向こうへ','arena',['プラス','ユージ','コンケ']),[
  cue('三人は、通路へ向かった。',location='闘技場／選手退場口',bg='arena-reception',cut=True),
  cue('ランスは、肩へ布を当てられながら出てきた。',cast=T,expressions={'lance_treated':True}),
  cue('ゆきめろが、入口の前にいた。',cast=['プラス','ランス','ゆきめろ']),
  cue('ゆきめろが、そのそばへ膝をつく。',cg='episode12-aftermath-corrected')])
]
PLANS[13]=[
 (scene('闘技場／治療へ向かう担架','arena-reception',cg='episode12-aftermath-corrected'),[
  cue('それが通路の角へ消えると、',cast=T,cg=None)]),
 (scene('決闘委員会／返ってくる星','arena-reception',['プラス','ユージ','コンケ']),[
  cue('ランスが、窓口から出てきた。',cast=T),
  cue('保健委員会の処置室へ繋がる廊下を、歩き始める。',location='保健委員会／処置室への廊下',bg='corridor',cut=True)]),
 (scene('保健委員会／処置室の外','corridor',['プラス','ランス','ゆきめろ']),[
  cue('ゆきめろは、目を下げた。',cg=None)]),
 (scene('保健委員会／もう戦わないで','corridor',['プラス','ランス','ゆきめろ']),[
  cue('手帳をポケットへ押し込み、廊下を歩き出す。',cast=T,cg=None)]),
 (scene('学園／夕方の帰り道','campus',T,tone='evening'),[
  cue('胸元を掴む前に、ランスの掌から小さな金属板が生まれた。',cg='episode13-hand-deflection-v4'),
  cue('プラスは、靴で土を削って止まった。',cg=None),
  cue('ユージが、間へ入った。',cg=None),
  cue('最後に、寮の方へ足を向けた。',cg='episode13-c')]),
 (scene('学園／寮までの長い道','campus',T,cg='episode13-c'),[
  cue('部屋へ戻ると、',location='学生寮／肩の布と夕食',bg='dorm',cg=None,cut=True),
  cue('部屋へ戻り、灯りを落とした。',location='学生寮／眠れない夜',bg='dorm-night',cast=['プラス'],cut=True)]),
 (scene('学生寮／夜の書き置き','dorm-night',P),[
  cue('二人は、部屋を出た。',location='学生寮／夜の出入口',bg='campus-night',cut=True)]),
 (scene('能力練習場／月明かりの端の区画','training-night',P),[]),
 (scene('能力練習場／斜めの盾','training-night',P,cg='episode13-b'),[]),
 (scene('能力練習場／質量を操るという言葉','training-night',P),[]),
 (scene('能力練習場／盾を持ちにくくする','training-night',P,cg='episode13-b'),[]),
 (scene('能力練習場／次は目の前に残る','training-night',P),[
  cue('プラスは、月明かりの下で、もう一度踏み込んだ。',cg='episode13-b')])
]
PLANS[14]=[
 (scene('学生寮／まだ少ない言葉','dorm-morning',T),[
  cue('学校へ向かった。',location='学園／朝の通学路',bg='campus',cut=True),
  cue('教室ではコンケが、',location='校舎／午前の教室',bg='classroom',cast=['プラス','ランス','ユージ','コンケ'],cut=True)]),
 (scene('オタクサークル／好きな作品の話','clubroom',['プラス','コバル'],cg='episode14-d'),[]),
 (scene('オタクサークル／部長が守りたかったもの','clubroom',['プラス','コバル'],cg='episode14-d'),[]),
 (scene('オタクサークル／見届けたい人','clubroom',['プラス','コバル'],cg='episode14-d'),[
  cue('プラスが部室を出ると、',location='離れ校舎／部室前の廊下',bg='club-corridor',cast=['プラス','ゆきめろ'],cg='episode14-e',cut=True),
  cue('扉が開き、コバルが廊下へ出てくる。',cast=['プラス','ゆきめろ','コバル'],cg=None)]),
 (scene('保健委員会／全回復の確認','infirmary',['プラス','ユージ']),[
  cue('手首を回し、指を曲げる。',cast=T),
  cue('帰り道、ランスがポケットへ手を入れた。',location='学園／練習場への夜道',bg='campus-night',cut=True),
  cue('グレード1の寮の裏へ回る。',location='能力練習場／星の動かない勝負',bg='training-night',cut=True),
  cue('コンケは、練習場の柵へ寄りかかっていた。',cast=['プラス','ランス','コンケ']),
  cue('ユージは、二人を中央へ呼んだ。',cast=T),
  cue('ユージは、二人から離れた。',cast=D)]),
 (scene('能力練習場／いつもより速い槍','training-night',D,cg='episode14-spar-proportions-v3'),[]),
 (scene('能力練習場／軽くしても残る形','training-night',D,cg='episode14-spar-proportions-v3'),[]),
 (scene('能力練習場／身体を軽くする','training-night',D,cg='episode14-spar-proportions-v3'),[
  cue('足が、床から離れた。',cg='episode14-light-evasion-proportions-v4'),
  cue('右手に、今度は長い槍が作られた。',cg='episode14-spar-proportions-v3')]),
 (scene('能力練習場／見届ける四人','training-night',['ユージ','ゆきめろ','コバル','コンケ']),[]),
 (scene('能力練習場／もう一手、その先へ','training-night',D,cg='episode14-spar-proportions-v3'),[
  cue('プラスは落とす方向へ腕を回し、背中を床へ押さえた。',cg='episode14-ground-control-r2'),
  cue('プラスは、すぐに手を離した。',cg=None,cast=T)]),
 (scene('能力練習場／今夜は話せなくても','training-night',T),[
  cue('夜間受付までは、六人で歩いた。',location='学園／夜間受付への道',bg='campus-night',cut=True),
  cue('治療を終え、寮へ帰ってからも、',location='学生寮／翌朝の目覚まし',bg='dorm-night',cut=True)]),
 (scene('校舎／昨日の続きが話したい','classroom',T),[
  cue('サークル活動が終わったあと、六人は昨日の練習場に集まった。',location='能力練習場／役に立たなくても帰る部屋',bg='training-night',cast=T,cut=True)]),
 (scene('能力練習場／一個ずつ話す','training-night',['プラス','ランス','ゆきめろ','コバル','ユージ','コンケ']),[
  cue('ゆきめろは、しゃがんだ。',cg='episode14-talk-kobal-v3')]),
 (scene('学園／まだ痛くても一緒に歩く','campus-night',T),[]),
 (scene('オタクサークル／同じ机で違う感想','clubroom',['ランス','ゆきめろ','コバル']),[]),
 (scene('学生寮／同じ部屋の明かり','dorm-night',T),[
  cue('教材を閉じ、三人で画面の前へ座った。',cg='episode14-b-v2')])
]


PLANS[15]=[
 (scene('食堂／わからないところの違い','cafeteria',T),[
  cue('向かいでコンケが笑った。',cast=['プラス','ランス','コンケ']),
  cue('ユージは汁物の椀を少しずらした。',cast=T),
  cue('プラスが顔を上げる。',cg='episode15-e'),
  cue('プラス「……その手があった」',cg=None,cast=T)]),
 (scene('校舎／役員会議へ急ぐX','corridor',['X'],cg='episode15-c'),[
  cue('扉を開けると、その声の主が窓を背に座っていた。',location='生徒会室／来月度の連絡',cast=[],cg='episode15-d-v5',cut=True),
  cue('X「最後に、例の転校生について」',location='生徒会室／転校生の到着確認'),
  cue('Xは、返事の代わりに軽く会釈した。',location='生徒会室／残った申請書',cast=['X'],cg=None)]),
 (scene('勉強サークル／再訪','club-corridor',D),[
  cue('ドーマ「こんにちは プラスさん ランスさん」',cast=['プラス','ランス','ドーマ']),
  cue('机の間を歩くと、焼いた甘い匂いがした。',location='勉強サークル／手作りのフィナンシェ',bg='library',cast=['プラス','ランス','ルサイ'],cut=True),
  cue('そのあとで、四人の前へ紙が広がった。',location='勉強サークル／途中の線から',cast=['プラス','ランス','ツクリ'],cg='episode15-a',cut=True)]),
 (scene('勉強サークル／戻ってきた部長','library',['プラス','ランス','X']),[
  cue('ルサイが飲み物を持ってきた。',cast=['プラス','X','ルサイ']),
  cue('X「……おやつは？」',cg='episode15-empty-snacks'),
  cue('ルサイが、容器の蓋を閉じた。',cg=None),
  cue('ツクリが、新しい紙を二枚出した。',cast=['プラス','ランス','X'],cg=None),
  cue('扉へ向かうところで、ルサイが声をかけた。',cast=['プラス','ランス','ルサイ'])]),
 (scene('校舎／一個でも増えた答え','corridor',D,tone='evening'),[
  cue('歩いてきたコンケが、二人を見つけて足を緩める。',cast=['プラス','ランス','コンケ']),
  cue('そのころ、勉強サークルの部室では、',location='勉強サークル／空になった皿',bg='library',cast=['X','ルサイ'],tone='evening',cut=True)])
]
PLANS[16]=[
 (scene('学生寮／教わった線を残す朝','dorm-morning',T),[
  cue('学校へ向かう道で、コンケと合流した。',location='学園／次に聞く場所',bg='campus',cast=['プラス','ランス','コンケ'],cut=True)]),
 (scene('勉強サークル／互いに教え合う','club-corridor',D),[
  cue('返事を待ってから開ける。',location='勉強サークル／単位と工程',bg='library',cast=['プラス','ランス','ドーマ'],cut=True),
  cue('奥の席を離れたXが、二人の紙を見た。',cast=['プラス','ランス','X']),
  cue('次の問題では、ドーマが手を止めた。',cast=['プラス','ランス','ドーマ'])]),
 (scene('勉強サークル／菓子の数と古い名前','library',['プラス','X','ルサイ']),[
  cue('Xは立ち上がり、資料を持ってそちらへ移った。',cast=['X','ルサイ']),
  cue('プラス「……ルサイさんって、Xさんに、普通に言うんだな」',cast=['プラス','ランス','ツクリ']),
  cue('休憩を終える前に、ツクリが棚へ向かった。',location='勉強サークル／残されたノート',cast=['プラス','ツクリ','ドーマ']),
  cue('ツクリが一冊を引き出した。',cg='episode16-a')]),
 (scene('勉強サークル／答えないことと知らないこと','library',['プラス','ランス','X']),[
  cue('ルサイが、机のそばへ来た。',cast=['プラス','X','ルサイ']),
  cue('ランスが、自分の紙を少し寄せる。',cast=['プラス','ランス','ツクリ'],cg='episode16-a')]),
 (scene('勉強サークル／マイナスという名前','library',['プラス','ランス','ツクリ']),[
  cue('プラスはそちらへ向かった。',cast=['プラス','X']),
  cue('二人で箱を持ち上げる。',location='勉強サークル／箱の重さ',cast=['プラス','ルサイ','X'],cg='episode16-b'),
  cue('その瞬間、Xの耳から、部室の音が遠ざかった。',location='Xの記憶／声と暗い床',bg='old-school-corridor',cast=[],cg=None,tone='night',cut=True),
  cue('プラスが、こちらを見ている。',location='勉強サークル／その手を離せ',bg='library',cast=['プラス','X','ルサイ'],tone='',expressions={'x_shaken':True},cut=True),
  cue('底が机へ触れる。',cg=None),
  cue('プラスは、入口の方へ動きかけた。',cast=['プラス','ランス','X']),
  cue('ルサイはカップを布で持ち、紙のない場所へ移す。',cast=['プラス','X','ルサイ']),
  cue('ランスが扉を開ける。',cast=D,cg=None),
  cue('部室を出ると、廊下はいつもと同じだった。',location='校舎／指は同じように動く',bg='corridor',cast=D,tone='evening',cut=True)]),
 (scene('学園／何が起きたかを話す','campus',D,tone='evening'),[]),
 (scene('勉強サークル／戻っていた箱','library',['X','ルサイ'],tone='evening',cg='episode16-c'),[
  cue('ツクリは、入口へ向かいかけてから戻った。',cast=['X','ツクリ','ドーマ'],cg=None),
  cue('部室に残ったのは、Xとルサイだけになった。',cast=['X','ルサイ'],cg='episode16-c'),
  cue('ルサイが、扉を開けた。',location='校舎／その角まで一緒に',bg='corridor',cast=['X','ルサイ'],cg=None,tone='evening',cut=True)])
]
PLANS[17]=[
 (scene('夢／届かなかった手','old-school-corridor',tone='night'),[
  cue('目が開いた。',location='学生寮／二人ともここにいる',bg='dorm-night',cast=[],tone='',cut=True),
  cue('ユージ「……早えな」',cast=P),
  cue('ランスも、その声で起きた。',cast=T)]),
 (scene('寮裏の練習場／変えたあとの動き','training',T),[
  cue('先に来ていたコンケが手を上げた。',cast=['プラス','ランス','コンケ']),
  cue('プラスは金属片を持ち上げた。',cg='episode17-morning-practice'),
  cue('プラスは、金属片を元の質量へ戻して置いた。',cg=None,cast=T),
  cue('コンケが、持っていた用具をプラスへ渡す。',cast=['プラス','ランス','コンケ']),
  cue('ランスが位置を確かめ、ユージが正面へ用具を持つ。',cast=T)]),
 (scene('学園／それぞれの午後','campus',T),[
  cue('四人で同じ道を歩く時間が終わり、',cast=['プラス']),
  cue('勉強サークルの扉の前へ着くと、',location='勉強サークル／返事のない挨拶',bg='club-corridor',cut=True),
  cue('ツクリの声がしてから、開けた。',bg='library',cast=['プラス','ツクリ','X']),
  cue('プラス「Xさん、こんにちは」',cg='episode17-c'),
  cue('プラスは、ツクリの隣へ座った。',cast=['プラス','ツクリ','ドーマ'],cg=None)]),
 (scene('勉強サークル／言葉と確かめたいこと','library',['プラス','ツクリ','ドーマ']),[
  cue('厚い辞書と、分野ごとの用語集が並んでいる。',location='勉強サークル／慣性・密度・熱容量'),
  cue('ルサイが、席の横へ来た。',cast=['プラス','ルサイ']),
  cue('ルサイは立ち上がった。',cast=['プラス','ルサイ','X'])]),
 (scene('勉強サークル／今年加わった条件','library',['プラス','ツクリ','ドーマ']),[
  cue('二冊を重ね、Xの机へ向かった。',cast=['プラス','X']),
  cue('プラスは、隣の椅子へ座った。',cg='episode17-a')]),
 (scene('勉強サークル／条件を読む','library',['プラス','X'],cg='episode17-a'),[
  cue('プラス「……やっぱ、Xさん、優しいよな」',cg=None),
  cue('あの床が、戻ってきた。',location='Xの記憶／消えない声',bg='old-school-corridor',cast=[],tone='night',cut=True),
  cue('今の部室だった。',location='勉強サークル／そのために何を賭ける',bg='library',cast=['プラス','X'],tone='',expressions={'x_shaken':True},cut=True),
  cue('ルサイ「Xくん」',cast=['プラス','X','ルサイ'],cg='episode17-e'),
  cue('X「ならば、そのために何を賭ける？」',cg=None),
  cue('ルサイは、その間へ身体を入れた。',cg='episode17-b-r3'),
  cue('Xは、書かれた紙を持ち上げた。',cg=None,cast=['プラス','X','ルサイ']),
  cue('扉へ向かう。',cast=['プラス','ルサイ']),
  cue('ルサイ「……プラスくん。少し、お時間をいただけますか」',cast=['プラス','ルサイ'])])
]

from chapter1_finale_plans import PLANS as FINALE_PLANS, CHARACTERS as FINALE_CHARACTERS, SPEAKERS as FINALE_SPEAKERS, TITLES as FINALE_TITLES, DESCRIPTIONS as FINALE_DESCRIPTIONS, IMAGES as FINALE_IMAGES
PLANS.update(FINALE_PLANS)
c.CHAR.update(FINALE_CHARACTERS)

def compile_episode(n,body,title):
 parts=body.split('　　　　　＊');assert len(parts)==len(PLANS[n]);entries=[];reports=[]
 for sn,(part,(initial,cues)) in enumerate(zip(parts,PLANS[n]),1):
  st=dict(initial);expr={};camera=st['cast'][:3];seen=set();start=len(entries)
  def portrait(name):
   emotion=expr.get(name,c.CHAR[name][2])
   if name=='プラス' and n==18 and expr.get('plus_training_hurt') and not expr.get('plus_treated'):return 'battle-hurt'
   if name=='プラス' and n==18 and sn==9 and not expr.get('plus_treated'):return 'battle-hurt'
   if name=='プラス' and n==19 and (expr.get('plus_duel_hurt') or sn in [6,11]):return 'battle-hurt'
   if name in ['プラス','X'] and n==20 and sn>=5:return 'battle-hurt'
   if name=='X' and expr.get('x_shaken'):return 'shaken'
   if name=='ランス' and (n==13 or (n==14 and sn==1) or (n==12 and sn==10 and expr.get('lance_treated'))):return 'hurt'
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
    segment=line[a:b];m=re.match(r'^([^「『]{1,16})([「『].*)$',segment);name=m.group(1) if m and (m.group(1) in c.CHAR or m.group(1) in FINALE_SPEAKERS or m.group(1) in ['担当者','保健委員','先生','決闘委員','通りがかりの生徒','別の生徒','別の親衛隊員','医療係の生徒','部員の男子','タイタン','アシャラ','ベレー','タナカ','セレナ','ミュー','クラリーヌ','ツキチヨ','ジャッジ','回想の声','勉強サークルの男子']) else '';text=m.group(2) if name else segment
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
 titles={7:'その笑顔は、誰のもの',8:'ちょっと様子を、見に来ただけ',9:'あの人の前では、格好つけたい',10:'放っておけと、言われても',11:'好きなはずなのに、見ていない',12:'君のためなら、勝てばよかった',13:'欲しかったのは、それじゃない',14:'帰ってきたら、何を話そう',15:'簡単だって、言われても',16:'その話だけは、聞いてはいけない',17:'その続きを、聞かせてくれ'}
 titles.update(FINALE_TITLES)
 source=json.loads(source_path.read_text()) if source_path.exists() else {'chapters':[{'id':f'chapter1-episode{n}','title':f'第1章　第{n}話　{titles[n]}','body':(ROOT/f'data/source/chapter1-episode{n}.txt').read_text()} for n in ns]}
 manifest=json.loads((ROOT/'data/episodes.json').read_text());review=json.loads((ROOT/'data/chapter1-scene-review.json').read_text())
 desc={7:'友達が断れる明日のために。プラスは星七つと契約変更を賭け、ヒカルへ挑む。',8:'治療を終えた朝、コンケの知らない顔を見つける。新聞部への取材と旧校舎への尾行。',9:'コンケが憧れた背中。色とりどりの紅茶の席に、ヒカルが現れる。',10:'割れた鏡に映る顔。コンケとの殴り合いの先で、グモンが部屋を出る。',11:'四人で囲む青いスープ。それぞれの午後、ランスは見逃した言葉に向き合う。',12:'星二十個と居場所を賭けたランスの決闘。その勝利が、守りたかった人へ届くとは限らなかった。',13:'返ってきた星と、届かなかった言葉。月明かりの下でプラスとユージが次の一歩を考える。',14:'同室の友と、星の動かない勝負。勝ち負けの先で、帰る部屋の明かりを確かめる。',15:'試験のわからない一行から、勉強サークルへ。残された線と、なくなったおやつ。',16:'古いノートと星を失った人々。軽くした箱が、Xの記憶を揺らす。',17:'届かなかった夢の手と、変わる部室の熱。すべての星と、三つの情報を賭ける約束。'}
 images={7:'episode07-a-r3',8:'episode08-d',9:'episode09-a',10:'episode10-tree-faceless',11:'episode11-e-blue-soup',12:'episode12-a',13:'episode13-b',14:'episode14-b-v2',15:'episode15-a',16:'episode16-a',17:'episode17-b-r3'}
 desc.update(FINALE_DESCRIPTIONS);images.update(FINALE_IMAGES)
 for n in ns:
  id=f'chapter1-episode{n}';ch=next(ch for ch in source['chapters'] if ch['id']==id);report=compile_episode(n,ch['body'],ch['title']);review['episodes'][id]=report;manifest['episodes']=[ep for ep in manifest['episodes'] if ep['id']!=id];manifest['episodes'].append(dict(id=id,title=ch['title'],file=f'data/{id}.json',image=c.CG(images[n]),description=desc[n]));print(id,len(report),'scenes')
 manifest['episodes'].sort(key=lambda ep:0 if ep['id']=='prologue' else int(ep['id'].split('episode')[-1]));(ROOT/'data/episodes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(ROOT/'data/chapter1-scene-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 main()
 from enhance_battles_audio import enhance
 enhance()
