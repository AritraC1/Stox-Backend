from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class CompanyInfoModel(Base):
    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String)
    industry = Column(String)
    exchange = Column(String)
    summary = Column(Text)
    website = Column(String)
    market_cap = Column(String)