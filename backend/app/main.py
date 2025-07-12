# AI Engineer Progress Tracker Backend
# FastAPI backend optimized for Railway.app deployment

import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.utils.config import get_config
from app.utils.tasks import cleanup_old_data
from app.api import progress, analytics
from app.models.database import db_manager

# Load configuration
config = get_config()
logger = config.logger  # App-level logger


# FastAPI app with lifespan management
@asynccontextmanager
async def lifespan(
    app: FastAPI,
):  # pylint: disable=redefined-outer-name,unused-argument
    logger.info("Starting AI Progress Tracker API...")
    # Initialize database
    await db_manager.initialize()

    # Start background tasks
    asyncio.create_task(cleanup_old_data())

    yield

    # Cleanup
    await db_manager.close()
    logger.info("Shutting down API Progress Tracker API...")


app = FastAPI(
    title="AI Engineer Progress Tracker API",
    description="Backend API for tracking AI engineering learning progress",
    version="1.0.0",
    debug=config.api.debug,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(progress.router, prefix="/api", tags=["progress"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])


@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "message": "AI Engineer Progress Tracker API",
        "version": "1.0.0",
        "environment": config.env.name,
        "debug": config.api.debug,
    }


@app.get("/config")
async def get_frontend_config():
    """Endpoint to provide frontend configuration"""
    return config.frontend


@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Test database connection
        db_status = "connected" if db_manager.pool else "file_based"

        # Check disk space (for file-based storage)
        import shutil

        disk_usage = shutil.disk_usage(".")
        free_space_gb = disk_usage.free / (1024**3)

        return {
            "status": "healthy",
            "database": db_status,
            "free_space_gb": round(free_space_gb, 2),
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.debug,
    )
