"""Audit all episodes and stage anonymous physical speakers and visible crowds.

Only presentation metadata is changed. Voice-only lines, named aliases and existing
authored childhood staging are excluded. Narration uses conservative appearance
phrases; explicit per-scene notes cover silent groups and teachers.
"""
import copy
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'X', 'ゼクサー', '少女', '謎の人物', '仮面の人物', '青髪の男', '来訪者', '背後の少女', '金髪の少女', '幼いプラス', '姉'}
SPEAKERS = set('不良 先生 店員 親衛隊の男子 不良の男子 審判 担当者 部長 保健委員 生徒 決闘委員 通りがかりの生徒 別の生徒 医療係の生徒 別の親衛隊員 部員の男子 勉強サークルの男子 決闘委員の生徒 保健委員の生徒 受付の生徒 一年生の男子 一年生の女子 勉強サークルの女子 通りすがりの生徒 対戦相手 不良の先輩 一年生の部員 不良の部員 別の部員 観客の生徒 別の観客 不良の女子 寮の生徒 不良サークルの女子 サークルの部長 同級生 倉庫の生徒 役員の生徒 放送担当の生徒 廊下の生徒 放送を聞く男子 隣の女子 急ぐ生徒 連れの生徒 通りかかった生徒 その友人 受付の委員 申し込む生徒 見物の生徒 隣の生徒 追い詰められた生徒 敗れた生徒 勝った生徒 道具を運ぶ生徒 奥の男子 隣の牢の男子 奥の女子 隣の男子 連れてこられた女子 新しく入った生徒 座っていた生徒 男子 女子 読書中の生徒 救護の生徒 応援の生徒 売り手の生徒 聴取担当 店の生徒 見学客 連れの客 美術部員 別の美術部員 不良部員 前会長 建設委員 係の者 委員 係 来賓 案内役 別の来賓 係の生徒 オタクサークルの部員 美術サークルの部員 除去を手伝う生徒 母親 店の客 店主 客 別の客 領主 奴隷 来賓の男 来賓の女'.split())
PRESENCE = re.compile(r'(?:生徒|部員|観客|来賓|不良)(?:たち|の一人|のひとり|が二人|が数人|が何人)|(?:数人|何人か|大勢|一人|ひとり)の(?:生徒|部員|観客|来賓|不良)|(?:受付の生徒|店員|教師|白衣の先生)(?:が|は)')
RECOLLECTION = re.compile(r'思い出|映像|写真|新聞|記事|想像|かもしれ|いなかった|いない|いなく|なるだろう|あのとき|ことがあった|こともあった|明日|昨日|話を聞|聞いた話')
# Reviewed narration that mentions people without showing them in this shot.
NO_PRESENCE = {
 'chapter1-episode1': ['白衣の先生は、次の授業へ向かった'],
 'chapter1-episode3': ['教室の生徒たち。'],
 'chapter1-episode6': ['窓の外から、生徒たちの笑い声'],
 'chapter1-episode8': ['昔の不良たちを力で従えた'],
 'chapter1-episode10': ['声が、廊下で不良たちを止めたときとは違った'],
 'chapter1-episode15': ['校舎の外から、練習をする生徒たちの声'],
 'chapter1-episode16': ['立っているのは、今の部員たちだった'],
 'chapter1-episode20': ['新しく勉強サークルへ来たときから、自分を見ていた部員たち'],
 'chapter1-episode21': ['図書館で、部員たちが同じ机を囲んでいた'],
 'extra4': ['その日のうちに、不良たちが消えたわけではない'],
 'extra5': ['部員たちが帰ると、部室は静かになった'],
 'chapter2-episode1': ['旧校舎に居場所を持つ不良サークルの生徒たち'],
 'chapter2-episode2': ['能力を持つ生徒たちが、何をできるのか', '生徒たちへ協力を求めること'],
 'chapter2-episode8': ['救援の生徒たちが通った道', '現場へ駆けつけた生徒たち。'],
 'chapter2-episode9': ['格子の下で、隣の人の足を避けて座っていた生徒たち'],
 'chapter2-episode10': ['昼食へ向かう生徒たちの流れから離れる'],
 'chapter2-episode11': ['演説をしたときにも、生徒たちの声', '生徒たちへ、必要のない動揺', '自分が代理だと知れたら、生徒たちが困る', '誰も、その生徒たちが生きているのか'],
 'chapter2-episode16': ['以前は、地下から盗み出したグレード0'],
 'chapter2-episode17': ['ここへ連れてきた生徒たちも、最初はダンカチのように'],
 'chapter2-episode18': ['生徒たちは立ち上がった。'],
 'chapter2-episode22': ['そこにいる一人の生徒へ、線が伸びた'],
}
# Silent people actually in the scene, rather than recalled people or voices.
SILENT = {
 'prologue': {2: [('同じ茶色のローブを着た生徒たち', 'students')], 3: [('教師が教壇に立ち', 'teacher')], 6: [('生徒たちは慣れた様子で', 'students')], 7: [('受付で手帳と転入の資料', 'clerk')]},
 'chapter1-episode1': {3: [('何人かが笑った。', 'students')], 4: [('白衣の先生が式を添える', 'teacher')], 6: [('店員が表示を確認し', 'clerk')]},
 'chapter1-episode2': {1: [('部員が一人、紙を持って近づいた', 'students')], 2: [('別の生徒が、バルーに手を振った', 'students')]},
 'chapter1-episode3': {7: [('コンケの仲間は、さっきほど笑わなかった', 'bullies')]},
 'chapter1-episode4': {2: [('遠くで一人、同じ動作を繰り返している生徒', 'students')], 3: [('先生が巡回', 'teacher')]},
 'chapter1-episode5': {4: [('手帳を開いて確認する生徒', 'clerk')]},
 'chapter1-episode6': {4: [('後ろにいる部員を振り返った', 'students')], 5: [('科学者の一人を呼び止め', 'teacher')], 8: [('数人ずつが動いている', 'students')]},
 'chapter1-episode7': {5: [('衣装を着た生徒たちの周りに', 'students')]},
 'chapter1-episode8': {12: [('入口の生徒たちに見られる', 'bullies')]},
 'chapter1-episode9': {11: [('不良の一人が顔を向けた', 'bullies')]},
 'chapter1-episode10': {13: [('別の生徒たちが昼飯の袋', 'students')]},
 'chapter1-episode11': {5: [('ほかの寮から来た生徒たち', 'students')], 11: [('入口の部員たちが', 'students')], 13: [('ランスに気づくと、一人が身体をずらした', 'students')]},
 'chapter1-episode12': {2: [('後ろの部員の一人が', 'students')], 5: [('オタクサークルの部員たちが固まっている', 'students')], 10: [('医療係が試合場へ入り', 'medic')]},
 'chapter1-episode14': {1: [('受付場所を確かめ', 'clerk')]},
 'chapter2-episode3': {6: [('床へ座る者。膝を抱えている者。', 'prisoners')]},
 'chapter2-episode4': {1: [('床へ座った男子の靴', 'prisoners')]},
 'chapter2-episode9': {4: [('背の高さが似た生徒が二人いた', 'students')], 12: [('受付へ伝えた', 'medic')]},
 'chapter2-episode10': {6: [('客の一人が、プラスを見た', 'students')]},
 'chapter2-episode14': {1: [('白い手袋をはめ', 'students')]},
 'chapter2-episode15': {12: [('生徒が何人も歩いている', 'students')]},
 'chapter2-episode16': {7: [('何人もがデヂの名前を出した', 'students')], 12: [('部員たちが申し出た', 'students')]},
 'chapter2-episode17': {7: [('もう一人の部員が一緒に', 'students')]},
 'chapter2-episode18': {2: [('受付の向こうから人が出てきた', 'clerk')]},
 'chapter2-episode19': {3: [('受付で名前を告げた', 'clerk')]},
 'chapter2-episode20': {2: [('護衛の一人が掌を上げた', 'clerk')]},
 'chapter2-episode21': {8: [('来賓の案内を終えた係が戻り', 'clerk')], 9: [('次の一人が、待っていた', 'students')], 14: [('次の一人へ同じ説明', 'students')]},
 'chapter2-episode22': {4: [('もう一人、もう一人と、席を離れる生徒', 'students')], 13: [('座ったままの観客の横へ屈んだ', 'students')]},
 'chapter2-episode23': {13: [('係が、前列の観客を', 'students')]},
 'chapter2-episode24': {9: [('一人は、何かを言おうとした', 'students')], 15: [('受付で利用条件を確認', 'clerk')]},
}


