"""Add episode 6 while preserving previously reviewed episode data."""
import json
from pathlib import Path
import compile_chapter1 as c
ROOT=Path(__file__).resolve().parents[1]
DUO=['プラス','ランス']
scene,cue=c.scene,c.cue
original_expression=c.default_expression
c.default_expression=lambda name,text: 'serious' if name=='プラス' else original_expression(name,text)
c.CHAR['プラス']=('plus',184,'serious')
c.CHAR['部長']=('mob-male-broad',180,'brown')
c.PLANS[6]=[
 (scene('闘技場／選手用通路','arena-reception',['プラス'],tone='dark'),[
  cue('プラスは一度うなずき、半歩下がった。',location='闘技場／保健室への通路',bg='corridor',tone='',cut=True)]),
 (scene('保健室／待合','infirmary-day',['プラス']),[
  cue('ランス「ユージは」',cast=DUO)]),
 (scene('保健室／ユージのベッド','infirmary-day',cg='episode06-a-r3'),[]),
 (scene('回想／以前のサークル','clubroom',['ユージ']),[
  cue('部長「新入生？',cast=['ユージ','部長']),
  cue('試合は、短かった。',location='回想／ヒカルとの決闘',bg='arena',cast=['ユージ','ヒカル','部長'],cut=True),
  cue('試合のあと、ユージは部長を待った。',location='回想／契約の手続き',bg='clubroom',cast=['ユージ','部長'],cut=True),
  cue('ヒカル「君がユージだね」',cast=['ユージ','ヒカル','部長']),
  cue('ヒカル「彼が払う星の代わりに、君をもらう。',cg='episode06-contract-memory')]),
 (scene('回想／ヒカルの活動室','clubroom',cast=[],cg='episode06-costume-memory'),[
  cue('ユージは、学園にいる誰かへ相談すればいいと思った。',location='回想／授業後の教室',bg='classroom',cast=['ユージ'],cg=None,cut=True),
  cue('その窓口では、契約を確認された。',location='回想／生徒会の管理窓口',bg='corridor',cut=True),
  cue('元のサークルへも行った。',location='回想／以前のサークル',bg='clubroom',cut=True),
  cue('部長「……どうした」',cast=['ユージ','部長']),
  cue('午後になると、ヒカルのところへ行く。',location='回想／ヒカルの活動',bg='courtyard',cast=[],cg='episode06-costume-memory',cut=True),
  cue('寮へ帰れば、ユージはいつもの調子で話した。',location='回想／学生寮',bg='dorm-night',cast=['ユージ','ランス'],cg=None,cut=True)]),
 (scene('保健室／ユージのベッド・夕方','infirmary-day',cg='episode06-a-r3'),[]),
 (scene('学園敷地内／夜の帰り道','campus-night',DUO),[]),
 (scene('保健室／荷物を預ける','infirmary-day',DUO,tone='night'),[
  cue('荷物を届けたとき、ユージはまだ眠っていた。',location='学園／夕食',bg='cafeteria',tone='night',cut=True),
  cue('練習場の明かりは、夜になってもついていた。',location='能力練習場／夜',bg='training-night',tone='',cut=True)]),
 (scene('能力練習場／足運びと棒の練習','training-night',DUO),[
  cue('その手の中に、金属の短い棒が生まれた。',cg='episode06-training-left'),
  cue('プラスは左手を上げ下げした。',cg=None)]),
 (scene('能力練習場／休憩','training-night',DUO),[]),
 (scene('能力練習場／素手の練習','training-night',DUO),[]),
 (scene('能力練習場／練習の終わり','training-night',DUO),[
  cue('そのあと、足の置き方だけをゆっくり確かめた。',location='学園敷地内／夜の帰り道',bg='campus-night',cut=True),
  cue('二人は部屋へ戻った。',location='学生寮／三人の部屋・夜',bg='dorm-night',cut=True),
  cue('部屋が暗くなる。',cast=[],tone='dark')])
]

def main():
 id='chapter1-episode6';body=(ROOT/'data/source'/f'{id}.txt').read_text()
 title='第1章　第6話　いつも通りが、うまくできない'
 source={'chapters':[{'id':id,'title':title,'body':body}]}
 report=c.compile_episode(6,source)
 for item in report:item.update(reviewed=False,review_basis='原文順序・登退場・負傷腕・回想分離のデータ検証。画面確認は別途記録。')
 p=ROOT/'data/chapter1-scene-review.json';review=json.loads(p.read_text());review['episodes'][id]=report;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'data/episodes.json';manifest=json.loads(p.read_text());manifest['episodes']=[e for e in manifest['episodes'] if e['id']!=id];manifest['episodes'].append(dict(id=id,title=title,file=f'data/{id}.json',image='assets/cg/episode06-a-r3.webp',description='ユージが語る契約の過去。いつもの笑顔の奥を知り、プラスとランスは夜の練習へ向かう。'));p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Compiled episode 6:',len(report),'scenes')
if __name__=='__main__':main()
