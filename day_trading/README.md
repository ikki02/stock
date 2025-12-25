# 環境構築
`% uv venv`  
`% source .venv/bin/activate`  
`% uv sync`  

# Pythonファイル説明
get_kabutan.py
- 市場(東証)と出来高で絞り込まれた、PTS市場の値上がり銘柄の一覧を取得する
- ローカルにcsv出力する
- 使い方: 使いたい関数だけコメントアウトを外して、`% uv run get_kabutan.py`

# ToDo
- Pagenationがうまくいってない
- 株探のassertつけたい
