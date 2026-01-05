def compute_rsi(series, period=14):
   delta = series.diff()
   gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
   loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
   rs = gain / loss
   return 100 - (100 / (1 + rs))   

def add_all_indicators(df):
    df["SMA_20"] = df["close"].rolling(window=20).mean()
    df["SMA_50"] = df["close"].rolling(window=50).mean()
    df["RSI_14"] = compute_rsi(df["close"])
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["EMA_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["BB_Middle"] = df["close"].rolling(window=20).mean()
    df["BB_StdDev"] = df["close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Middle"] + (2 * df["BB_StdDev"])
    df["BB_Lower"] = df["BB_Middle"] - (2 * df["BB_StdDev"])