def sprite(kind, name):
    files = {'male': ('mob-male-slim', 'brown', 172), 'broad': ('mob-male-broad', 'brown', 181), 'female': ('mob-female-average', 'brown', 164), 'petite': ('mob-female-petite', 'brown', 157), 'teacher': ('mob-civilian-teacher', 'neutral', 178), 'lord': ('mob-civilian-lord', 'neutral', 178), 'lady': ('mob-civilian-noblewoman', 'neutral', 168), 'attendant': ('mob-civilian-servant', 'neutral', 174), 'boy': ('mob-civilian-schoolboy', 'neutral', 164), 'girl': ('mob-civilian-schoolgirl', 'neutral', 157), 'seated-male': ('mob-prisoner-male', 'neutral', 172), 'seated-female': ('mob-prisoner-female', 'neutral', 161)}
    ident, expression, height = files[kind]
    return dict(id=ident, name=name, height=height, expression=expression, anonymous=True, pose='seated' if kind.startswith('seated') else 'standing')


def role(ep, sn, name):
    if name == '先生':
        return 'teacher'
    if ep == 'extra5' and sn in range(2, 10):
        return 'girl' if '女' in name else 'boy'
    if ep in ['chapter2-episode3', 'chapter2-episode4'] and ((ep.endswith('3') and sn >= 5) or (ep.endswith('4') and sn <= 2)):
        if name not in ['決闘委員', '道具を運ぶ生徒']:
            return 'seated-female' if '女' in name else 'seated-male'
    if '来賓' in name:
        return 'lady' if '女' in name or name == '別の来賓' else 'lord'
    if name == '係の者':
        return 'attendant'
    if any(w in name for w in ['女子', '女']):
        return 'female'
    if ep == 'extra4' and name == '寮の生徒':
        return 'petite'
    if name in ['保健委員', '医療係の生徒', '保健委員の生徒', '救護の生徒']:
        return 'female'
    if name == '担当者' and ep == 'chapter1-episode6' and sn <= 2:
        return 'female'
    if any(w in name for w in ['不良', '親衛隊', '前会長', '勝った']):
        return 'broad'
    if name.startswith('別の') or name in ['連れの生徒', 'その友人', '隣の生徒']:
        return 'female' if name != '別の親衛隊員' else 'male'
    return 'male'


