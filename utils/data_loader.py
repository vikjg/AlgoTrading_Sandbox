import ccxt
import pandas as pd
import time
import os
from datetime import datetime

def fetch_ohlcv_to_csv(exchange, symbol, timeframe, since, output_path):
    all_ohlcv = []
    since_ms = exchange.parse8601(since)
    limit = 720  # Kraken's hourly max limit is ~720 for 1h (~30 days)
    
    while True:
        print(f"Fetching candles starting from: {exchange.iso8601(since_ms)}")
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_ms, limit)
        
        if not ohlcv:
            break

        all_ohlcv += ohlcv
        since_ms = ohlcv[-1][0] + 1  # next candle

        time.sleep(exchange.rateLimit / 1000)  # rate limiting

        if len(ohlcv) < limit:
            break

    df = pd.DataFrame(all_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("datetime", inplace=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"Saved {len(df)} candles to {output_path}")

def fetch_latest_ohlcv(symbol, timeframe='1h', limit=200):
    exchange = ccxt.kraken()
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
   
