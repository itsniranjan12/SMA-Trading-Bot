import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from ta.momentum import RSIIndicator
from data.MyFile import fetch_and_clean_ticker_data


def sma_rsi_crossover(data, short_window=20, long_window=50, rsi_window=14):
    # Calculate SMAs
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    
    # Ensure Close is a flat Series for RSI calculation
    close_series = pd.Series(data['Close'].values.ravel())
    
    # Calculate RSI using ta library
    rsi_indicator = RSIIndicator(close=close_series, window=rsi_window)
    data['RSI'] = rsi_indicator.rsi()
    
    data['Signal'] = 0
    data.loc[
        (data['SMA_Short'] > data['SMA_Long']) &
        (data['SMA_Short'].shift(1) <= data['SMA_Long'].shift(1)) &
        (data['RSI'] < 70),
        'Signal'
    ] = 1
    
    data.loc[
        (data['SMA_Short'] < data['SMA_Long']) &
        (data['SMA_Short'].shift(1) >= data['SMA_Long'].shift(1)) &
        (data['RSI'] > 30),
        'Signal'
    ] = -1
    
    return data

if __name__ == "__main__":
    tickers = ["AAPL", "GOOG", "TSLA", "AMZN", "META"]

    # Fetch cleaned data
    cleaned_data = fetch_and_clean_ticker_data(tickers)

    # Apply strategy to each
    for ticker in tickers:
        if ticker in cleaned_data:
            df = cleaned_data[ticker]
            result = sma_rsi_crossover(df)
            print(f"\n{ticker} Signals:")
            print(result[['Date', 'Close', 'SMA_Short', 'SMA_Long', 'RSI', 'Signal']].tail())



