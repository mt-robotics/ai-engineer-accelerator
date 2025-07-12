from datetime import datetime, timedelta
from app.models.database import db_manager
from app.utils.config import get_logger

logger = get_logger(__name__)  # Module-specific logger


# Background task for data cleanup
async def cleanup_old_data():
    """Background task to clean up old data"""
    try:
        # Clean up old spaced repetition items (older than 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        if db_manager.pool:
            async with db_manager.pool.acquire() as conn:
                await conn.execute(
                    """
                    DELETE FROM spaced_repetition 
                    WHERE next_review < $1
                """,
                    cutoff_date,
                )
        logger.info("Completed data cleanup")
    except Exception as e:
        logger.error(f"Data cleanup failed: {e}")
