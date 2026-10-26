# カス校 — STORY ARCHIVE

カス校メインストーリーのブラウザ向けストーリーモード。PC・スマートフォン横持ちを基本に、プロローグと第1章第1〜14話の全文を収録しています。

タイトル → ストーリー選択 → 第1章 → 各エピソード。クリック・タップ・Space・右矢印で進みます。場所カットイン、立ち絵の表情、挿絵、オート、既読スキップ、ログ、文字速度・サイズ変更、途中保存を搭載しています。打撃・鞭・瞬間移動などのオリジナルSEを搭載。設定からSEの音量・ミュート・試聴を変更できます。場面別BGM6曲を搭載。BGMとSEはそれぞれ音量・ミュート・試聴を設定できます。ボイスは未収録です。

保存はブラウザのlocalStorageを利用します。別端末へは同期されません。

静的サイトのため、HTTPサーバーからそのまま配信できます。GitHub Actionsがmainへの更新でGitHub Pagesへ配置します。

本編原文: ginghum/cursehighschool- の stories.json。原作は変更せず、このゲーム用に台本を分けています。本文の非空行を順序どおり保持し、長い地の文の表示区切りを追加しています。

第6話は原文740行・12シーンを収録。第7〜10話は原文全文・53シーンを収録しています。

第11話は原文746行・15シーン。第3話・第5話の戦闘へ挿絵4枚を追加し、主要戦闘区間の表示を挿絵中心にしています。

再生成: `python tools/compile_chapter1.py`（全話）、`python tools/compile_continuation.py 12 13 14`（続話）。戦闘・SE演出は `tools/enhance_battles_audio.py` で再適用されます。SEの再生成は `python tools/generate_sfx.py`。

検証: `python tools/validate_chapter1.py`、`node tools/test_chapter_runtime.cjs`、`node tools/test_sound.cjs`。

SEは全15エピソードの279か所へ配置。21種類の選択試聴が可能です。`data/se-cues.json` は原文で確認した動作の指定、`data/se-review.json` は実際の表示行との対応です。`python tools/annotate_sfx.py` で再配置、`python tools/validate_sfx.py` で全話・WAVを検証できます。文字送りごとの音や常時ループはありません。

BGMは `data/bgm-scenes.json` に全173場面の割当と切替位置を記録しています。同じ曲では再生を継続し、曲を変える時は1.2秒でクロスフェードします。全曲オリジナルのインスト曲で、`python tools/generate_bgm.py` から再生成できます。`python tools/assign_bgm.py` で再配置（台本コンパイル時にも実行）、`python tools/validate_bgm.py` と `node tools/test_music.cjs` で検証できます。

第12〜14話は原文1,864行・38シーンを収録。戦闘・負傷・昼夜を合わせた新規／修正CG9枚と立ち絵2枚、既刊CG7枚を追加。SEは74か所を新規設定し、全38場面へBGMを割り当てています。
