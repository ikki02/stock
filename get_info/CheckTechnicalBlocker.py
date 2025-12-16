from logging import getLogger

import yfinance as yf

from lib.args import parse_args
from lib.technical import *

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)


def main():
    args = parse_args()
    symbol = args.symbol
    logger.info(f"銘柄コード{symbol}のテクニカルを出力します。")
    df = yf.download(symbol, period="6mo", interval="1d")
    df.columns = df.columns.get_level_values(0) # 列が銘柄のマルチインデックスのため、この2段重ねのうち、列名（0番目）だけ残したい

    df["VolMA5"] = df["Volume"].rolling(window=5).mean()
    df["Vol_diff"] = df["Volume"] - df["VolMA5"]
    # assert df['Vol_diff'].tail(1).iloc[0] > 0
    logger.info(f"直近の出来高は{int(df['Volume'].iat[-1])}です。")
    logger.info(f"出来高の評価は{int(df['Vol_diff'].iat[-1])}です。(5日間移動平均と比較)")

    close = df["Close"]
    df["Return"] = close.pct_change()

    # 移動平均線(SMA, Simple Moving Average)
    df["SMA_5"] = close.rolling(window=5).mean()
    df["SMA_25"] = close.rolling(window=25).mean()
    # ゴールデンクロス/デッドクロス検出
    df["GC_Signal"] = 0
    df.loc[df["SMA_5"] > df["SMA_25"], "GC_Signal"] = 1
    df.loc[df["SMA_5"] < df["SMA_25"], "GC_Signal"] = -1
    if int(df["GC_Signal"].tail(1).iloc[0]) == -1:
        logger.warning("デッドクロスが検出されました")

    df = calc_rsi(df)
    df = calc_macd(df)
    df = calc_bb(df)


if __name__ == "__main__":
    main()
