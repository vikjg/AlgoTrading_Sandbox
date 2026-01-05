import mplfinance as mpf
import pandas as pd

# more data to be found here https://www.kaggle.com/code/carlmcbrideellis/plotting-ohlc-and-v-ticker-data-using-mplfinance

def plot_candles(df):
    mpf.plot(df[-100:], type='candle', volume=True, style='charles')

def plot_smas_candles(df):
    smas = [df["SMA_20"], df["SMA_50"]]
    mpf.plot(df[-100:], type='candle', volume=True, style='charles', mav=(20, 50))


def plot_rsi_macd(df):
    apds = [
        mpf.make_addplot(df["SMA_20"][-150:], color='blue'),
        mpf.make_addplot(df["SMA_50"][-150:], color='red'),
        mpf.make_addplot(df["RSI_14"][-150:], panel=1, color='purple', ylabel='RSI'),
        mpf.make_addplot(df["MACD"][-150:], panel=2, color='green', ylabel='MACD'),
        mpf.make_addplot(df["Signal"][-150:], panel=2, color='orange')
    ]
    mpf.plot(df[-150:], type='candle', style='charles', volume=True, addplot=apds, panel_ratios=(2,1,1))

def plot_ema(df):
    apds = [
        mpf.make_addplot(df["EMA_12"][-150:], color='blue'),
        mpf.make_addplot(df["EMA_26"][-150:], color='red'),
    ]
    mpf.plot(df[-150:], type='candle', style='charles', volume=True, addplot=apds)

def plot_bollinger(df):
    apds = [
        mpf.make_addplot(df["BB_Middle"][-150:], color='blue'),
        mpf.make_addplot(df["BB_StdDev"][-150:], color='red'),
        mpf.make_addplot(df["BB_Upper"][-150:], color='purple'),
        mpf.make_addplot(df["BB_Lower"][-150:], color='green'),
    ]
    mpf.plot(df[-150:], type='candle', style='charles', volume=True, addplot=apds)