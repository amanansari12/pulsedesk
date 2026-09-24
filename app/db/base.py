"""
SQLAlchemy declarative base for PulseDesk database models.

All database models will inherit from Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class shared by all SQLAlchemy ORM models.

    SQLAlchemy uses Base to keep track of our models
    and their table metadata.
    """

    pass
