"""Postcompile staging and sound cues; never alter original prose."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def enhance():
 for p in sorted((ROOT/'data').glob('chapter1-episode*.json')):
  d=json.loads(p.read_text());n=int(d['id'].split('episode')[-1]);active=None;previous_scene=None
  for e in d['entries']:
   raw=e.get('raw','');s=e['scene'];new_scene=s!=previous_scene;previous_scene=s;e.pop('se',None)
   if n==3:
    if s==4 and raw=='拳が来た。':active='episode03-guard'
    if s==5 and raw=='左を出す。':active='episode03-heavy-miss'
    if s==5 and raw=='コンケが左右へ、細かく身体を揺らした。':active='episode03-guard'
    if s==6 and raw=='拳が届く、その直前。':active='episode03-impact-night'
    if s==6 and raw=='ランス「終わり」':active=None
    if s in [4,5,6] and active:
     e['cg']='assets/cg/'+active+'.webp';e['cgAlt']={'episode03-guard':'夜の練習場でコンケの拳を受けるプラス','episode03-heavy-miss':'重い左拳をかわされ、横腹への蹴りを受けるプラス','episode03-impact-night':'コンケの左腕の防御へ重い右拳を届かせるプラス'}[active]
   if n==5 and s in [6,7,8]:
    if raw=='ダイは、消えた。' or (s==7 and new_scene):active='episode05-teleport'
    if s==6 and raw=='そこへ左拳を出す。':active='episode05-a-r3'
    if s==6 and raw=='届く前に、ダイが消えた。':active='episode05-teleport'
    if s==7 and raw=='左拳が伸びた。':active='episode05-a-r3'
    if s==7 and raw=='ダイは次のマークへ移った。':active='episode05-teleport'
    if s==8 and raw=='ダイが右手を上げた。':active='episode05-flank'
    if s==8 and raw=='ダイが消えた。':active='episode05-teleport'
    if s==8 and raw=='ダイの肩が、空いた横へ入る。':active='episode05-flank'
    if s==8 and raw=='膝が床へつき、身体を起こすための場所が、ひとつずつなくなった。':active='episode05-hold'
    if s==8 and raw=='ダイの腕が、すぐに離れた。':active=None
    if active:
     e['cg']='assets/cg/'+active+'.webp';e['cgAlt']='右腕を支持具で保護し、左腕でダイに挑むプラス'
   if not raw:continue
   if (e.get('effect')=='teleport' or re.search(r'^(ダイ[はが]、?消えた。|消えた。|届く前に、ダイが消えた。)$',raw)):e['se']='teleport'
   elif raw in ['鈍い音がした。','横腹へ蹴りが入った。','鞭が床を打つ。'] or re.search(r'拳[がを].*(当たった|当たる|入った)。',raw):e['se']='heavy' if '鈍い' in raw else 'whip' if '鞭' in raw else 'hit'
   elif raw in ['そこへ、反対の拳が短く入った。','背中の斜め後ろから、軽く肩を打たれた。','プラスは顔を引き、腕で受けた。']:e['se']='hit'
   elif raw in ['拳だけが、届かなかった場所を通った。','プラスの拳は、空いた場所を通った。']:e['se']='whoosh'
   elif re.search(r'(表紙が閉じた。|手帳を閉じた。)$',raw) and not e.get('speaker'):e['se']='rustle'
   elif raw.startswith(('サニー「始め','サニー「そこまで','サニー「止め')):e['se']='chime'
   elif raw in ['鞭が、そこへ来た。','もう一度、鞭が来た。','跳ばずに、小さく足を引いた。鞭が床を打つ。','鞭に腕の横を打たれ、痛みで考えが途切れる。','廊下では、ヒカルの鞭が壁を打った。']:e['se']='whip'
   elif raw in ['ユージが床へ落ちた。','重い音が、客席まで響いた。','廊下で、大きな音がした。']:e['se']='heavy'
   elif raw=='音がした。' and n in [5,7]:e['se']='whip' if n==5 else 'heavy'
   elif n==11 and raw=='もう一枚。今度は、こっちを向いて。':e['se']='camera'
  save(p,d)
  if n in [3,5]:
   for sn in ([4,5,6] if n==3 else [6,7,8]):
    es=[e for e in d['entries'] if e['scene']==sn and e['type']=='line'];print(n,sn,sum(bool(e.get('cg')) for e in es),'/',len(es),'CG')
if __name__=='__main__':enhance()
