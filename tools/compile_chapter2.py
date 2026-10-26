"""Compile all chapter-two prose verbatim with reviewed scene staging and source CG anchors.
Run: python tools/compile_chapter2.py --source ../prose --catalog ../catalog.json
"""
import argparse,json,re,hashlib
from pathlib import Path
from chapter2_plans import SCENES,PLACES,MEMORIES,DESCRIPTIONS
import compile_chapter1 as base
R=Path(__file__).resolve().parents[1]
SOURCE_SITE='https://ginghum.github.io/cursehighschool-/'
NIGHT={6,7,8}
# Broadcast voices and aliases keep their printed speaker labels; only physically present actors enter the camera.
ALIASES={(1,'少女'):'ミルク',(3,'少女'):'ジェンド',(3,'少女の声'):'ジェンド',(4,'仮面の人物'):'マイナス',(4,'青髪の男'):'シグマ',(6,'背後の少女'):'バグ',(6,'金髪の少女'):'ヴァイン',(7,'来訪者'):'レオルカ'}
SPEAKER_RE=re.compile(r'^([^「『]{1,20})([「『].*)$')
def norm(s):return re.sub(r'\s+','',s)
def emotion(id,text,default):
 choices=[]
 if re.search('ごめん|申し訳|怖|不安|大丈夫|……',text):choices+=['worried','serious']
 if re.search('ありがとう|嬉し|楽しい|一緒|やった|よかった',text):choices=['smile']+choices
 if re.search('ふざけ|やめろ|許さ|殺|戦|倒す|勝つ|負け',text):choices=['serious']+choices
 if re.search('えっ|え？|何で|なんで|!?|！？',text):choices=['surprised']+choices
 return next((x for x in choices if (R/f'assets/characters/{id}-{x}.webp').exists()),default)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--catalog',type=Path,default=R/'data/chapter2-cast.json');args=ap.parse_args()
 source=json.loads((args.source/'stories.json').read_text()) if args.source else {'chapters':[dict(id=e['id'],title=e['title'],body=(R/f"data/source/{e['id']}.txt").read_text()) for e in json.loads((R/'data/episodes.json').read_text())['episodes'] if e['id'].startswith('chapter2-')]};art=json.loads((args.source/'illustrations.json').read_text())['chapters'] if args.source else {f'chapter2-episode{n}':[{k:v for k,v in a.items() if k!='episode'} for a in json.loads((R/'data/chapter2-illustrations.json').read_text()) if a['episode']==f'chapter2-episode{n}'] for n in range(1,25)};catalog=json.loads(args.catalog.read_text());chars={}
 for c in catalog:
  height=next((int(re.search(r'\d+',f['value'])[0]) for f in c['facts'] if f['label']=='身長' and re.search(r'\d+',f['value'])),175)
  default='neutral'
  if c['id']=='plus':default='smile'
  if c['id']=='x':default='stern'
  chars[c['name']]=(c['id'],height,default)
 chars.update(base.CHAR)
 chars['X']=('x',180,'stern')
 manifest=json.loads((R/'data/episodes.json').read_text());manifest['episodes']=[e for e in manifest['episodes'] if not e['id'].startswith('chapter2-')];review={};allcg=[]
 for n in range(1,25):
  id=f'chapter2-episode{n}';ch=next(c for c in source['chapters'] if c['id']==id);body=ch['body'];parts=body.split('　　　　　＊');keys=SCENES[n].split();assert len(keys)==len(parts),(n,len(keys),len(parts))
  (R/f'data/source/{id}.txt').write_text(body)
  full=norm(body);cgs=[]
  for item in art.get(id,[]):
   anchor=norm('エンプレス「ツキチヨ。マイナスの弟を、見ておきなさい」' if item['src'].endswith('chapter2-episode24-d-throne.webp') else item['after']);assert full.count(anchor)==1,(id,item['src'],'ambiguous CG anchor');cgs.append((full.index(anchor)+len(anchor),SOURCE_SITE+item['src'],item['alt']));allcg.append(dict(episode=id,**item))
  entries=[];offset=0;last_track=None;scene_review=[]
  for sn,(part,key) in enumerate(zip(parts,keys),1):
   loc,bg=PLACES[key];loc=MEMORIES.get((n,sn),loc);tone='night' if key in ['F','E'] or (n in NIGHT and key in ['C','J']) else ''
   if key=='d':tone='';
   if n==3 and sn==4:bg='training'
   if (n,sn) in [(19,9),(24,21)]:bg='dorm-night' if n==19 else 'library';tone='dream'
   if n==16 and sn in [6,7]:tone='memory'
   if n==23 and 6<=sn<=11:tone='memory';bg='ch2-memory-room'
   track='daily'
   if key in ['Q','L','N','G','K','V']:track='calm'
   if key in ['P','T','B','W','d']:track='underground' if n<=5 else 'tension'
   if key=='F':track='forest-battle' if n in [7,8] else 'tension'
   if key=='A':track='finale' if n>=20 else 'battle'
   if key=='Z':track='training'
   if key in ['U','I','E','X'] or (n,sn) in MEMORIES:track='reflection'
   if key=='Y' and n>=20:track='festival'
   if n==24 and key in ['k','C','D']:track='homecoming'
   # Dialogue comes from non-indented lines. Narration quoting a word stays narration.
   lines=[raw for raw in part.splitlines() if raw.strip()];names=[]
   for raw in lines:
    m=SPEAKER_RE.match(raw) if not raw.startswith(('　',' ')) else None
    if m:
     name=ALIASES.get((n,m[1]),m[1])
     if name in chars and name not in names:names.append(name)
   camera=[];cg=None;cgalt='';appearance={};start=len(entries);masked=n==4;armored=n==22 and sn==6
   def actors():
    result=[]
    for name in camera:
     aid,h,default=chars[name]
     # The mask hides Minus during the escape; X is serving suspension late in the festival.
     if name=='マイナス' and masked:aid,default='minus-masked','neutral'
     if name=='ランス' and armored:aid,default='lance-armored','neutral'
     if name=='ベレー' and n==23 and 6<=sn<=11:aid,default,h='beret-past','neutral',137
     if name=='X' and n in [21,22,23,24] and (R/'assets/characters/x-suspended-neutral.webp').exists():aid,default='x-suspended','neutral'
     expr=appearance.get(name,default)
     if name=='ランス' and (8<=n<=12):expr='hurt'
     if name=='プラス' and (9<=n<=12):expr='bandaged-serious' if expr=='serious' else 'bandaged-smile'
     if name=='X' and n in [21,22,23,24] and aid=='x-suspended':expr='neutral'
     if aid in ['beret-past','minus-masked','lance-armored']:expr=default
     if not (R/f'assets/characters/{aid}-{expr}.webp').exists():expr=default
     result.append(dict(id=aid,name='仮面の人物' if aid=='minus-masked' else name,height=h,expression=expr))
    return result
   def state():return dict(scene=sn,location=loc,bg=f'assets/bg/{bg}.webp',tone=tone,cg=cg,cgAlt=cgalt,cast=actors(),bgm=track)
   st=state();st['cast']=[]
   transition='major' if (n,sn) in MEMORIES and (n,sn-1) not in MEMORIES or (sn>1 and (n,sn-1) in MEMORIES and (n,sn) not in MEMORIES) or sn==1 else 'inline'
   # Geographic changes, rather than every scene marker, receive a cut.
   if sn>1 and keys[sn-2]!=key and (key in ['T','P','U','F','f','k'] or keys[sn-2] in ['T','P','U','F','f','k']):transition='major'
   if (n,sn) in [(8,12),(11,1),(12,1),(13,1),(16,2),(16,14),(20,1),(24,11),(24,14)]:transition='major'
   entries.append(dict(type='location',transition=transition,**st))
   for raw in lines:
    line=raw.strip();m=SPEAKER_RE.match(raw) if not raw.startswith(('　',' ')) else None;speaker=m[1] if m else '';name=ALIASES.get((n,speaker),speaker);text=m[2] if m else line
    if not speaker:
     if n==22 and '甲冑が全身を覆う' in line:armored=True
     if n==4 and ('仮面を胸の前へ下げた' in line or '仮面を下ろした' in line):masked=False
     for present in names:
      if re.match(re.escape(present)+r'[はがのもと、]',line) and present not in camera:camera=camera[-2:]+[present]
    if name in chars and not speaker.endswith('の声'):
     if name not in camera:camera=(camera[-2:]+[name])
     aid,h,default=chars[name];appearance[name]=emotion(aid,text,default)
    # Match each illustration to its exact source paragraph, never by guessed scene number.
    offset+=len(norm(line))
    for end,path,alt in cgs:
     if offset-len(norm(line))<end<=offset:cg,cgalt=path,alt
    # A CG is a short held shot; return to sprites after six source lines.
    if cg and cg!=locals().get('previous_cg'):cg_age=0
    elif cg:cg_age+=1
    if cg and cg_age>=6:cg=None;cgalt=''
    previous_cg=cg
    chunks=base.chunks(text);se=None
    if not speaker:
     for pattern,sound in [(r'扉.*開','door-open'),(r'扉.*閉','door-close'),(r'足音|歩き出','steps'),(r'紙.*(開|畳|めく)','rustle'),(r'拳.*(当た|届)|殴','hit'),(r'爆発','heavy')]:
      if re.search(pattern,line):se=sound;break
    for k,chunk in enumerate(chunks):
     entry=dict(type='line',speaker=speaker,character=next((a['id'] for a in actors() if a['name']==name or a['id']=='minus-masked' and name=='マイナス'),chars[name][0]) if name in chars and not speaker.endswith('の声') else '',text=chunk,raw=line if k==0 else '',effect=False,**state())
     if se and k==0:entry['se']=se
     entries.append(entry)
   scene_review.append(dict(scene=sn,location=loc,background=bg,entries=[start,len(entries)-1],speakers=names,transition=transition,bgm=track))
   offset+=len(norm('　　　　　＊')) if sn<len(parts) else 0
  d=dict(id=id,title=ch['title'],entries=entries,source_lines=sum(bool(l.strip()) and l.strip()!='＊' for l in body.splitlines()),source_scenes=len(parts),source_hash=hashlib.sha256(body.encode()).hexdigest())
  # Compact JSON avoids downloading repeated whitespace over mobile connections.
  (R/f'data/{id}.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
  manifest['episodes'].append(dict(id=id,title=ch['title'],file=f'data/{id}.json',image=cgs[0][1] if cgs else 'assets/bg/campus.webp',description=DESCRIPTIONS[n],collection='chapter2'))
  review[id]=scene_review;print(id,len(entries),'entries',len(cgs),'CG')
 manifest['episodes'].sort(key=lambda e:(2,int(e['id'].split('episode')[-1])) if e['id'].startswith('chapter2-') else (1,int(e['id'][5:])) if e['id'].startswith('extra') else (0,0 if e['id']=='prologue' else int(e['id'].split('episode')[-1])))
 (R/'data/episodes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(R/'data/chapter2-scene-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 (R/'data/chapter2-illustrations.json').write_text(json.dumps(allcg,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()

if __name__=="__main__":
 from enhance_visual_audit import main as enhance_visual_audit
 enhance_visual_audit()
