import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
import os
warnings.filterwarnings('ignore')
os.chdir(os.path.dirname(os.path.abspath(__file__)))


stocks = {
    'Apple':     'AAPL',
    'Google':    'GOOGL',
    'Microsoft': 'MSFT',
    'Tesla':     'TSLA'
}

period = '6mo' 

print("Downloading stock data...")
data = {}
data = {}
for name, ticker in stocks.items():
    df = yf.download(ticker, period=period, progress=False)
    close = df['Close']
    if hasattr(close, 'squeeze'):
        close = close.squeeze()
    data[name] = close
    print(f"✅ {name} ({ticker}) — {len(df)} trading days loaded")

combined = pd.concat(data, axis=1)
combined.columns = list(stocks.keys())
combined.dropna(inplace=True)


combined = pd.DataFrame(data)
print("\nSample data:")
print(combined.tail())

normalized = (combined / combined.iloc[0]) * 100


plt.figure(figsize=(12, 6))
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
for (name, series), color in zip(normalized.items(), colors):
    plt.plot(series.index, series.values, label=name, color=color, linewidth=2)

plt.title('Stock Performance Comparison (Last 6 Months)', fontsize=15)
plt.xlabel('Date')
plt.ylabel('Normalized Price (Base = 100)')
plt.legend(fontsize=11)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('stock_comparison.png')
print("\nStock comparison chart saved!")

ticker_name = 'Apple'
stock_df = combined[ticker_name].to_frame(name='Close')
stock_df['MA20']  = stock_df['Close'].rolling(window=20).mean()
stock_df['MA50']  = stock_df['Close'].rolling(window=50).mean()

plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['Close'],
         label='Close Price', color='#3498db', linewidth=1.5)
plt.plot(stock_df.index, stock_df['MA20'],
         label='20-Day MA',   color='#e74c3c', linewidth=1.5, linestyle='--')
plt.plot(stock_df.index, stock_df['MA50'],
         label='50-Day MA',   color='#2ecc71', linewidth=1.5, linestyle='--')

plt.title(f'{ticker_name} Stock Price with Moving Averages', fontsize=15)
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend(fontsize=11)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('apple_moving_averages.png')
print("Moving averages chart saved!")

apple_full = yf.download('AAPL', period=period, progress=False)
plt.figure(figsize=(12, 4))
plt.bar(apple_full.index, apple_full['Volume'].squeeze(),
        color='#9b59b6', alpha=0.7, width=1)
plt.title('Apple Trading Volume (Last 6 Months)', fontsize=15)
plt.xlabel('Date')
plt.ylabel('Volume')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('apple_volume.png')
print("Volume chart saved!")

print("\n--- 6 Month Performance Summary ---")
for name, series in combined.items():
    start  = series.iloc[0]
    end    = series.iloc[-1]
    change = ((end - start) / start) * 100
    emoji  = "📈" if change > 0 else "📉"
    print(f"{emoji} {name}: ${start:.2f} → ${end:.2f} ({change:.1f}%)")

print("\nDone! Check your folder for all 3 charts.")