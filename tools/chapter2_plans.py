"""Reviewed scene locations for the complete second chapter. Short movements stay inline."""
# bg aliases keep authoring concise, but only Japanese labels reach the reader.
PLACES={
'A':('闘技場／競技場','arena-floor'),'R':('闘技場／受付・通路','arena-reception'),'S':('闘技場／観客席','arena'),
'C':('学園／通学路','campus'),'H':('校舎／廊下','corridor'),'L':('図書館／閲覧室','library'),
'O':('旧校舎／不良サークル','gumon-office'),'P':('地下牢／鉄格子の通路','ch2-prison'),
'T':('女帝の間／玉座の広間','ch2-throne'),'U':('地下／避難した部屋','ch2-shelter'),
'N':('新聞部／部室','newsroom'),'D':('学生寮／寮室','dorm'),'E':('学生寮／寮室・夜','dorm-night'),
'F':('裏山／夜の広場','ch2-forest'),'I':('保健委員会／病室','infirmary-day'),'J':('保健委員会／廊下','corridor'),
'G':('美術サークル／展示室','ch2-gallery'),'B':('美術サークル／裏の通路','old-school-corridor'),
'W':('美術サークル／アトリエ','ch2-atelier'),'Q':('生徒会／会議室','ch2-council'),
'K':('美食サークル／レストラン','ch2-restaurant'),'V':('建設委員会／作業場','ch2-construction'),
'Y':('中庭／祭典の準備','courtyard'),'Z':('寮裏／能力練習場','training-night'),
'M':('ミルクの寮／応接室','ch2-council'),'X':('校舎／夕暮れの休憩場所','courtyard-tree'),
'd':('裏山／排水路','ch2-forest'),'k':('カラオケ／五人の部屋','ch2-karaoke'),
'r':('学園／雨宿りの軒下','ch2-rain'), 'f':('裏山／昼の林','ch2-forest-day'),
}
# One letter per source scene; no prose is shortened or reordered.
SCENES={
1:'A R C O H r',
2:'Q Q Q Q H H H H H',
3:'C R P Z P P P',
4:'P P T T P P P U',
5:'U U U U U U U U U C',
6:'L C D E C F F F F',
7:'L C F F F F F F F',
8:'F F F F F F F F F F J C',
9:'C N N N H I I I I I I J',
10:'I J G H C K K K K K K K K K K',
11:'H H C C Q C C Q T T T T T T T T T T',
12:'K K K K K K K K H I I I I I I I I I I J C E E',
13:'J D C V C H H',
14:'G G G B W W C X',
15:'C V V B B B B B C O Y C H E',
16:'E V f d d V V d f d C I E V',
17:'V W W W W W C I J',
18:'J M M M M M M M',
19:'I I M E E Z C E E',
20:'D C Y Q S T A R A R A',
21:'A S A R R A S R R R A S S R S',
22:'A S R S S S R G R L A R R A',
23:'A S A S A X W W W W W A S A A S A A A S A R',
24:'R D M S R M W W I N I L C D k k k C T E L',
}
# Deliberate flashbacks, dreams and the following day retain a clear boundary.
MEMORIES={(3,4):'回想／寮裏の能力練習場',(7,1):'回想／同じ日の夕方・図書館',(11,5):'回想／生徒会長代理に決まった日',(16,6):'回想／建設委員会の作業場',(16,7):'回想／建設委員会の作業場',(19,9):'夢／幼い日の少女',(22,8):'回想／トリエが追った作品',(23,6):'回想／ベレーの生まれた街',(23,7):'回想／ベレーの過去',(23,8):'回想／ベレーの過去',(23,9):'回想／領主の屋敷',(23,10):'回想／ベレーの制作室',(23,11):'回想／ベレーの制作室',(24,2):'回想／決着前の学生寮',(24,21):'夢／自由サークルの部室'}
DESCRIPTIONS={
1:'昇格した日の午後、道に迷った少女と雨を待つ。',2:'創立記念日の告知。画面の向こうに、知っている顔がある。',3:'敗れた生徒を追い、プラスは地下の鉄格子へ辿り着く。',4:'助けるための手が届かない。仮面の人物と地下を走る。',5:'女帝と捕食の真実。知ってしまったあとで、何を選ぶのか。',6:'帰ってこない同居人を捜し、二人は夜の裏山へ。',7:'ユージが足を踏み入れた夜。遊びの続きへ、爆発が割り込む。',8:'友達へ伸ばした手を離さず、暗い森の戦いを終わらせる。',9:'自分たちが見た出来事と、新聞に載らないこと。',10:'美術の廊下を出た先で、温かい料理と新しい問いに出会う。',11:'笑顔を求められる皇女が、姉のいる地下へ降りる。',12:'食卓で聞いたことを持ち帰り、病室で話を合わせる。',13:'退院したランスの寄り道。祭典の準備と、展示への誘い。',14:'美しい展示の向こうに隠された、赤い木のある部屋。',15:'建設の仕事を手伝ったコンケが、見過ごせない声を聞く。',16:'六人分の手帳と、デヂが抱え込んでいた過去。',17:'いなくなったダンカチを捜し、アトリエの扉を押す。',18:'ミルクが差し出す協力と、自分で選ぶ決闘の条件。',19:'明日の約束を、狭い寮室と夜の練習場で重ねる。',20:'帝国創立記念日。華やかな舞台で、少女を送り出す。',21:'当たらない拳の理由を探し、仲間たちが星を確かめる。',22:'競技場と客席。それぞれの戦いは、まだ終わっていない。',23:'失われていく幸運と、誰にも見てもらえなかった作品。',24:'残った仕事を終え、五人で晴れた日の約束を果たす。'}
