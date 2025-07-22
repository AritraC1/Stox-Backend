from sqlalchemy.orm import Session
from app.models.company_info_model import CompanyInfoModel
from app.utils.yfinance_utils import fetch_company_info

DEFAULT_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "AMZN", "GOOGL",
    "INFY.NS", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ITC.NS"
]

def seed_company_info(db: Session, symbols: list[str] = DEFAULT_SYMBOLS) -> int:
    inserted = 0
    for symbol in symbols:
        info = fetch_company_info(symbol)
        if not info or not info.get("name"):
            continue

        company = CompanyInfoModel(
            symbol=symbol,
            name=info.get("name"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            exchange=None,  # yfinance doesn't provide this reliably
            summary=info.get("summary"),
            website=info.get("website"),
            market_cap=str(info.get("market_cap")) if info.get("market_cap") else None,
        )

        db.merge(company)  # upsert by primary key or unique symbol
        inserted += 1

    db.commit()
    return inserted