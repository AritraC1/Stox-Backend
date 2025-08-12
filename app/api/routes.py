import yfinance as yf
from typing import List, Dict
import re
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.company_info_model import CompanyInfoModel
from app.services.company_seed import seed_company_info
from app.services.stock_service import get_company_info, get_stock_data, get_technical_indicators
from app.models.schemas import CompanyInfoSchema, StockPriceSchema, TechnicalIndicatorSchema
from app.services.stock_service import get_technical_indicators as calculate_indicators

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# YFinance - Historical Data & recent stock prices
@router.get("/stocks/{symbol}", response_model=list[StockPriceSchema])
def fetch_stock(symbol: str, db: Session = Depends(get_db)):
    return get_stock_data(symbol, db)

# Technical Indicators
@router.get("/stocks/{symbol}/indicators", response_model=list[TechnicalIndicatorSchema])
def fetch_indicators(symbol: str, db: Session = Depends(get_db)):
    return calculate_indicators(symbol, db)

# Company Info
@router.get("/stocks/{symbol}/info")
def fetch_company_info(symbol: str):
    return get_company_info(symbol)

# Paginated stock ticker/company info list
@router.get("/stocks", response_model=list[CompanyInfoSchema])
def list_stocks(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    companies = db.query(CompanyInfoModel).offset(offset).limit(limit).all()

    if not companies:
        seed_company_info(db)  # fallback populate
        companies = db.query(CompanyInfoModel).offset(offset).limit(limit).all()

    return companies

# Get historical price data
def get_price_history(symbol: str):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="6mo", interval="1mo")
    history = [
        {"month": str(idx.strftime("%b %Y")), "price": row["Close"]}
        for idx, row in hist.iterrows()
    ]

    return history

# Get Logo URL
def get_logo_url(website: str) -> str:
    if website:
        # Extract domain from URL
        domain_match = re.search(r"https?://(www\.)?([^/]+)", website)
        if domain_match:
            domain = domain_match.group(2)
            return f"https://logo.clearbit.com/{domain}"
    return ""

# get stock data
def fetch_stock_data(symbol: str) -> Dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    if "shortName" not in info:
        raise ValueError(f"No data found for symbol: {symbol}")

    return {
        "symbol": symbol.upper(),
        "companyName": info.get("shortName", ""),
        "logo": get_logo_url(info.get("website", "")),
        "revenue": info.get("totalRevenue", None),
        "marketCap": info.get("marketCap", None),
    }


@router.get("/compare")
def compare_stocks(stock1: str = Query(...), stock2: str = Query(...)):
    try:
        data1 = fetch_stock_data(stock1)
        data2 = fetch_stock_data(stock2)

        # Calculate price change percentage
        for stock in [data1, data2]:
            prev = stock.get("previousClose", 0)
            curr = stock.get("price", 0)
            if prev:
                stock["change"] = round(((curr - prev) / prev) * 100, 2)
            else:
                stock["change"] = 0.0
            stock["history"] = get_price_history(stock["symbol"])

        return {
            "overview": [data1, data2],
            "priceData": [data1, data2],
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get All tickers
