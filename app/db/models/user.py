"""
User model for PulseDesk.

This module defines the users who can access the PulseDesk platform.
It stores user identity, authentication information, account status,
and timestamps for tracking record creation and updates.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    """
    Represents a user account in PulseDesk.

    Each user has a unique identifier, email address, password hash,
    and full name. The account's active status determines whether the
    user is permitted to access the platform.
    """

    # Name of the database table.
    __tablename__ = "users"

    # Unique identifier for each user.
    # UUIDs provide globally unique IDs without relying on sequential integers.
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # User's email address.
    # Must be unique across the platform and cannot be NULL.
    # The index helps speed up lookups, such as during login.
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # Stores the hashed password, never the plain-text password.
    # Passwords should be hashed using a secure algorithm such as Argon2.
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Full name of the user, used for display and identification.
    # Cannot be NULL.
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Indicates whether the user account is active.
    # Defaults to True when a new user is created.
    # Inactive users can be prevented from accessing the platform.
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Timestamp indicating when the user account was created.
    # The database automatically sets the current timestamp on insertion.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Timestamp indicating when the user account was last updated.
    # Initially set by the database on insertion.
    # SQLAlchemy updates it whenever it issues an UPDATE for this record.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
