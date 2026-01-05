import time
from datetime import datetime
from utils.data_loader import fetch_latest_ohlcv
from indicators.technicals import add_all_indicators
from strategies.ema_crossover import generate_signals
from live_trading.state_manager import check_last_signal, update_position
from live_trading.paper_broker import execute_paper_trade
from utils.ohlcv_plots import plot_ema

SYMBOL = 'BTC/USD'
TIMEFRAME = '1m'
WINDOW_SIZE = 150  # candles to keep in memory
state = {}
portfolio = {
    'BTC/USD': {'position': 0, 'balance': 1000.0}  # USD balance
}

while True:
    # 1. Fetch latest WINDOW_SIZE candles
    print(f"[{datetime.now()}] Pulling fresh data...")
    df = fetch_latest_ohlcv(SYMBOL, TIMEFRAME, limit=WINDOW_SIZE)
    print(f"Latest close: {df.iloc[-1]['close']}")

    # 2. Calculate indicators
    add_all_indicators(df)
    print(f"EMA_12: {df.iloc[-1]['EMA_12']} | EMA_26: {df.iloc[-1]['EMA_26']}")
    #plot_ema(df)
    df.to_csv('data/live_data.csv', index=False)

    # 3. Generate signal
    generate_signals(df)
    latest_signal = df.iloc[-1]['ema_signal']

    print(f"Signal: {latest_signal}")
    print(f"Previous signal: {check_last_signal(SYMBOL, state)}")
    
    # 4. Compare to previous signal
    if check_last_signal(SYMBOL, state) != latest_signal:
        print(f"Execute: {check_last_signal(SYMBOL, state) != latest_signal}")
        # 5. Paper trade if signal changed
        execute_paper_trade(SYMBOL, df, latest_signal, portfolio)
        update_position(SYMBOL, latest_signal, state)
    print(f"Simulated position: {portfolio[SYMBOL]}")
    # 6. Sleep until next candle
    #time.sleep(60 * 60)  # sleep for 1h; change if using 1m or 5m
    time.sleep(30)  # sleep for 1h; change if using 1m or 5m
