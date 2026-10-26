# 第2章のノベルゲーム実装

第1〜24話を全文収録。第1章・おまけとは別の章一覧から選択でき、第1章最終話からも続けて進める。

- 原作: ginghum/cursehighschool-、309d88b 時点。原作側の本文は変更しない。
- 24話・18,669エントリー。本文は data/source/chapter2-episode*.txt に保存。
- 原作の挿絵102点を、原作サイトの既存URLと正確な本文アンカーで再利用。19話の寮室五人・夢のミルク、23話の台詞修正を含む。
- 新規素材: 立ち絵・差分34点、人物のいない背景13点、オリジナル合成BGM5曲。
- 立ち絵には仮面のマイナス、停学中のローブなしX、過去の長髪ベレー、甲冑のランス、ミルク等の表情差分を含む。
- 同一場所の会話、近距離の移動は暗転を省略。回想・夢への出入り、地下や裏山への移動は区切る。
- 一話ごとの進行保存、既読管理、画面長押しによる未読スキップ、BGM復帰処理を維持。

## 再生成と検証

```sh
python tools/compile_chapter2.py
python tools/validate_chapter2.py
node tools/test_chapter_runtime.cjs
node tools/test_music.cjs
node tools/test_sound.cjs
```

原作の更新を取り込む場合は `compile_chapter2.py --source 原作リポジトリ --catalog data/chapter2-cast.json` を使う。本文アンカーが一致しないときは停止する。24話の玉座の挿絵だけ、原作側の旧アンカーを現在本文へ読み替えている。

新規画像の用途・プロンプト方針は data/chapter2-new-assets.json。画像は組み込み image_gen で制作。BGMは tools/generate_chapter2_bgm.py による独自作曲・加算合成で、第三者録音は使用していない。
