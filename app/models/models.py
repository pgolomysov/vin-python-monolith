from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, JSON, String, INT, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.models import Base


class Request(Base):
    __tablename__ = "requests"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String(17), unique=True)
    email: Mapped[str] = mapped_column(String)
    done: Mapped[bool] = mapped_column(Boolean, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default="CURRENT_TIMESTAMP"
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class Car(Base):
    __tablename__ = "cars"

    vin: Mapped[str] = mapped_column(String(17), primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default="CURRENT_TIMESTAMP"
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class OutboxRelayer(Base):
    __tablename__ = "outbox_relayer"

    id: Mapped[int] = mapped_column(INT, primary_key=True)
    event_type: Mapped[str] = mapped_column(String)
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default="CURRENT_TIMESTAMP"
    )
    consumed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default="CURRENT_TIMESTAMP"
    )