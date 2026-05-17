"""Database models for the collector album."""

from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return a timezone-aware timestamp for persisted events."""
    return datetime.now(UTC)


class Country(SQLModel, table=True):
    """A national team section in the album."""

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True, min_length=2, max_length=3)
    name: str
    wikipedia_url: str
    stripe_colors: str = Field(default="#75aadb|#ffffff|#75aadb")


class Player(SQLModel, table=True):
    """A footballer represented by one collectible sticker."""

    id: int | None = Field(default=None, primary_key=True)
    country_id: int = Field(foreign_key="country.id", index=True)
    name: str = Field(index=True)
    position: str | None = None
    image_url: str | None = None
    source_url: str
    scarcity: int = Field(default=100, ge=1)


class Collector(SQLModel, table=True):
    """A person collecting stickers."""

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    display_name: str
    created_at: datetime = Field(default_factory=utc_now)


class OwnedSticker(SQLModel, table=True):
    """A sticker owned by a collector."""

    __table_args__ = (UniqueConstraint("collector_id", "player_id"),)

    id: int | None = Field(default=None, primary_key=True)
    collector_id: int = Field(foreign_key="collector.id", index=True)
    player_id: int = Field(foreign_key="player.id", index=True)
    acquired_at: datetime = Field(default_factory=utc_now)
    copies: int = Field(default=1, ge=1)


class PackOpening(SQLModel, table=True):
    """A daily pack opening event."""

    id: int | None = Field(default=None, primary_key=True)
    collector_id: int = Field(foreign_key="collector.id", index=True)
    opened_on: date = Field(index=True)
    created_at: datetime = Field(default_factory=utc_now)


class PackSticker(SQLModel, table=True):
    """One sticker pulled from a pack."""

    id: int | None = Field(default=None, primary_key=True)
    pack_opening_id: int = Field(foreign_key="packopening.id", index=True)
    player_id: int = Field(foreign_key="player.id", index=True)
    is_new: bool
