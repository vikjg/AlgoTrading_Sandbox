import backtrader as bt
import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch data using yfinance
data_df = yf.download('RELIANCE.NS', start='2022-01-01', end='2025-01-01', multi_level_index=False)

# Create a custom pandas feed to use with Backtrader
class PandasData(bt.feeds.PandasData):
    params = (
        ('fromdate', datetime.datetime(2022, 1, 1)),
        ('todate', datetime.datetime(2025, 1, 1)),
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
        ('openinterest', None),  # No open interest in Yahoo data
    )

# Define the EMA Crossover Strategy
class EmaCrossStrategy(bt.Strategy):
    params = (('short_period', 10), ('long_period', 20),)

    def __init__(self):
        # Initialize the 10-day and 20-day EMA indicators
        self.ema_short = bt.indicators.EMA(self.data.close, period=self.params.short_period)
        self.ema_long = bt.indicators.EMA(self.data.close, period=self.params.long_period)
        self.trade_list = []  # To keep track of trades

    def next(self):
        if not self.position:  # Check if we are not in a position
            if self.ema_short > self.ema_long:  # Buy if short EMA crosses above long EMA
                self.buy()
        else:
            if self.ema_short < self.ema_long:  # Sell if short EMA crosses below long EMA
                self.sell()

    def notify_trade(self, trade):
        if trade.isclosed:
            exit_price = None
            if trade.size != 0:
                exit_price = trade.price + trade.pnlcomm / trade.size  # Calculate exit price
            else:
                exit_price = trade.price  # Set exit price to entry price if size is zero (or handle as needed)

            # Log the trade details when a trade is closed
            trade_details = {
                'Entry Price': trade.price,  # Entry price of the trade
                'Exit Price': exit_price,  # Calculated exit price
                'Size': trade.size,  # Size of the trade
                'Profit/Loss': trade.pnlcomm  # Net PnL after commission
            }
            self.trade_list.append(trade_details)


    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy Executed: Price: {order.executed.price}, Size: {order.executed.size}")
            elif order.issell():
                print(f"Sell Executed: Price: {order.executed.price}, Size: {order.executed.size}")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print("Order Failed")

    def stop(self):
        # Print list of trades
        print("List of Trades:")
        for trade in self.trade_list:
            print(trade)
        print("\n")

# Create an instance of Cerebro engine
cerebro = bt.Cerebro()

# Add the strategy to Cerebro
cerebro.addstrategy(EmaCrossStrategy)

# Convert the DataFrame into a Backtrader-compatible data feed
data_feed = PandasData(dataname=data_df)

# Add the data feed to Cerebro
cerebro.adddata(data_feed)

# Set initial capital and commissions
cerebro.broker.setcash(300000)  # Rs 3,00,000 starting capital
cerebro.broker.setcommission(commission=0.002 / 100)  # 0.002% commission on turnover

# Print the starting portfolio value
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run the backtest
results = cerebro.run()

# Print the final portfolio value
final_value = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % final_value)

# Calculate Profit/Loss and other metrics
profit_loss = final_value - 300000
print('Net Profit/Loss: %.2f' % profit_loss)

# Plot the results
fig = cerebro.plot() #iplot=False)[0][0]
plt.show()
