# Pydantic response/request models

from pydantic import BaseModel
from datetime import date
from typing import Optional

class StockPriceSchema(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        from_attributes = True
        orm_mode = True

class TechnicalIndicatorSchema(BaseModel):
    date: date
    close: float
    sma_20: Optional[float]
    sma_50: Optional[float]
    rsi_14: Optional[float]
    macd: Optional[float]
    signal: Optional[float]

class CompanyInfoSchema(BaseModel):
    id: int
    symbol: Optional[str]
    name: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    summary: Optional[str]
    website: Optional[str]
    market_cap: Optional[float]

    class Config:
        from_attributes = True
        orm_mode = True
