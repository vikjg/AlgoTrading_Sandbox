def execute_paper_trade(symbol, df, signal, portfolio):
    price = df.iloc[-1]['close']
    if signal == 1:
        print(f"BUY {symbol} at {price}")
        portfolio[symbol]['position'] = price
    elif signal == -1:
        print(f"SELL {symbol} at {price}")
        pnl = price - portfolio[symbol]['position']
        portfolio[symbol]['balance'] += pnl
        portfolio[symbol]['position'] = 0
