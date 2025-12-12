import argparse
from logging import getLogger
import matplotlib.pyplot as plt
import pandas as pd
import ta
import yfinance as yf

def check_technical_blocker(symbol:str):
    df = yf.download(symbol, period="6mo", interval="1d")
    
    logger = getLogger(__name__)
    
    df['Return'] = df['Close'].pct_change()
    
    df['VolMA5'] = df['Volume'].squeeze().rolling(window=5).mean()
    df['Vol_diff'] = df['Volume'].squeeze() - df['VolMA5']
    #assert df['Vol_diff'].tail(1).iloc[0] > 0
    logger.info(f"出来高の評価は{int(df['Vol_diff'].tail(1).iloc[0])}です。(5日間移動平均と比較)")
    
    # 移動平均線(SMA, Simple Moving Average)
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_25'] = df['Close'].rolling(window=25).mean()
    
    close=df['Close'].squeeze()
    df['RSI'] = ta.momentum.RSIIndicator(close=close).rsi()
    df['MACD'] = ta.trend.MACD(close=close).macd() # MACD = EMA(12)-EMA(26)
    df['BB_Upper'] = ta.volatility.BollingerBands(close=close).bollinger_hband()
    df['BB_Lower'] = ta.volatility.BollingerBands(close=close).bollinger_lband()
    df['BB_Mid'] = ta.volatility.BollingerBands(close=close).bollinger_mavg()
    
    # ゴールデンクロス/デッドクロス検出
    df['GC_Signal'] = 0
    df.loc[df['SMA_5']>df['SMA_25'], 'GC_Signal'] = 1
    df.loc[df['SMA_5']<df['SMA_25'], 'GC_Signal'] = -1
    if int(df['GC_Signal'].tail(1).iloc[0]) == -1:
        logger.warning(f"デッドクロスが検出されました")
    
    df['RSI_Signal'] = 0
    df.loc[df['RSI']<30, 'RSI_Signal'] = 1 
    df.loc[df['RSI']>70, 'RSI_Signal'] = -1
    if int(df['RSI_Signal'].tail(1).iloc[0]) == -1:
        logger.warning(f"RSIが70以上です")
    
    df['MACD_Signal'] = 0
    df.loc[df['MACD']>0, 'MACD_Signal'] = 1
    df.loc[df['MACD']<0, 'MACD_Signal'] = -1
    if int(df['MACD_Signal'].tail(1).iloc[0]) == -1:
        logger.warning(f"MACDが0以下です: {int(df['MACD'].tail(1).iloc[0])}")
    
    df['BB_Signal'] = 0
    df.loc[df['Close'].squeeze()<df['BB_Lower'], 'BB_Signal'] = 1 
    df.loc[df['Close'].squeeze()>df['BB_Upper'], 'BB_Signal'] = -1
    if int(df['BB_Signal'].tail(1).iloc[0]) == -1:
        logger.warning(f"BB_Upper以上の値上がりです")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, help="symbol such as 3315.T")
    args = parser.parse_args()
    print("Received arguments {}".format(args))
    symbol = args.symbol
    check_technical_blocker(symbol)
