import pytest
from unittest.mock import MagicMock, patch
from app.services.stock_service import get_stock_data
from app.models import model
from app.models.schemas import StockPriceSchema
import datetime

@pytest.fixture
def fake_stock_data():
    return [
        {
            "date": datetime.date(2024, 7, 19),
            "open": 100.0,
            "high": 110.0,
            "low": 95.0,
            "close": 105.0,
            "volume": 1500000,
        }
    ]

def test_get_stock_data_from_db(fake_stock_data):
    # Mock database session and data
    mock_db = MagicMock()
    stock_row = model.StockPrice(symbol="AAPL", **fake_stock_data[0])
    mock_db.query().filter().all.return_value = [stock_row]

    result = get_stock_data("AAPL", db=mock_db)

    assert isinstance(result, list)
    assert isinstance(result[0], StockPriceSchema)
    assert result[0].symbol == "AAPL"

@patch("app.services.stock_service.redis_client.get")
@patch("app.services.stock_service.redis_client.set")
@patch("app.services.stock_service.fetch_from_yfinance")
def test_get_stock_data_from_yfinance(mock_yf, mock_redis_set, mock_redis_get, fake_stock_data):
    mock_redis_get.return_value = None  # no cache
    mock_yf.return_value = fake_stock_data

    mock_db = MagicMock()
    mock_db.query().filter().all.return_value = []

    result = get_stock_data("GOOG", db=mock_db)

    assert len(result) == 1
    assert result[0].close == 105.0
    mock_redis_set.assert_called_once()
