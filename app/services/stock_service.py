import numpy as np
import pandas as pd
import yfinance as yf
from app.db.redis_client import redis_client
from app.utils.yfinance_utils import fetch_from_yfinance
from app.models import model
from app.models.schemas import StockPriceSchema
from sqlalchemy.orm import Session
import json

def get_stock_data(symbol: str, db: Session):
    # 1. Check DB
    db_data = db.query(model.StockPrice).filter(model.StockPrice.symbol == symbol).all()
    if db_data:
        return [StockPriceSchema.from_orm(row) for row in db_data]

    # 2. Check Redis
    cache_key = f"stock:{symbol.upper()}"
    cached = redis_client.get(cache_key)
    if cached:
        try:
            cached_data = json.loads(cached)
            return [StockPriceSchema(**entry) for entry in cached_data]
        except Exception:
            redis_client.delete(cache_key)  # remove corrupted cache

    # 3. Fetch fresh
    fresh_data = fetch_from_yfinance(symbol)
    if not fresh_data:
        return []

    # 4. Save to DB
    save_stock_data_to_db(symbol, fresh_data, db)

    # 5. Save to cache
    redis_client.set(cache_key, json.dumps(fresh_data), ex=43200)

    return [StockPriceSchema(**entry) for entry in fresh_data]


def save_stock_data_to_db(symbol: str, data: list[dict], db: Session):
    for entry in data:
        stock = model.StockPrice(
            symbol=symbol.upper(),
            date=entry["date"],
            open=entry["open"],
            high=entry["high"],
            low=entry["low"],
            close=entry["close"],
            volume=entry["volume"],
        )
        db.merge(stock)  # merge handles insert or update
    db.commit()

def get_technical_indicators(symbol: str, db: Session):
    data = get_stock_data(symbol, db)
    df = pd.DataFrame([d.dict() for d in data])

    df.sort_values("date", inplace=True)
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()

    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    df["ema_12"] = df["close"].ewm(span=12).mean()
    df["ema_26"] = df["close"].ewm(span=26).mean()
    df["macd"] = df["ema_12"] - df["ema_26"]
    df["signal"] = df["macd"].ewm(span=9).mean()

    # Fix for JSON serialization issues
    df = df.replace([np.nan, np.inf, -np.inf], None)

    return df[["date", "close", "sma_20", "sma_50", "rsi_14", "macd", "signal"]].to_dict(orient="records")

def get_company_info(symbol: str):
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
        print(f"Error fetching company info for {symbol}: {e}")
        return {}
