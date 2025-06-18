# visionwell-da

高校推薦枠マッチングシステムのサンプルアプリです。CSVアップロード機能を利用して
生徒データや学校データを一括で取り込むことができます。

## 学生CSV
`name`, `grade`, `teamwork`, `preferences` 列を含め、`preferences` は `A,B,C` のようにカンマ区切りで記述します。

## 学校CSV
`name`, `capacity`, `grade_weight`, `teamwork_weight` の4列を用意します。`grade_weight`
と `teamwork_weight` はそれぞれ評定と協調性の重みです。
