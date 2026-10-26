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
  save(p,d)
  if n in [3,5]:
   for sn in ([4,5,6] if n==3 else [6,7,8]):
    es=[e for e in d['entries'] if e['scene']==sn and e['type']=='line'];print(n,sn,sum(bool(e.get('cg')) for e in es),'/',len(es),'CG')
 from annotate_sfx import annotate
 annotate()
if __name__=='__main__':enhance()
