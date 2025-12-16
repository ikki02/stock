from logging import getLogger

import yfinance as yf

from get_kabutan import get_kabutan_stocks
from lib.args import parse_args
from lib.slack import notify_slack
from lib.technical import *

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)


def main() -> None:
    args = parse_args()
    df_vol = get_kabutan_stocks(markets=["東Ｐ", "東Ｓ", "東Ｇ", "東E"])
    logger.info(f"今回の出来高急増銘柄(by株探)を{df_vol.shape[0]}件取得できました。")

    for index, row in df_vol.iterrows():
        symbol = row["コード"] + ".T"
        logger.info(symbol)
        df = yf.download(symbol, period="3mo", interval="1d")
        df.columns = df.columns.get_level_values(0) # 列が銘柄のマルチインデックスのため、この2段重ねのうち、列名（0番目）だけ残したい

        df = calc_rsi(df)
        df = calc_macd(df)
        df = calc_bb(df)

        df_latest = df.tail(1)
        datetime = df_latest.index[0].strftime("%Y-%m-%d %H:%M:%S")
        close = float(df_latest["Close"].iat[0])
        vol = float(df_latest["Volume"].iat[0])
        rsi = float(df_latest["RSI"].iat[0])
        macd = float(df_latest["MACD"].iat[0])
        bb_upper = float(df_latest["BB_Upper"].iat[0])
        bb_mid = float(df_latest["BB_Mid"].iat[0])
        bb_low = float(df_latest["BB_Lower"].iat[0])

        text = f"""
    ```
    日付      : {datetime}
    市場      : {row["市場"]}
    銘柄コード : {symbol}
    銘柄名    : {row["銘柄名"]}
    終値      : {close:.2f}
    出来高(Y!Finance)    : {int(vol)}
    出来高(株探): {row["出来高"]}
    出来高前日比率: {row["出来高前日比率"]}
    PER      : {row["PER"]}
    PBR      : {row["PBR"]}
    利回り      : {row["利回り"]}
    RSI       : {rsi:.1f}
    MACD      : {macd:.3f}
    BB Upper  : {bb_upper:.2f}
    BB Middle : {bb_mid:.2f}
    BB Lower  : {bb_low:.2f}
    ```
        """.strip()

        logger.info(text)
        notify_slack(url=args.slack_webhook_url, text=text)


if __name__ == "__main__":
    main()
