from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as stock_router
from app.db.database import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Market Dashboard API",
    version="1.0.0"
)

# CORS Middleware (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(stock_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Stock Market API is running 🚀"}

