"""
Organization membership model for PulseDesk.

This module defines the relationship between users and organizations.
It also defines the roles a user can have within an organization.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OrganizationRole(str, enum.Enum):
    """
    Defines the roles available to a user within an organization.

    ADMIN:
        Has administrative privileges within the organization.

    AGENT:
        Handles customer support operations.

    CUSTOMER:
        Can interact with the organization's support system.
    """

    ADMIN = "ADMIN"
    AGENT = "AGENT"
    CUSTOMER = "CUSTOMER"


class OrganizationMember(Base):
    """
    Represents a user's membership in an organization.

    This model connects users and organizations through foreign keys.
    A user can belong to multiple organizations and have a different
    role in each one.
    """

    __tablename__ = "organization_members"

    # Prevents the same user from being added to the same organization
    # more than once. The combination of both columns must be unique.
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_organization_member",
        ),
    )

    # Unique identifier for each membership record.
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # References the organization to which the user belongs.
    # CASCADE automatically removes this membership if the organization
    # is deleted.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    # References the user associated with this membership.
    # CASCADE automatically removes this membership if the user is deleted.
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Defines the user's role within the organization.
    # Defaults to CUSTOMER if no role is explicitly provided.
    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole, name="organization_role"),
        nullable=False,
        default=OrganizationRole.CUSTOMER,
    )

    # Records when the user became a member of the organization.
    # The database automatically supplies the current timestamp.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
