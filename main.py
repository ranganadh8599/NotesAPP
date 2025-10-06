"""Main FastAPI application file for the Notes API."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from database import DatabaseManager
from routers import auth, notes, health
from config import settings

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    print("Starting Notes API...")
    try:
        # Initialize the database manager
        db = DatabaseManager()
        
        # Initialize database (create tables if they don't exist)
        db.initialize_database()
        
        # Test the connection
        if db.test_connection():
            print("Database connection established successfully")
        else:
            raise Exception("Database connection test failed")
        
        yield
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise
    finally:
        print("Shutting down Notes API...")


# Create the FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(notes.router)


# Development server entry point
def run_development_server():
    """Run the development server using uvicorn."""
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    run_development_server()
