from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_stock_data():
    response = client.get("/stocks/AAPL")
    assert response.status_code == 200
    assert isinstance(response.json(), list)