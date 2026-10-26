import json,re,hashlib
from pathlib import Path
import compile_chapter1 as c
import compile_continuation
R=Path(__file__).resolve().parents[1]
C=c.CHAR
C['ゼクサー']=('x-past',180,'neutral')
BG={1:['newsroom','classroom','newsroom','arena-floor','campus','newsroom','newsroom','library','newsroom','newsroom','newsroom','newsroom','newsroom'],2:['old-school-corridor','old-school-corridor']+['clubroom']*7+['old-school-corridor','gumon-office','clubroom'],3:['arena-floor','arena-floor']+['library']*5+['arena-reception']+['library']*6+['corridor','library','library','library'],4:['dorm-night','corridor','dorm-night','corridor','corridor','dorm','cafeteria','campus','clubroom','campus','club-corridor','dorm','dorm-night','library','cafeteria','dorm-night'],5:['library','classroom']+['classroom']*6+['campus','classroom','campus']+['library']*3+['arena-floor',None]+['library']*5+['arena-floor','library','library']}
ART={1:{3:'extra01-a',8:'extra01-b',13:'extra01-c-v2'},2:{3:'extra02-a',8:'extra02-b',11:'extra02-c'},3:{2:'extra03-a',6:'extra03-b',13:'extra03-c'},4:{4:'extra4-doma-rescue',13:'extra4-etiquette-practice',14:'extra4-study-interview'},5:{7:'extra5-lusai-handshake',13:'extra5-lusai-circle',18:'extra5-lusai-return',24:'extra5-lusai-wait'}}
TITLES=['正しいだけでは、売れません','呼ばれたからには、行くしかない','帰れと言っても、また来る','隣に座るなら、明日もここで','君と並んで、歩いていた']
def main():
 manifest=json.loads((R/'data/episodes.json').read_text());manifest['episodes']=[e for e in manifest['episodes'] if not e['id'].startswith('extra')]
 for n in range(1,6):
  body=(R/f'data/source/extra{n}.txt').read_text();entries=[];parts=body.split('　　　　　＊')
  assert len(parts)==len(BG[n])
  for sn,part in enumerate(parts,1):
   bg=BG[n][sn-1];names=list(dict.fromkeys(re.findall(r'^([^「\n]{1,16})「',part,re.M)));cast=[]
   for name in names:
    if name not in C:continue
    id,h,expr=C[name]
    if n==5 and 2<=sn<=10:
     if name in ['X','ゼクサー']:id,expr='x-past','neutral'
     if name=='ルサイ':id,expr='lusai-past','neutral'
    if n==5 and 11<=sn<=14 and name=='X':id,expr='x-young','neutral'
    if n==4 and sn<13 and name=='ドーマ':continue
    if not any(actor['id']==id for actor in cast):cast.append(dict(id=id,name=name,height=h,expression=expr))
   cast=cast[:3];cg=ART[n].get(sn);track='reflection' if n==5 else 'calm' if bg in ['library','newsroom'] else 'daily'
   if bg=='arena-floor':track='battle'
   loc=('過去／' if n==5 and 2<=sn<=20 else '')+{'old-school-corridor':'旧校舎／廊下','gumon-office':'旧校舎／グモンの部長室','corridor':'校舎／廊下','dorm':'学生寮／寮室','cafeteria':'学園／食堂','campus':'学園敷地内','club-corridor':'サークル棟／廊下','arena-reception':'闘技場／受付・通路','newsroom':'新聞部','library':'勉強サークル','classroom':'故郷の学校' if n==5 else '教室','clubroom':'サークル部室','arena-floor':'闘技場','dorm-night':'学生寮・夜'}.get(bg,bg or '記憶')
   state=dict(scene=sn,location=loc,bg=f'assets/bg/{bg}.webp' if bg else None,cg=f'assets/cg/{cg}.webp' if cg else None,cgAlt=TITLES[n-1],tone='dark' if not bg else '',cast=cast,bgm=track)
   entries.append(dict(type='location',**{**state,'cast':[]}))
   for raw in part.splitlines():
    line=raw.strip()
    if not line:continue
    m=re.match(r'^([^「]{1,16})(「.*)$',line);speaker=m[1] if m and not any(x in m[1] for x in ['、','。','それでも']) else '';text=m[2] if speaker else line
    for i,chunk in enumerate(c.chunks(text)):
     e=dict(type='line',speaker=speaker,character=next((x['id'] for x in cast if x['name']==speaker),None),text=chunk,raw=line if i==0 else '',effect=False,**state)
     if not speaker and i==0:
      for word,sound in [('扉が','door-open'),('紙を','rustle'),('カップ','tableware'),('拳が','hit'),('足音','steps')]:
       if word in line:e['se']=sound;break
     entries.append(e)
  d=dict(id=f'extra{n}',title=f'おまけ{n}　{TITLES[n-1]}',entries=entries,source_lines=sum(bool(l.strip()) and l.strip()!='＊' for l in body.splitlines()),source_scenes=len(parts),source_hash=hashlib.sha256(body.encode()).hexdigest())
  (R/f'data/extra{n}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  manifest['episodes'].append(dict(id=d['id'],title=d['title'],file=f'data/extra{n}.json',image=f'assets/cg/{next(iter(ART[n].values()))}.webp',description=TITLES[n-1],collection='extras'))
 (R/'data/episodes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()

if __name__=='__main__':
 from assign_expressions import main as assign_expressions
 assign_expressions()

if __name__=="__main__":
 from enhance_visual_audit import main as enhance_visual_audit
 enhance_visual_audit()
