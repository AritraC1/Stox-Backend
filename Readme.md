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
GET    /api/stocks/{symbol}          # Get real-time stock data
GET    /api/stocks/{symbol}/history  # Get historical stock data
POST   /api/auth/register            # Register a new user
POST   /api/auth/login               # Login and receive JWT token
GET    /api/user/watchlist           # Get user watchlist
POST   /api/user/watchlist           # Add a stock to watchlist
DELETE /api/user/watchlist/{symbol}  # Remove a stock from watchlist
```