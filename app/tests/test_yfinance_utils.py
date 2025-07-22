from app.utils.yfinance_utils import fetch_from_yfinance

def test_fetch_from_yfinance():
    data = fetch_from_yfinance("AAPL")
    assert isinstance(data, list)
    assert all("date" in d for d in data)