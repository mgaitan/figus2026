"""Database setup and seed helpers."""

from __future__ import annotations

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from figus2026.models import Collector, Country, Player
from figus2026.seed_data import WIKIPEDIA_TEAMS

DEFAULT_DATABASE_URL = "sqlite:///figus2026.db"
DEMO_COLLECTOR_SLUG = "demo"


def build_engine(database_url: str = DEFAULT_DATABASE_URL) -> Engine:
    """Create an engine suitable for the local SQLite MVP."""
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


def create_db_and_tables(engine: Engine) -> None:
    """Create all tables for the album."""
    SQLModel.metadata.create_all(engine)


def seed_database(session: Session) -> None:
    """Load deterministic prototype data without duplicating rows."""
    for seed_country in WIKIPEDIA_TEAMS:
        country = session.exec(select(Country).where(Country.code == seed_country.code)).one_or_none()
        if country is None:
            country = Country(
                code=seed_country.code,
                name=seed_country.name,
                wikipedia_url=seed_country.wikipedia_url,
            )
            session.add(country)
            session.flush()

        for seed_player in seed_country.players:
            player = session.exec(
                select(Player).where(Player.country_id == country.id, Player.name == seed_player.name)
            ).one_or_none()
            if player is not None:
                continue
            session.add(
                Player(
                    country_id=country.id or 0,
                    name=seed_player.name,
                    position=seed_player.position,
                    scarcity=seed_player.scarcity,
                    image_url=seed_player.image_url,
                    source_url=seed_country.wikipedia_url,
                )
            )

    collector = session.exec(select(Collector).where(Collector.slug == DEMO_COLLECTOR_SLUG)).one_or_none()
    if collector is None:
        session.add(Collector(slug=DEMO_COLLECTOR_SLUG, display_name="Demo collector"))

    session.commit()
