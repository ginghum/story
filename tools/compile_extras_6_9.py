"""Compile extras 6–9 from preserved source, with exact illustration anchors.

Does not rebuild or alter existing episodes. Run from any directory.
"""
import json, re, hashlib
from pathlib import Path
from copy import deepcopy
from compile_chapter1 import chunks, CHAR

R = Path(__file__).resolve().parents[1]
SITE = 'https://ginghum.github.io/cursehighschool-/'
TITLES = {6:'先に行くなら、待っていて',7:'次のごはんも、君と',8:'笑っていれば、いいはずだった',9:'明日も来るなら、隣を空けて'}
DESC = {6:'ワンと、先で待っていてくれる仲間たち。',7:'食卓と帳簿の向こうに残る、カガチの過去。',8:'居場所を探すオリハと、思いがけない優しさ。',9:'気力を失ったデヂの隣に、毎日やってくるダンカチ。'}
# Each row gives background, location, physically present actors, BGM.
def row(bg, loc, cast, bgm='daily'):
    return (bg, loc, cast.split(), bgm)
W='ワン'; O='ルト バグ ワン'; F='ワン ヴァイン ルト'; K='カガチ ボンボリ ホオズキ'; D='デヂ ダンカチ'
PLANS = {
6:[row('arena-reception','闘技場／調査と勧誘','ワン ルト','calm'),row('arena-floor','闘技場／アシャラとの決闘','ワン アシャラ','battle'),row('infirmary','保健棟／病室','ワン ルト','reflection'),row('infirmary','保健棟／病室',O,'calm'),row('dorm','学生寮／退院のあと',W,'reflection'),row('clubroom','オカルト＆昆虫／入部',O,'calm'),row('ch2-forest','裏山／三人の活動',O),row('clubroom','オカルト＆昆虫／片づけ',O),row('clubroom','オカルト＆昆虫／新入部員','ワン バグ ヴァイン'),row('clubroom','オカルト＆昆虫／四人の机','ワン ヴァイン ルト'),row('ch2-forest','裏山／山道',F,'calm'),row('ch2-forest','裏山／休憩場所',F,'calm'),row('ch2-forest','裏山／次の坂',F,'calm'),row('ch2-forest','裏山／開けた場所',F),row('ch2-forest','裏山／帰り道',F,'calm'),row('clubroom','オカルト＆昆虫／次の活動','ワン ヴァイン','calm')],
7:[row('ch2-restaurant','美食サークル／事務机',K),row('ch2-restaurant','美食サークル／店の運営',K),row('ch2-restaurant','美食サークル／移転の相談',K,'calm'),row('ch2-restaurant','美食サークル／昼の片づけ',K),row('ch2-restaurant','美食サークル／有線電話','カガチ','tension'),row('ch2-memory-room','回想／生徒会長への襲撃','カガチ','tension'),row('ch2-memory-room','回想／崩れた石の陰','カガチ マイナス','underground'),row('ch2-memory-room','回想／逃げ延びたあと','カガチ','reflection'),row('ch2-restaurant','美食サークル／電話の続き','カガチ','calm'),row('ch2-restaurant','美食サークル／次の食事',K),row('ch2-restaurant','美食サークル／明日の仕込み',K)],
8:[row('arena-floor','闘技場／オリハの決闘','オリハ','battle'),row('classroom','教室／友達のできない理由','オリハ','reflection'),row('clubroom','オタクサークル／入部','オリハ ゆきめろ コバル'),row('clubroom','オタクサークル／衣装の話','オリハ ゆきめろ'),row('clubroom','オタクサークル／闇に堕ちた日','オリハ ゆきめろ コバル'),row('clubroom','オタクサークル／後輩のランス','オリハ コバル ランス'),row('clubroom','オタクサークル／好きな作品','オリハ ランス ゆきめろ','calm'),row('corridor','校舎／慣れない靴','オリハ','daily'),row('courtyard','校舎／柱の陰の腰掛け','オリハ ランス','calm'),row('courtyard','校舎／金属の杖','オリハ ランス ゆきめろ','calm'),row('clubroom','オタクサークル／隣の席','オリハ コバル ゆきめろ','calm')],
9:[row('ch2-construction','建設委員会／作業場',D,'reflection'),row('ch2-construction','建設委員会／低い椅子',D,'reflection'),row('ch2-construction','建設委員会／道具の順番',D,'calm'),row('ch2-construction','建設委員会／翌日の午後',D,'calm'),row('ch2-construction','建設委員会／爆発の音',D,'tension'),row('ch2-atelier','美術棟／崩れた通路','デヂ ベレー','tension'),row('ch2-atelier','美術棟／作業の準備',D,'reflection'),row('ch2-construction','美術棟／修復現場',D,'calm'),row('ch2-construction','美術棟／支柱の確認',D,'tension'),row('ch2-construction','美術棟／分かるまで待つ',D,'calm'),row('ch2-construction','美術棟／夜の作業灯',D,'reflection'),row('ch2-construction','美術棟／紙包みの食事',D,'calm'),row('ch2-construction','美術棟／台車の通る道',D,'calm'),row('ch2-construction','美術棟／復旧の確認','デヂ ベレー ダンカチ','calm'),row('ch2-construction','建設委員会／翌日の作業',D),row('ch2-construction','建設委員会／続く日々',D),row('ch2-construction','建設委員会／夕方の食事',D,'calm'),row('cafeteria','学園／食堂',D),row('ch2-construction','建設委員会／座れる椅子',D,'calm'),row('ch2-construction','建設委員会／任せる仕事',D,'calm'),row('ch2-construction','建設委員会／端材の課題',D),row('ch2-construction','建設委員会／ベレーの訪問','デヂ ベレー','tension'),row('ch2-construction','建設委員会／明日の図面',D,'calm'),row('ch2-construction','建設委員会／二つの椅子',D,'homecoming')]
}
MAJOR = {6:{1,2,3,5,6,7,8,9,11,16},7:{1,6,9},8:{1,2,3,4,5,6,8,11},9:{1,4,6,11,15,18,19,21,22,24}}
MOBS = {'審判':('mob-male-slim',175,'brown'),'対戦相手':('mob-male-broad',180,'brown'),'観客の生徒':('mob-male-slim',175,'brown'),'同級生':('mob-female-average',165,'brown'),'部員':('mob-male-slim',175,'brown'),'料理人の生徒':('mob-male-broad',178,'brown'),'東の店の部員':('mob-male-slim',175,'brown'),'襲撃した生徒':('mob-male-broad',180,'brown'),'建設委員':('mob-male-broad',180,'brown'),'通りかかった生徒':('mob-male-slim',175,'brown')}
def norm(s): return re.sub(r'\s+', '', s)
def main():
    chars = dict(CHAR)
    for c in json.loads((R/'data/chapter2-cast.json').read_text()):
        h=next((int(re.search(r'\d+',f['value'])[0]) for f in c['facts'] if f['label']=='身長'),175)
        chars[c['name']]=(c['id'],h,'neutral')
    chars.update(MOBS)
    chars['ホオズキ']=chars.get('ホオヅキ',('hoozuki',160,'neutral'))
    art=json.loads((R/'data/extra6-9-illustrations.json').read_text())
    manifest=json.loads((R/'data/episodes.json').read_text())
    manifest['episodes']=[e for e in manifest['episodes'] if e['id'] not in {f'extra{n}' for n in range(6,10)}]
    review={}
    for n in range(6,10):
        id=f'extra{n}';body=(R/f'data/source/{id}.txt').read_text();parts=body.split('　　　　　＊');assert len(parts)==len(PLANS[n])
        full=norm(body);anchors=[]
        for a in art[id]:
            anchor=norm(a['after']);assert full.count(anchor)==1,(id,a['src'])
            anchors.append((full.index(anchor)+len(anchor),a.get('gameSrc',SITE+a['src']),a['alt']))
        es=[];offset=0;review[id]=[]
        for sn,(part,plan) in enumerate(zip(parts,PLANS[n]),1):
            bg,loc,camera,track=plan;camera=camera.copy();mood={};cg=None;cgalt='';age=0
            if n==6 and sn in [6,8,9,10,16]:bg='extra-occult-club'
            if n==7:bg='extra-assault-before' if sn==6 else 'extra-assault-hall' if sn in [7,8] else 'extra-gourmet-office'
            if n==9 and sn in [1,2,3,4,5,15,16,17,19,20,21,22,23,24]:bg='extra-construction-workshop'
            memory=n==7 and 6<=sn<=8
            def actors():
                out=[]
                for name in camera[-3:]:
                    aid,h,default=chars[name];expr=mood.get(name,default)
                    if n==6 and name=='ワン' and sn<=2:aid,expr,default='wan-past','neutral','neutral'
                    if n==7 and name=='カガチ' and 6<=sn<=8:aid,expr,default='kagachi-robed','neutral','neutral'
                    if n==6 and name=='ワン' and sn in [3,4]:expr='hurt'
                    if not (R/f'assets/characters/{aid}-{expr}.webp').exists():expr=default
                    if not (R/f'assets/characters/{aid}-{expr}.webp').exists():
                        expr='stern' if aid=='x' else 'neutral'
                    assert (R/f'assets/characters/{aid}-{expr}.webp').exists(),(id,sn,aid,expr)
                    out.append(dict(id=aid,name=name,height=h,expression=expr))
                return out
            def state():return dict(scene=sn,location=loc,bg=f'assets/bg/{bg}.webp',tone='memory' if memory else 'night' if (n==6 and bg=='ch2-forest') or (n==9 and sn in [11,12,13]) else '',cg=cg,cgAlt=cgalt,cast=actors(),bgm=track)
            es.append(dict(type='location',transition='major' if sn in MAJOR[n] else 'inline',**{**state(),'cast':[]}))
            start=len(es)-1
            for raw in part.splitlines():
                line=raw.strip()
                if not line:continue
                if n==7 and sn==6 and line=='身体が床から離れた。':bg='extra-assault-hall'
                m=re.match(r'^([^「]{1,20})(「.*)$',raw) if not raw.startswith(('　',' ')) else None
                speaker=m[1] if m else '';text=m[2] if m else line
                if speaker in chars and speaker!='デビル':
                    if speaker not in camera:
                        camera=[name for name in camera if name not in MOBS]
                        camera=camera[-2:]+[speaker]
                    aid,_,default=chars[speaker]
                    for pattern,expression in [('笑|嬉|ありがと|よかった','smile'),('怖|不安|ごめん|やめろ|震','worried'),('許|怒|ふざけ','angry')]:
                        if re.search(pattern,text) and (R/f'assets/characters/{aid}-{expression}.webp').exists():mood[speaker]=expression
                if n==8 and sn==8 and line.startswith('ランス') and 'ランス' not in camera:camera.append('ランス')
                offset+=len(norm(line));hit=next((a for a in anchors if offset-len(norm(line))<a[0]<=offset),None)
                if hit:_,cg,cgalt=hit;age=0
                elif cg:
                    age+=1
                    if age>=7:cg=None;cgalt=''
                sound=None
                if not speaker:
                    for pattern,se in [('爆発|床が突き上がり','heavy'),('拳.*当た|頬へ当た','hit'),('扉.*開','door-open'),('足音|歩き出','steps'),('紙.*畳|紙.*開','rustle'),('皿|カップ|フォーク','tableware')]:
                        if re.search(pattern,line):sound=se;break
                for i,chunk in enumerate(chunks(text)):
                    e=dict(type='line',speaker=speaker,character=next((a['id'] for a in actors() if a['name']==speaker),''),text=chunk,raw=line if i==0 else '',effect=False,**deepcopy(state()))
                    if sound and i==0:e['se']=sound
                    es.append(e)
            review[id].append(dict(scene=sn,location=loc,background=bg,bgm=track,start=start,end=len(es)-1))
            if sn<len(parts):offset+=len(norm('　　　　　＊'))
        data=dict(id=id,title=f'おまけ{n}　{TITLES[n]}',entries=es,source_lines=sum(bool(l.strip()) and l.strip()!='＊' for l in body.splitlines()),source_scenes=len(parts),source_hash=hashlib.sha256(body.encode()).hexdigest())
        (R/f'data/{id}.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
        manifest['episodes'].append(dict(id=id,title=data['title'],file=f'data/{id}.json',image=anchors[0][1],description=DESC[n],collection='extras'))
        print(id,len(es),'entries',len(parts),'scenes',len(anchors),'illustrations')
    # Keep the collection's numeric order, independent of the other archives.
    manifest['episodes'].sort(key=lambda e:(1,int(e['id'][5:])) if e['id'].startswith('extra') else (2,int(e['id'].split('episode')[-1])) if e['id'].startswith('chapter2-') else (0,0 if e['id']=='prologue' else int(e['id'].split('episode')[-1])))
    (R/'data/episodes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (R/'data/extra6-9-scene-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
