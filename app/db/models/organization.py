"""
Organization model for PulseDesk.

This module defines the organizations (tenants) that use the PulseDesk
customer support platform. Each organization has its own identity and
can have multiple users associated with it.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Organization(Base):
    """
    Represents an organization (tenant) in PulseDesk.

    Each organization has a unique identifier, name, and URL-friendly
    slug. Timestamps track when the organization was created and
    last updated.
    """

    # Name of the database table.
    __tablename__ = "organizations"

    # Unique identifier for each organization.
    # UUIDs provide globally unique IDs without relying on sequential integers.
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Display name of the organization.
    # Cannot be NULL, so every organization must have a name.
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # URL-friendly identifier for the organization.
    # Must be unique across all organizations and cannot be NULL.
    # Example: "Acme Technologies" -> "acme-technologies"
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # Timestamp indicating when the organization was created.
    # The database automatically sets the current timestamp on insertion.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Timestamp indicating when the organization was last updated.
    # Initially set by the database on insertion.
    # SQLAlchemy updates it whenever it issues an UPDATE for this record.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
