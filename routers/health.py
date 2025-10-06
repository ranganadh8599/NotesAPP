"""Health check and status routes."""

from datetime import datetime, timezone
from fastapi import APIRouter

from database import DatabaseManager


router = APIRouter(tags=["Health"])
db = DatabaseManager()


@router.get("/", summary="Root endpoint")
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns basic information about the API including version and database type.
    """
    return {
        "message": "Notes API is running",
        "version": "1.0.0",
        "database": "MySQL"
    }


@router.get("/health", summary="Health check endpoint")
async def health_check():
    """
    Health check endpoint for monitoring API status.
    
    Checks database connectivity and returns overall system health status.
    Useful for load balancers and monitoring systems.
    """
    db_status = "connected" if db.test_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }