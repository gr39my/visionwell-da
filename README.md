# visionwell-da

高校推薦枠マッチングシステムのサンプルアプリです。CSVアップロード機能を利用して
生徒データを一括で取り込むことができます。CSV には `name`, `grade`,
`teamwork`, `preferences` 列を含め、`preferences` は `A,B,C` のようにカンマ
区切りで記述します。

## 先生画面

`teacher.py` を実行すると、`shared_sheets` フォルダ内の Markdown を一覧表示します。
一覧は「氏名」「年月日」で表示され、シートを選択すると内容が Markdown として表示されます。

サンプルとして `shared_sheets/田中_2024-01-01.md` を同梱しています。
