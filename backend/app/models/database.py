import os
import json
from typing import List, Optional
import asyncpg
from app.utils.config import get_logger
from .progress import ProgressData, DailyLog, SpacedRepetitionItem

logger = get_logger(__name__)  # Module-specific logger


# Database Manager
class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///progress.db")

    async def initialize(self):
        """Initialize database connection pool"""
        try:
            if self.database_url.startswith("postgresql"):
                self.pool = await asyncpg.create_pool(
                    self.database_url, min_size=1, max_size=10, command_timeout=60
                )
                await self.create_tables()
                logger.info("Connected to PostgreSQL database")
            else:
                # Fallback to file-based storage for development
                logger.info("Using file-based storage (development mode)")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Continue with file-based storage as fallback

    async def create_tables(self):
        """Create necessary database tables"""
        if not self.pool:
            return

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_progress (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) DEFAULT 'default_user',
                    data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """
            )

            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_logs (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) DEFAULT 'default_user',
                    date DATE NOT NULL,
                    data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """
            )

            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS spaced_repetition (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) DEFAULT 'default_user',
                    task_id VARCHAR(100) NOT NULL,
                    data JSONB NOT NULL,
                    next_review TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """
            )

            # Create indexes for better performance
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id)
            """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_daily_logs_user_date ON daily_logs(user_id, date)
            """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_spaced_repetition_review ON spaced_repetition(user_id, next_review)
            """
            )

    async def save_progress(self, user_id: str, progress_data: ProgressData) -> bool:
        """Save user progress to database"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO user_progress (user_id, data, updated_at)
                        VALUES ($1, $2, NOW())
                        ON CONFLICT (user_id) DO UPDATE SET
                        data = $2, updated_at = NOW()
                    """,
                        user_id,
                        json.dumps(progress_data.dict()),
                    )
                    return True
            else:
                # File-based fallback
                os.makedirs("data", exist_ok=True)
                with open(f"data/progress_{user_id}.json", "w") as f:
                    json.dump(progress_data.dict(), f, indent=2)
                return True

        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
            return False

    async def load_progress(self, user_id: str) -> Optional[ProgressData]:
        """Load user progress from database"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    row = await conn.fetchrow(
                        """
                        SELECT data FROM user_progress WHERE user_id = $1
                        ORDER BY updated_at DESC LIMIT 1
                    """,
                        user_id,
                    )

                    if row:
                        return ProgressData(**row["data"])
            else:
                # File-based fallback
                file_path = f"data/progress_{user_id}.json"
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        return ProgressData(**data)

        except Exception as e:
            logger.error(f"Failed to load progress: {e}")

        return None

    async def save_daily_log(self, user_id: str, daily_log: DailyLog) -> bool:
        """Save daily log entry"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO daily_logs (user_id, date, data)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (user_id, date) DO UPDATE SET
                        data = $3
                    """,
                        user_id,
                        daily_log.date,
                        json.dumps(daily_log.dict()),
                    )
                    return True
            else:
                # File-based fallback
                os.makedirs("data/logs", exist_ok=True)
                with open(f"data/logs/{user_id}_{daily_log.date}.json", "w") as f:
                    json.dump(daily_log.dict(), f, indent=2)
                return True

        except Exception as e:
            logger.error(f"Failed to save daily log: {e}")
            return False

    async def get_spaced_repetition_items(
        self, user_id: str
    ) -> List[SpacedRepetitionItem]:
        """Get items due for spaced repetition review"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    rows = await conn.fetch(
                        """
                        SELECT task_id, data FROM spaced_repetition 
                        WHERE user_id = $1 AND next_review <= NOW()
                        ORDER BY next_review ASC
                    """,
                        user_id,
                    )

                    return [
                        SpacedRepetitionItem(taskId=row["task_id"], **row["data"])
                        for row in rows
                    ]
            else:
                # File-based fallback - simple implementation
                return []

        except Exception as e:
            logger.error(f"Failed to get spaced repetition items: {e}")
            return []

    async def close(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()


# Initialize database manager
db_manager = DatabaseManager()
