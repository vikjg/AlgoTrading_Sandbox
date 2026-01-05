

def generate_signals(df):
    df["ema_signal"] = 0
    df.loc[df["EMA_12"] > df["EMA_26"], "ema_signal"] = 1
    df.loc[df["EMA_12"] < df["EMA_26"], "ema_signal"] = -1
