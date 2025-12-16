import logging

import pandas as pd
import ta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calc_rsi(df: pd.DataFrame) -> pd.DataFrame:
    """
    終値からRSIを計算する
    計算式
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    Args:
        df: 終値を持つDataFrame

    Returns:
        RSI列(Signal付き)を追加したDataFrame
    """
    close = df["Close"]
    df["RSI"] = ta.momentum.RSIIndicator(close=close).rsi()

    df["RSI_Signal"] = 0
    df.loc[df["RSI"] < 30, "RSI_Signal"] = 1
    df.loc[df["RSI"] > 70, "RSI_Signal"] = -1
    if int(df["RSI_Signal"].tail(1).iloc[0]) == -1:
        logger.warning("RSIが70以上です")

    return df


def calc_macd(df: pd.DataFrame) -> pd.DataFrame:
    """
    終値からMACDを計算する。# MACD = EMA(12)-EMA(26)

    Args:
        df: 終値を持つDataFrame

    Returns:
        MACD列(Signal付き)を追加したDataFrame
    """
    close = df["Close"]
    df["MACD"] = ta.trend.MACD(close=close).macd()

    df["MACD_Signal"] = 0
    df.loc[df["MACD"] > 0, "MACD_Signal"] = 1
    df.loc[df["MACD"] < 0, "MACD_Signal"] = -1
    if int(df["MACD_Signal"].tail(1).iloc[0]) == -1:
        logger.warning(f"MACDが0以下です: {int(df['MACD'].tail(1).iloc[0])}")

    return df


def calc_bb(df: pd.DataFrame) -> pd.DataFrame:
    """
    終値からBB(ボリンジャーバンド)を計算する。
    計算式
    df['BB_Mid20'] = df['Close'].rolling(window=20).mean()
    df['BB_STD20'] = df['Close'].rolling(window=20).std()

    df['BB_Upper'] = df['BB_Mid20'] + 2 * df['BB_STD20']
    df['BB_Lower'] = df['BB_Mid20'] - 2 * df['BB_STD20']

    Args:
        df: 終値を持つDataFrame

    Returns:
        BB列(Signal付き)を追加したDataFrame
    """
    close = df["Close"]
    df["BB_Upper"] = ta.volatility.BollingerBands(close=close).bollinger_hband()
    df["BB_Lower"] = ta.volatility.BollingerBands(close=close).bollinger_lband()
    df["BB_Mid"] = ta.volatility.BollingerBands(close=close).bollinger_mavg()

    df["BB_Signal"] = 0
    df.loc[df["Close"].squeeze() < df["BB_Lower"], "BB_Signal"] = 1
    df.loc[df["Close"].squeeze() > df["BB_Upper"], "BB_Signal"] = -1
    if int(df["BB_Signal"].tail(1).iloc[0]) == -1:
        logger.warning("BB_Upper以上の値上がりです")

    return df
