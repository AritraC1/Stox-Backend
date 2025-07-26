from typing import List
from fastapi import APIRouter, Depends
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

# charts
@router.get("/stocks/{symbol}/chart-data")
def get_chart_data(symbol: str, db: Session = Depends(get_db)):
    try:
        data = get_technical_indicators(symbol, db)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Paginated stock ticker/company info list
@router.get("/stocks", response_model=list[CompanyInfoSchema])
def list_stocks(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    companies = db.query(CompanyInfoModel).offset(offset).limit(limit).all()

    if not companies:
        seed_company_info(db)  # fallback populate
        companies = db.query(CompanyInfoModel).offset(offset).limit(limit).all()

    return companies

# Route for Bulk Historical Data Fetching
@router.post("/stocks/bulk", response_model=dict)
def fetch_bulk_stock_data(symbols: List[str], db: Session = Depends(get_db)):
    results = {}
    for symbol in symbols:
        try:
            data = get_stock_data(symbol, db)
            results[symbol] = data
        except Exception as e:
            results[symbol] = {"error": str(e)}
    return results
