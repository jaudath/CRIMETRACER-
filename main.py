#!/usr/bin/env python3
"""
CrimeTracer - Production-grade crime tracking system
Single entry point for the entire backend system
"""
import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Import our modules
from Backend.db import init_db, get_db_session
from Backend.models import Station, PoliceUser, Complaint
from Backend.auth_router import auth_router
from Backend.complaint_router import complaint_router
from Backend.stations_router import stations_router
from Backend.uploads_router import uploads_router
from Backend.ml_router import ml_router
from Backend.admin_router import admin_router
from Backend.stats_router import stats_router
from Backend.seed_stations import seed_stations_from_csv
from Backend.aws_utils import setup_cloudwatch_logging, check_all_aws_services_health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crimetracer.log', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs('logs', exist_ok=True)
os.makedirs('uploads/complaint_photos', exist_ok=True)
os.makedirs('uploads/attachments', exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup"""
    logger.info("Initializing CrimeTracer system...")
    
    # Setup CloudWatch logging if configured
    setup_cloudwatch_logging()
    
    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    logger.info("CrimeTracer shutting down...")

# Create FastAPI app
app = FastAPI(
    title="CrimeTracer API",
    description="Production-grade crime tracking system with AI-powered insights",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(complaint_router, prefix="/complaints", tags=["Complaints"])
app.include_router(stations_router, prefix="/stations", tags=["Police Stations"])
app.include_router(uploads_router, prefix="/uploads", tags=["File Uploads"])
app.include_router(ml_router, prefix="/ml", tags=["Machine Learning"])
app.include_router(admin_router, prefix="/admin", tags=["Administration"])
app.include_router(stats_router, prefix="/stats", tags=["Statistics"])

# Serve static files (fallback for local uploads when S3 not configured)
if os.path.exists("uploads"):
    app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "CrimeTracer API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check database connection
        async with get_db_session() as session:
            result = await session.execute("SELECT 1")
            db_status = "connected" if result else "disconnected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"
    
        # Get comprehensive AWS health status
        aws_health = check_all_aws_services_health()
        
        return {
            "success": True,
            "data": {
                "database": db_status,
                "gemini_ai": "configured" if os.getenv("GEMINI_API_KEY") else "fallback_mock",
                "ml_models": "loaded" if Path("models/xgb_classifier.model").exists() else "fallback_rules",
                **aws_health  # Include all AWS service statuses
            }
        }

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="CrimeTracer Backend System")
    parser.add_argument(
        "--seed-stations", 
        type=str, 
        help="Path to officer roster CSV file for seeding stations"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the server on"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        default=1, 
        help="Number of worker processes"
    )
    return parser.parse_args()

async def seed_stations_if_provided(csv_path: str):
    """Seed stations from CSV if path provided"""
    if csv_path and os.path.exists(csv_path):
        logger.info(f"Seeding stations from {csv_path}")
        try:
            await seed_stations_from_csv(csv_path)
            logger.info("Station seeding completed successfully")
        except Exception as e:
            logger.error(f"Failed to seed stations: {e}")
            sys.exit(1)
    elif csv_path:
        logger.error(f"CSV file not found: {csv_path}")
        sys.exit(1)

def main():
    """Main entry point"""
    args = parse_args()
    
    logger.info("Starting CrimeTracer Backend System")
    logger.info(f"Host: {args.host}, Port: {args.port}")
    
    # Handle station seeding if requested
    if args.seed_stations:
        logger.info(f"Station seeding requested: {args.seed_stations}")
        # Run seeding in asyncio context
        asyncio.run(seed_stations_if_provided(args.seed_stations))
        return
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()