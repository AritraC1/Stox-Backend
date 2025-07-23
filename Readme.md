# Stox: Stocks Dashboard Backend
**Stox** is the backend service for a stock market dashboard application. It delivers real-time and historical financial data, personalized user features, and efficient data caching. Built with performance and scalability in mind.

## Features

- Real-time and historical stock data via yFinance
- Company info and market insights
- Watchlist and preferences management
- Redis-based caching to reduce API overhead
- Technical indicators (e.g. SMA, EMA, RSI)
- Bulk data fetching support
- Paginated ticker listing
- Auto-generated Swagger & ReDoc documentation

## Tech Stack

- **Python 3.10+**
- **FastAPI** – High-performance Python web framework
- **PostgreSQL** – Relational database for user and stock metadata
- **Redis** – In-memory data store for caching and real-time updates
- **yFinance** – Yahoo Finance API wrapper for stock data
- **SQLAlchemy** – ORM for database interaction
- **Pydantic** – For request/response validation

## End Points

```http
# Stock Data (via yFinance)
GET    /api/stocks/{symbol}              # Get real-time stock price data
POST   /api/stocks/bulk                  # Fetch real-time data for multiple symbols
GET    /api/stocks/{symbol}/history      # Get historical stock data (assumed from initial docs)

# Technical Analysis
GET    /api/stocks/{symbol}/indicators   # Get technical indicators (SMA, EMA, RSI, etc.)
GET    /api/stocks/{symbol}/chart-data   # Get chart data for plotting (from indicators)

# Company Info
GET    /api/stocks/{symbol}/info         # Get company metadata and profile
GET    /api/tickers?page=1&limit=10      # Paginated company/ticker listing
```

## Documentation
Stox provides auto-generated API documentation to help developers explore and interact with the available endpoints:

**Swagger UI**: Interactive API docs
Visit: [Swagger Docs]()

**ReDoc**: Clean and customizable API reference
Visit: [ReDoc]()

**OpenAPI Spec (JSON)**: Full OpenAPI schema definition reference
Visit: [OpenAPI Spec]()

## Setup Instructions
```bash
# Clone the repo
git clone https://github.com/AritraC1/Stox-Backend.git
cd stox

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup env file
DATABASE_URL=postgresql://username:password@localhost:5432/stock_db
REDIS_HOST=localhost # for local development, change it accordingly
REDIS_PORT=6379 #Redis default port

# Run the app
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001

```