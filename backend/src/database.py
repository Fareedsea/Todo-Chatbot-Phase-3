"""
Database engine and session management using SQLModel.

Provides connection pooling for Neon PostgreSQL with serverless-optimized configuration.
All database operations use dependency injection for automatic session lifecycle management.
"""

from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import QueuePool
from typing import Generator
from .config import settings


# Create SQLModel engine with connection pooling
# Configuration optimized for Neon serverless PostgreSQL
# Use psycopg (v3) driver explicitly by replacing postgresql:// with postgresql+psycopg://
database_url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")

engine = create_engine(
    database_url,
    echo=settings.environment == "development",  # Log SQL queries in dev mode
    pool_size=5,  # Maintain 5 persistent connections
    max_overflow=10,  # Allow up to 10 additional connections under load
    pool_pre_ping=True,  # Verify connection before use (handles serverless drops)
    poolclass=QueuePool,  # Standard connection pool
    pool_recycle=3600,  # Recycle connections after 1 hour (prevent stale connections)
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Automatically handles session lifecycle:
    - Creates session at request start
    - Commits on successful completion
    - Rolls back on exception
    - Closes session at request end

    Usage:
        @app.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            tasks = session.exec(select(Task)).all()
            return tasks
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """
    Create all database tables defined by SQLModel models.

    Called on application startup. Safe to run multiple times (idempotent).
    Uses SQLAlchemy's create_all which only creates missing tables.

    Note: All models must be imported before calling this function
    to ensure their metadata is registered with SQLModel.
    """
    # Import all models to register them with SQLModel metadata
    # This ensures create_all knows about all tables
    from .models import User, Task, Conversation, ChatMessage

    SQLModel.metadata.create_all(engine)