def group(ep, sn, kind):
    if kind == 'teacher':
        if ep == 'extra5' and sn < 10:
            return [sprite('attendant', '先生'), sprite('boy', '教室の男子'), sprite('girl', '教室の女子')]
        return [sprite('teacher', '白衣の先生')]
    if kind == 'prisoners':
        return [sprite('seated-male', '牢の男子'), sprite('seated-female', '牢の女子')]
    if kind == 'guests':
        return [sprite('lord', '来賓の男'), sprite('lady', '来賓の女')]
    if kind == 'bullies':
        return [sprite('broad', '不良の男子'), sprite('male', '別の不良')]
    if kind in ['clerk', 'medic']:
        return [sprite('female' if kind == 'medic' else 'male', '保健委員' if kind == 'medic' else '係の生徒')]
    if ep == 'extra5' and sn in range(2, 10):
        return [sprite('boy', '同級生'), sprite('girl', '別の同級生')]
    return [sprite('male', '周囲の男子'), sprite('female', '周囲の女子')]


def authored(ep, sn):
    return (ep == 'chapter2-episode23' and sn in range(6, 12)) or (ep == 'prologue' and sn == 4)


def stage(ep, d, named):
    before = copy.deepcopy(d)
    es = d['entries']
    for e in es:
        e.pop('mobs', None)
        e.pop('mobShot', None)
    scenes = defaultdict(list)
    segment = 0
    previous_place = None
    for i, e in enumerate(es):
        place = (e['scene'], e.get('location'), e.get('bg'))
        if e['type'] == 'location' or place != previous_place:
            segment += 1
        previous_place = place
        if e['type'] == 'line':
            scenes[(e['scene'], segment)].append(i)
    events = []
    for (sn, segment), indices in scenes.items():
        if authored(ep, sn):
            continue
        events_here = []
        for pos, i in enumerate(indices):
            e = es[i]
            name = e.get('speaker', '')
            raw = e.get('raw', '')
            if name in SPEAKERS:
                who = sprite(role(ep, sn, name), name)
                # Preserve existing named or authored anonymous speaker identity.
                if e.get('character') and not e['character'].startswith('mob-'):
                    continue
                events_here.append((max(0, pos - 2), min(len(indices), pos + 5), [who], 'speaker', i))
            if name:
                continue
            if any(phrase in raw for phrase in NO_PRESENCE.get(ep, [])):
                continue
            explicit = [(phrase, kind) for phrase, kind in SILENT.get(ep, {}).get(sn, []) if phrase in raw]
            if explicit:
                for phrase, kind in explicit:
                    events_here.append((pos, min(len(indices), pos + 8), group(ep, sn, kind), 'presence', i))
            elif raw and PRESENCE.search(raw) and not RECOLLECTION.search(raw):
                kind = 'teacher' if re.search('教師|白衣の先生', raw) else 'clerk' if re.search('受付の生徒|店員', raw) else 'guests' if '来賓' in raw else 'bullies' if '不良' in raw else 'students'
                # Never insert an upright crowd into the prison floor scenes.
                if ep in ['chapter2-episode3', 'chapter2-episode4'] and ('牢' in e['location'] or 'prison' in e.get('bg', '')):
                    kind = 'prisoners'
                events_here.append((pos, min(len(indices), pos + 5), group(ep, sn, kind), 'presence', i))
        for lo, hi, actors, kind, anchor in events_here:
            events.append(dict(episode=ep, scene=sn, anchor=es[anchor].get('raw', ''), first=indices[lo], last=indices[hi - 1], reason=kind, actors=[c['name'] for c in actors]))
            for i in indices[lo:hi]:
                e = es[i]
                current = {c['name']: c for c in e.get('mobs', [])}
                for c in actors:
                    current[c['name']] = c
                # Actual speaker gets priority over surrounding extras.
                ranked = sorted(current.values(), key=lambda c: c['name'] != e.get('speaker'))
                e['mobs'] = ranked[:3]
                if e.get('speaker') in current:
                    e['character'] = current[e['speaker']]['id']
                # Cut to the physical background for a brief dialogue/appearance shot.
                # Keep every authored CG reference intact; key battle art is never erased.
                protected = 'episode20-final-fists' in e.get('cg', '') if e.get('cg') else False
                safe_bg = e.get('bg') and '/cg/' not in e['bg'] and not e.get('bgContainsCharacters')
                action = not e.get('speaker') and re.search(r'拳|剣|触手|鞭|殴|爆発|衝撃|突き|倒れ|吹き飛', e.get('raw', ''))
                voice_only = any(word in e.get('speaker', '') for word in ['声', '悲鳴'])
                if safe_bg and not protected and not action and not voice_only and (kind == 'speaker' or i == anchor):
                    e['mobShot'] = True
        # The same student can reply several times. Keep the partner visible between
        # nearby exchanges without carrying anybody through a scene boundary.
        for j in range(1, len(indices) - 1):
            i, left, right = indices[j], es[indices[j - 1]], es[indices[j + 1]]
            if not es[i].get('mobs') and left.get('mobs') == right.get('mobs') and left.get('mobs'):
                es[i]['mobs'] = copy.deepcopy(left['mobs'])
    allowed = {'mobs', 'mobShot', 'character'}
    for a, b in zip(before['entries'], es):
        assert {k: v for k, v in a.items() if k not in allowed} == {k: v for k, v in b.items() if k not in allowed}, ep
    return events


