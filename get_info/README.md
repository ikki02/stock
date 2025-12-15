CheckTechnicalBlocker.py
- 銘柄を指定して、テクニカル指標(PER, PBR, 利回り, RSI, MACD, BB)を取得する
- 望ましくない値が得られた場合はWARNING出力する

VolumeSpike.py
- 出来高上昇銘柄を取得する
- テクニカル指標(PER, PBR, 利回り, RSI, MACD, BB)を関連づける
- slackに通知する

ToDo
- yfのダウンロード時、マルチインデックスの処理をする。
- CheckTechnicalBlocker.pyについて、libを読み込むようにする。
