from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# Database Models
class ProgressData(BaseModel):
    currentWeek: int = 1
    currentDay: int = 1
    totalXP: int = 0
    dailyXP: int = 0
    streak: int = 0
    completedTasks: List[str] = []
    struggledTasks: List[str] = []
    notes: Dict[str, str] = {}
    portfolioItems: List[Dict[str, Any]] = []
    certificationProgress: Dict[str, int] = Field(
        default_factory=lambda: {
            "Google Cloud AI": 0,
            "AWS ML Specialty": 0,
            "Azure AI Engineer": 0,
        }
    )
    difficultyLevel: str = "medium"
    lastUpdated: Optional[str] = None


class TaskCompletion(BaseModel):
    taskId: str
    points: int
    time: float
    category: str
    notes: Optional[str] = None
    difficulty: str = "medium"


class DailyLog(BaseModel):
    date: str
    tasksCompleted: List[str]
    hoursSpent: float
    xpEarned: int
    notes: str
    challenges: str
    learnings: str
    mood: str = "neutral"


class SpacedRepetitionItem(BaseModel):
    taskId: str
    lastReviewed: str
    nextReview: str
    difficulty: float = 1.0
    interval: int = 1
