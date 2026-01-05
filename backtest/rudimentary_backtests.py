import pandas
import matplotlib.pyplot as plt

def rude_backtest(df):
    # Forward fill signals for holding period simulation
    #df["position"] = df["ema_signal"].shift(1)  # shift so we don't trade on the same candle
    df["position"] = df["bb_rsi_signal"].shift(1)  # shift so we don't trade on the same candle

    # Strategy returns
    df["strategy_return"] = df["position"] * df["close"].pct_change()

    # Cumulative returns
    df["cumulative_strategy"] = (1 + df["strategy_return"]).cumprod()
    df["cumulative_market"] = (1 + df["close"].pct_change()).cumprod()

def plot_backtest(df):
    plt.figure(figsize=(12,6))
    plt.plot(df["cumulative_strategy"], label="Strategy")
    plt.plot(df["cumulative_market"], label="Market (HODL)")
    plt.legend()
    plt.grid(True)
    plt.show()
