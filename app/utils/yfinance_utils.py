import yfinance as yf
import pandas as pd 

def fetch_from_yfinance(symbol: str):
    try:
        df = yf.download(symbol, period="1y", interval="1d").reset_index()
        print(df.head())
        print(type(df))

        # Flatten multi-level columns
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]


        if df.empty:
            print(f"No data returned for {symbol}")
            return []

        required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
        if not all(col in df.columns for col in required_cols):
            print(f"Missing columns in yfinance response for {symbol}: {df.columns}")
            return []

        return [
            {
                "date": pd.to_datetime(row["Date"]).date(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
            }
            for _, row in df.iterrows()
            if not any(pd.isna(row[col]) for col in ["Open", "High", "Low", "Close", "Volume"])
        ]
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")
        return []

def compute_technical_indicators(df: pd.DataFrame):
    df = df.copy()

    # SMA (Simple Moving Average)
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

def fetch_company_info(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "summary": info.get("longBusinessSummary"),
            "website": info.get("website"),
            "market_cap": info.get("marketCap"),
        }
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {}