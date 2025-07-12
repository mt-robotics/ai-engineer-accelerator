from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.progress import ProgressData, TaskCompletion, DailyLog
from app.models.database import db_manager
from app.utils.config import get_logger

# Create router
router = APIRouter()
logger = get_logger(__name__)  # Module-specific logger


@router.get("/progress")
async def get_progress(user_id: str = "default_user"):
    """Get user progress data"""
    try:
        progress = await db_manager.load_progress(user_id)
        if not progress:
            # Return default progress for new users
            progress = ProgressData()

        return progress
    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve progress")


@router.post("/progress")
async def save_progress(progress: ProgressData, user_id: str = "default_user"):
    """Save user progress data"""
    try:
        progress.lastUpdated = datetime.now().isoformat()
        success = await db_manager.save_progress(user_id, progress)

        if success:
            return {"success": True, "message": "Progress saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save progress")

    except Exception as e:
        logger.error(f"Error saving progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to save progress")


@router.post("/task/complete")
async def complete_task(completion: TaskCompletion, user_id: str = "default_user"):
    """Mark a task as completed and update progress"""
    try:
        # Load current progress
        progress = await db_manager.load_progress(user_id) or ProgressData()

        # Add task to completed list if not already there
        if completion.taskId not in progress.completedTasks:
            progress.completedTasks.append(completion.taskId)

            # Update XP
            multiplier = (
                1.5
                if completion.category == "capstone"
                else 1.2 if completion.category == "project" else 1.0
            )
            earned_xp = int(completion.points * multiplier)
            progress.totalXP += earned_xp
            progress.dailyXP += earned_xp

            # Update certification progress
            cert_progress_map = {"ai": 5, "production": 3, "project": 2, "capstone": 10}
            cert_increase = cert_progress_map.get(completion.category, 1)
            progress.certificationProgress["Google Cloud AI"] = min(
                100, progress.certificationProgress["Google Cloud AI"] + cert_increase
            )

            # Add to portfolio if applicable
            if completion.category in ["project", "capstone"]:
                portfolio_item = {
                    "id": completion.taskId,
                    "name": f"Task: {completion.taskId}",
                    "completedDate": datetime.now().isoformat(),
                    "type": completion.category,
                    "xp": earned_xp,
                }
                progress.portfolioItems.append(portfolio_item)

            # Save notes if provided
            if completion.notes:
                progress.notes[completion.taskId] = completion.notes

        # Save updated progress
        await db_manager.save_progress(user_id, progress)

        return {
            "success": True,
            "message": "Task completed successfully",
            "xp_earned": (
                earned_xp if completion.taskId not in progress.completedTasks else 0
            ),
            "total_xp": progress.totalXP,
        }

    except Exception as e:
        logger.error(f"Error completing task: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete task")


@router.post("/daily-log")
async def save_daily_log(log: DailyLog, user_id: str = "default_user"):
    """Save daily learning log"""
    try:
        success = await db_manager.save_daily_log(user_id, log)
        if success:
            return {"success": True, "message": "Daily log saved"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save daily log")
    except Exception as e:
        logger.error(f"Error saving daily log: {e}")
        raise HTTPException(status_code=500, detail="Failed to save daily log")
