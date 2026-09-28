"""
Database engine and session management for PulseDesk.

This module is responsible for creating the SQLAlchemy async engine
and providing database sessions to FastAPI endpoints.

It does not contain database models or business logic.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# Create the SQLAlchemy async engine.
#
# The engine manages the connection infrastructure between our
# application and PostgreSQL.
#
# settings.database_url comes from the .env file through our
# Pydantic Settings configuration.
engine = create_async_engine(
    settings.database_url,
    echo=False,
)

# Create a factory for generating AsyncSession objects.
#
# Each database operation/request can obtain its own session from
# this factory. AsyncSession is used because PulseDesk uses
# asynchronous FastAPI endpoints and asyncpg for PostgreSQL.
#
# expire_on_commit=False means SQLAlchemy will not automatically
# expire ORM object attributes after a transaction is committed.
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """
    Provide an asynchronous database session for a FastAPI request.

    A session is created when the dependency is used and is
    automatically closed when the request finishes.

    Yields:
        AsyncSession: The SQLAlchemy async session used to interact
        with the PostgreSQL database.
    """

    async with async_session_factory() as session:
        yield session
