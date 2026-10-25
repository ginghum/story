"""Apply visual pacing to the existing prologue without changing text or save indices."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/prologue.json'
data=json.loads(p.read_text());es=data['entries']
def find(text):
 hits=[i for i,e in enumerate(es) if e.get('raw')==text]
 assert len(hits)==1,(text,hits)
 return hits[0]
def span(start,end,filename,alt):
 for e in es[start:end]:e['cg']='assets/cg/'+filename+'.webp';e['cgAlt']=alt
# The departure line itself removes X, including any illustration that depicts him.
exit_x=find('今度こそ、Xは歩き去った。')
for e in es[exit_x:]:
 if e['scene']!=4:break
 e['cast']=[c for c in e.get('cast',[]) if c['id']!='x']
 if e.get('cg')=='assets/cg/prologue-e-handbook-v2.webp':e['cg']=None;e['cgAlt']=None
scene_end=lambda n:next((i for i,e in enumerate(es) if e['scene']>n),len(es))
span(find('ユージ「なんだよ。俺、何もしてねえぞ！」'),scene_end(2),'prologue-b','ユージと歩く学園')
span(find('X「プラス・ゼロ。……なるほど。上から聞いていた転入生というのは、君か」'),exit_x,'prologue-e-handbook-v2','プラスの手帳を確認するX')
span(find('小柄な少女が座っていた。'),scene_end(6),'prologue-f','プラス・ユージ・ヤオイの観戦')
span(find('机に向かっていた青年が、椅子ごと少し振り向いた。青みの強い短髪。眼鏡の奥に黄色い目。プラスよりずっと小柄だったが、目つきは鋭かった。'),scene_end(7),'prologue-d','寮でランスと出会う')
span(next(i for i,e in enumerate(es) if e['scene']==9),scene_end(9),'prologue-c','三人で過ごす寮の夜')
span(find('巨大な球と壁の間に、プラスの身体が挟まった。'),find('男が、慌てて球を消した。'),'sphere','球と壁に挟まれるプラス')
span(find('それでも、空中のボールが横へ跳ねた。ぼん、という音を残し、離れた的に当たって落ちる。'),find('転がったボールを、プラスが拾ってくる。'),'yuji-training','ボールを弾くユージ')
span(find('槍が走った。'),find('槍を消し、手帳を閉じる。'),'lance-training','槍を繰り出すランス')
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Updated illustration spans and X departure; original lines and entry indices preserved.')
