"""
Configuration management for AI Progress Tracker
"""

import os
import logging
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv


@dataclass
class EnvironmentConfig:
    """Configuration for environment settings."""

    name: str
    file: str


@dataclass
class APIConfig:
    """Configuration for API settings."""

    host: str
    port: int
    debug: bool
    cors_origins: List[str]


@dataclass
class DatabaseConfig:
    """Configuration for database settings."""

    url: str
    pool_size: int
    max_overflow: int


@dataclass
class ProgressConfig:
    """Configuration for progress tracking features."""

    default_xp_multiplier: float
    spaced_repetition_enabled: bool
    analytics_enabled: bool
    backup_interval_hours: int


class Config:
    """Manage application configuration for AI Progress Tracker."""

    def __init__(self, environment: str = None):
        self._init_environment(environment)
        self._load_env_file()
        self._load_config()
        self._setup_logging()

        self.logger.info("Configuration loaded for environment: %s", self.env.name)

    def _init_environment(self, environment: str = None):
        """Initialize environment configurations"""
        env_name = (
            environment
            or os.getenv("APP_ENV")
            or os.getenv("ENVIRONMENT", "development")
        )

        self.env = EnvironmentConfig(name=env_name, file=f".env.{env_name}")

    def _load_env_file(self):
        """Load environment variables from the appropriate file"""
        if os.path.exists(self.env.file):
            load_dotenv(self.env.file, override=True)
        else:
            load_dotenv(".env")

    def _load_config(self):
        """Load all configuration values from environment variables"""

        # API Configuration
        cors_origins = os.getenv("CORS_ORIGINS", "*")
        self.api = APIConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            debug=os.getenv("API_DEBUG", "false").lower() == "true",
            cors_origins=[origin.strip() for origin in cors_origins.split(",")],
        )

        # Database Configuration
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///progress.db"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
        )

        # Progress Tracking Configuration
        self.progress = ProgressConfig(
            default_xp_multiplier=float(os.getenv("DEFAULT_XP_MULTIPLIER", "1.0")),
            spaced_repetition_enabled=os.getenv(
                "SPACED_REPETITION_ENABLED", "true"
            ).lower()
            == "true",
            analytics_enabled=os.getenv("ANALYTICS_ENABLED", "true").lower() == "true",
            backup_interval_hours=int(os.getenv("BACKUP_INTERVAL_HOURS", "24")),
        )

        # Frontend Configuration (for auto-generation)
        self.frontend = {
            "api_url": os.getenv(
                "FRONTEND_API_URL", f"http://{self.api.host}:{self.api.port}"
            ),
            "debug": self.api.debug,
            "environment": self.env.name,
            "analytics_enabled": self.progress.analytics_enabled,
            "spaced_repetition_enabled": self.progress.spaced_repetition_enabled,
        }

    def _setup_logging(self):
        """Configure logging"""
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format=(
                "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
                if self.env.name == "development"
                else "%(asctime)s - %(levelname)s - %(message)s"
            ),
        )

        self.logger = logging.getLogger("ai_tracker")


# Singleton pattern
class ConfigManager:
    """Singleton configuration manager"""

    def __init__(self):
        self.config = None

    def get_config(self, environment: str = None) -> Config:
        if self.config is None:
            self.config = Config(environment)
        return self.config

    def get_logger(self, name: str = None):
        return logging.getLogger(f"ai_tracker.{name}" if name else "ai_tracker")


config_manager = ConfigManager()


def get_config(environment: str = None) -> Config:
    return config_manager.get_config(environment)


def get_logger(name: str = None):
    """Get a logger instance from anywhere in the app"""
    return config_manager.get_logger(name)
