# 環境構築
uv sync

# Pythonファイル説明
CheckTechnicalBlocker.py
- 銘柄を指定して、テクニカル指標(PER, PBR, 利回り, RSI, MACD, BB)を取得する
- 望ましくない値が得られた場合はWARNING出力する
- 使い方: uv run CheckTechnicalBlocker.py --symbol=7992.T

VolumeSpike.py
- 出来高上昇銘柄(東証、上昇株)を取得する
- テクニカル指標(PER, PBR, 利回り, RSI, MACD, BB)を関連づける
- slackに通知する
- 使い方: slackの環境変数設定後、uv run VolumeSpike.py

get_kabutan.py
- PTS市場の株価上昇率ランキング(東証)を取得する
- 出来高絞り込み
- ローカルにcsv出力する
- 使い方: 使いたい関数だけコメントアウトを外して、uv run get_kabutan.py

# ToDo
- 株探のassertつけたい
