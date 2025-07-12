from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.database import db_manager
from app.models.analytics import analytics
from app.utils.config import get_logger

router = APIRouter()
logger = get_logger(__name__)  # Module-specific logger


@router.get("/analytics")
async def get_analytics(user_id: str = "default_user"):
    """Get advanced progress analytics"""
    try:
        progress = await db_manager.load_progress(user_id)
        if not progress:
            raise HTTPException(status_code=404, detail="No progress data found")

        learning_velocity = analytics.calculate_learning_velocity(progress)
        certification_readiness = analytics.predict_certification_readiness(progress)
        recommendations = analytics.generate_personalized_recommendations(progress)

        return {
            "learning_velocity": learning_velocity,
            "certification_readiness": certification_readiness,
            "recommendations": recommendations,
            "summary": {
                "total_xp": progress.totalXP,
                "completion_rate": len(progress.completedTasks)
                / max(1, progress.currentWeek * 5),
                "struggle_rate": len(progress.struggledTasks)
                / max(1, len(progress.completedTasks)),
                "portfolio_count": len(progress.portfolioItems),
            },
        }

    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")


@router.get("/spaced-repetition")
async def get_spaced_repetition(user_id: str = "default_user"):
    """Get items due for spaced repetition review"""
    try:
        items = await db_manager.get_spaced_repetition_items(user_id)
        return {"items": items, "count": len(items)}
    except Exception as e:
        logger.error(f"Error getting spaced repetition: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve spaced repetition items"
        )


@router.get("/backup")
async def create_backup(user_id: str = "default_user"):
    """Create a backup of user progress data"""
    try:
        progress = await db_manager.load_progress(user_id)
        if not progress:
            raise HTTPException(status_code=404, detail="No progress data found")

        backup_data = {
            "backup_date": datetime.now().isoformat(),
            "user_id": user_id,
            "progress": progress.dict(),
            "version": "1.0.0",
        }

        return backup_data
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        raise HTTPException(status_code=500, detail="Failed to create backup")
