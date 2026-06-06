import yfinance as yf
import pandas as pd

def get_prediction(ticker, impact_score, short_window=10, long_window=60):
    
    df = pd.DataFrame(yf.download(ticker, period="60d", interval="1d", auto_adjust=True))
    
    df['SMA_short'] = df['Close'].rolling(short_window).mean()
    df['SMA_long'] = df['Close'].rolling(long_window).mean()

    last_row = df.iloc[-1]

    short_MA = last_row['SMA_short'].item()
    long_MA  = last_row['SMA_long'].item()

    if pd.isna(short_MA) or pd.isna(long_MA):
        return "UNCERTAIN"

    if impact_score >= 0 and short_MA > long_MA:
        return "UP"

    elif impact_score <= 0 and short_MA < long_MA:
        return "DOWN"

    else:
        return "UNCERTAIN"



