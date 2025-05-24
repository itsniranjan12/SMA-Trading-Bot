import pandas as pd
import yfinance as yf
import os

def fetch_and_clean_ticker_data(tickers, period='1y', save_folder='data'):
    os.makedirs(save_folder, exist_ok=True)
    data_dict = {}
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        data = yf.download(ticker, period=period, threads=False, progress=False)
        if data.empty:
            print(f"No data for {ticker}")
            continue
            
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data = data.rename(columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume"
        })
        
        data = data[["Date", "Close", "High", "Low", "Open", "Volume"]]
        data['Close'] = data['Close'].values.flatten()
        
        for col in data.columns:
            if col != "Volume" and pd.api.types.is_numeric_dtype(data[col]):
                data[col] = data[col].round(2)
        
        file_path = os.path.join(save_folder, f"{ticker}.csv")
        data.to_csv(file_path, index=False, date_format='%Y-%m-%d')    
        print(f"Data saved to {file_path}")
        
        data_dict[ticker] = data
    
    return data_dict

if __name__ == "__main__":
    tickers = ["AAPL", "GOOG", "TSLA", "AMZN", "META"]
    fetch_and_clean_ticker_data(tickers)

