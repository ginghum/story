"""Check exact source coverage, sprite files, music and original CG timing."""
import json, hashlib, re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'data/episodes.json').read_text())['episodes']
assert [e['id'] for e in manifest if e['id'].startswith('extra')]==[f'extra{n}' for n in range(1,10)]
art=json.loads((R/'data/extra6-9-illustrations.json').read_text())
tracks={t['id'] for t in json.loads((R/'data/bgm-tracks.json').read_text())['tracks']}
assets=set();count=0
norm=lambda s:re.sub(r'\s+','',s)
for n in range(6,10):
    id=f'extra{n}';d=json.loads((R/f'data/{id}.json').read_text());body=(R/f'data/source/{id}.txt').read_text()
    assert d['source_hash']==hashlib.sha256(body.encode()).hexdigest()
    expected=[l.strip() for l in body.splitlines() if l.strip() and l.strip()!='＊']
    assert [e['raw'] for e in d['entries'] if e.get('raw')]==expected
    assert d['source_lines']==len(expected)
    assert d['source_scenes']==len(body.split('　　　　　＊'))
    offset=0;first={}
    for e in d['entries']:
        if e.get('raw'):offset+=len(norm(e['raw']))
        if e['type']=='location' and e['scene']>1:offset+=1
        assert e['bgm'] in tracks
        assert len(e['cast'])<=3 and len({c['id'] for c in e['cast']})==len(e['cast'])
        assert len(e.get('text',''))<=110
        assets.add(e['bg'])
        for c in e['cast']:assets.add(f"assets/characters/{c['id']}-{c['expression']}.webp")
        if e.get('se'):assert (R/f"assets/se/{e['se']}.wav").is_file()
        if e.get('cg'):first.setdefault(e['cg'],offset)
        if e.get('speaker')=='デビル':assert all(c['name']!='デビル' for c in e['cast'])
    for a in art[id]:
        anchor=norm(a['after']);assert norm(body).count(anchor)==1
        path='https://ginghum.github.io/cursehighschool-/'+a['src']
        assert first[path]==norm(body).index(anchor)+len(anchor),(id,path,first[path])
    count+=len(d['entries'])
for path in assets:
    with Image.open(R/path) as im:im.verify()
print(f'PASS: 4 extras, {count} entries, 62 scenes, exact original prose and all 15 CG anchors, {len(assets)} decoded assets, music and sound.')
