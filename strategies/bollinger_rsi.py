
def generate_signals(df):
    df["bb_rsi_signal"] = 0
    df.loc[(df["close"] < df["BB_Lower"]) & (df["RSI_14"] < 30), "bb_rsi_signal"] = 1
    df.loc[(df["close"] > df["BB_Upper"]) & (df["RSI_14"] > 70), "bb_rsi_signal"] = -1
