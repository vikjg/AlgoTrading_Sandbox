import pandas as pd
import ccxt
from utils.data_loader import fetch_ohlcv_to_csv
from indicators.technicals import add_all_indicators
import utils.ohlcv_plots as plts
#from strategies.ema_crossover import generate_signals
from strategies.bollinger_rsi import generate_signals
from backtest.rudimentary_backtests import rude_backtest, plot_backtest

if __name__ == "__main__":
    kraken = ccxt.kraken()
    fetch_ohlcv_to_csv(
        exchange=kraken,
        symbol='BTC/USD',
        timeframe='1h',
        since='2023-01-01T00:00:00Z',
        output_path='data/btc_usd_1h.csv'
    )
    # fetch_ohlcv_to_csv(
    #     exchange=kraken,
    #     symbol='ETH/USD',
    #     timeframe='1h',
    #     since='2023-01-01T00:00:00Z',
    #     output_path='data/eth_usd_1h.csv'
    # )
    df_btc = pd.read_csv("data/btc_usd_1h.csv", parse_dates=['datetime'], index_col=['datetime'])
    #df_eth = pd.read_csv("data/eth_usd_1h.csv", parse_dates=['datetime'], index_col=['datetime'])
    add_all_indicators(df_btc)
    #plts.plot_candles(df_btc)
    #plts.plot_smas_candles(df_btc)
    #plts.plot_rsi_macd(df_btc)
    #plts.plot_bollinger(df_btc)
    #plts.plot_ema(df_btc)
    generate_signals(df_btc)
    rude_backtest(df_btc)
    plot_backtest(df_btc)
