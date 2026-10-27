"""Scene-specific childhood staging. Preserve prose, sound and saved entry positions."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / 'data/chapter2-episode23.json'
BG = {name: f'assets/bg/beret-past-{name}.webp' for name in ['street', 'shop', 'manor', 'studio']}
BG['room'] = 'assets/bg/ch2-memory-room.webp'


def actor(role, expression='neutral'):
    if role == 'beret':
        return dict(id='beret-past', name='ベレー', height=137, expression=expression)
    names = dict(lord='領主', mother='母親', merchant='店主', servant='使用人', commoner='街の人')
    return dict(id=f'mob-civilian-{role}', name=names[role], height=177 if role != 'mother' else 165, expression='neutral')


def stage(document):
    before = copy.deepcopy(document)
    scene = None
    for entry in document['entries']:
        sn = entry['scene']
        if sn not in range(6, 12):
            continue
        if sn != scene:
            scene = sn
            tone = 'memory'
            background = {6: 'street', 7: 'room', 8: 'manor', 9: 'street', 10: 'studio', 11: 'studio'}[sn]
            expression = 'groomed' if sn >= 11 else 'afraid' if sn == 9 else 'neutral'
            roles = ['beret'] if sn != 8 else []
        raw = entry.get('raw', '')
        if sn == 6:
            if raw == '母親は、売春で生計を立てていた。':
                background = 'room'
            elif raw == 'ベレー「お腹が、すいた」':
                roles = ['beret', 'mother']
            elif raw == '別の通りでは、転んだ子供が泣いていた。':
                background, roles = 'street', ['beret']
            elif raw == '雨の日、屋根から落ちる水を器へ受けた。':
                background, roles = 'room', ['beret']
            elif raw == 'ベレー「箱、知らない？」':
                roles = ['beret', 'mother']
            elif raw == '通りのごみを探した。':
                background, roles = 'street', ['beret']
            elif raw == '見つけたのは、店先だった。':
                background, roles = 'shop', ['beret', 'merchant']
            elif raw == '店の客「この角度からでも、飛ぶ直前に見える」':
                roles = ['beret', 'merchant', 'customer']
            elif raw == '自分が何日も見ていたところを、その人も見ていた。':
                expression = 'hopeful'
            elif raw == '帰り道を、ゆっくり歩いた。':
                background, roles = 'street', ['beret']
        elif sn == 7:
            if raw == '母親「金があるのね」':
                roles, expression = ['beret', 'mother'], 'afraid'
            elif raw == 'ベレーは、人の顔を見るようになった。':
                background, roles = 'street', ['beret']
            elif raw == '母親が戻ってきた夜も、顔を見た。':
                background, roles = 'room', ['beret', 'mother']
            elif raw == 'その夜、ベレーは母親を殺した。':
                roles, expression = ['beret'], 'neutral'
        elif sn == 8:
            if raw == '客「これは、穏やかなものではないね」':
                roles = ['customer', 'merchant']
            elif raw == 'ベレーは、隅に立っていた。':
                roles = ['beret', 'customer', 'merchant']
            elif raw == '帰ってから、新聞を開いた。':
                background, roles = 'room', ['beret']
            elif raw == '帰り道で会えば、向こうは知らずに道を空けた。':
                background, roles = 'street', ['beret']
            elif raw == '部屋へ戻った。':
                background, roles = 'room', ['beret']
            elif raw == '作品が増えた。':
                background, roles = 'street', ['beret']
        elif sn == 9:
            if raw == '厚い絨毯が、濡れた靴の音を吸った。':
                background, roles = 'manor', ['beret']
            elif raw == 'その前に、領主がいた。':
                roles = ['beret', 'lord']
            elif raw == '領主は、使用人を呼んだ。':
                roles = ['beret', 'lord', 'servant']
            elif raw == 'しばらくして、もう一度、椅子へ座った。':
                roles = ['beret', 'lord']
        elif sn == 10:
            if raw == 'ベレーが開けると、使用人が、替えの服を抱えていた。':
                roles = ['beret', 'servant']
            elif raw == '鏡の中に、見慣れない顔があった。':
                expression, roles = 'groomed', ['beret']
            elif raw == '数日後、裏の部屋へ、人が連れてこられた。':
                roles = ['beret', 'lord', 'captive']
            elif raw == '領主が、部屋を出た。':
                roles = ['beret', 'captive']
            elif raw == '廊下から、次の指示は来なかった。':
                roles = ['beret']
            elif raw == 'あとで、温かい食事が運ばれてきた。':
                roles = ['beret', 'servant']
            elif raw == '領主は、作品を見た。':
                roles = ['beret', 'lord']
            elif raw == '白い紙を、惜しまずに使うようになった。':
                roles = ['beret']
            elif raw == 'ある日、食事を下げる使用人へ、少し待ってと声を掛けた。':
                roles = ['beret', 'servant']
        elif sn == 11:
            if raw == '領主が来ると、紙を伏せた。':
                roles = ['beret', 'lord']
            elif raw == '旅の支度が整えられた。':
                roles = ['beret']

        if raw in ['夜、腕を抱えたまま、窓の下へ座った。', '母親が戻ってきた夜も、顔を見た。', '捕らえられた夜は、雨だった。', '最初の夜、何度も確かめた。', '机の上へ、売れなかった木彫りを出した夜があった。']:
            tone = 'night'
        elif raw in ['夜が明けるころ、鳥を作ったときのことを思い出した。', 'そのまま、朝になった。', '数日後、裏の部屋へ、人が連れてこられた。', 'ベレーは、人の顔を見るようになった。', '厚い絨毯が、濡れた靴の音を吸った。']:
            tone = 'memory'
        entry['bg'] = BG[background]
        entry['tone'] = tone
        # Keep memory boundaries without extra blackout cards for short moves.
        entry['cast'] = []
        for role in roles:
            if role in ['customer', 'captive']:
                c = actor('servant' if role == 'customer' else 'commoner')
                c['name'] = '店の客' if role == 'customer' and sn == 6 else '客' if role == 'customer' else '奴隷'
                entry['cast'].append(c)
            else:
                entry['cast'].append(actor(role, expression if role == 'beret' else 'neutral'))
        name = entry.get('speaker')
        if name in ['ベレー', '母親', '領主', '店主', '店の客', '客', '別の客', '奴隷']:
            match = next((c for c in entry['cast'] if c['name'] == name), None)
            if name == '別の客':
                match = next((c for c in entry['cast'] if c['id'] == 'mob-civilian-merchant'), None)
            if match:
                entry['character'] = match['id']
    allowed = {'bg', 'cast', 'character', 'tone'}
    for a, b in zip(before['entries'], document['entries']):
        assert {k: v for k, v in a.items() if k not in allowed} == {k: v for k, v in b.items() if k not in allowed}
        if a['scene'] not in range(6, 12):
            assert a == b
    return document


def main():
    doc = json.loads(EPISODE.read_text())
    stage(doc)
    EPISODE.write_text(json.dumps(doc, ensure_ascii=False, separators=(',', ':')) + '\n')
    print('Beret childhood: scenes 6–11 staged; prose/audio/CG/save positions preserved')


if __name__ == '__main__':
    main()