def main():
    manifest = json.loads((ROOT / 'data/episodes.json').read_text())['episodes']
    docs = {m['id']: json.loads((ROOT / m['file']).read_text()) for m in manifest}
    named = {c['name'] for d in docs.values() for e in d['entries'] for c in e.get('cast', []) if not c['id'].startswith('mob-')} | EXCLUDE
    events = []
    actor_pool = []
    actor_index = {}
    episode_cues = {}
    missing = []
    for m in manifest:
        ep, d = m['id'], docs[m['id']]
        before = copy.deepcopy(d)
        events += stage(ep, d, named)
        for i, e in enumerate(d['entries']):
            name = e.get('speaker', '')
            if name and name not in named and not any(s in name for s in ['声', '悲鳴']) and name not in SPEAKERS:
                missing.append((ep, i, name))
        rows = []
        for i, e in enumerate(d['entries']):
            if not e.get('mobs'):
                continue
            ids = []
            for c in e['mobs']:
                key = json.dumps(c, ensure_ascii=False, sort_keys=True)
                if key not in actor_index:
                    actor_index[key] = len(actor_pool)
                    actor_pool.append(c)
                ids.append(actor_index[key])
            rows.append([i, ids, e.get('character', '') if e.get('speaker') in SPEAKERS else '', int(bool(e.get('mobShot')))])
        if rows:
            episode_cues[ep] = dict(source_hash=d.get('source_hash', d.get('source_blob', '')), length=len(d['entries']), rows=rows)
    assert not missing, missing
    (ROOT / 'data/mob-staging.json').write_text(json.dumps(dict(actors=actor_pool, episodes=episode_cues), ensure_ascii=False, separators=(',', ':')) + '\n')
    report = dict(episodes_checked=len(manifest), staged_episodes=len({e['episode'] for e in events}), staged_scenes=len({(e['episode'], e['scene']) for e in events}), events=len(events), speaker_events=sum(e['reason'] == 'speaker' for e in events), missing_speakers=missing, shots=events)
    (ROOT / 'data/mob-scene-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print({k: v for k, v in report.items() if k != 'shots'})


if __name__ == '__main__':
    main()
