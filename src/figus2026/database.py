"""Database setup and seed helpers."""

from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from figus2026.models import Collector, Country, Player, Question
from figus2026.seed_data import WIKIPEDIA_TEAMS
from figus2026.trivia_data import TRIVIA_QUESTIONS

DEFAULT_DATABASE_URL = "sqlite:///figus2026.db"
DEMO_COLLECTOR_SLUG = "demo"


def build_engine(database_url: str = DEFAULT_DATABASE_URL) -> Engine:
    """Create an engine suitable for the local SQLite MVP."""
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


def create_db_and_tables(engine: Engine) -> None:
    """Create all tables for the album."""
    SQLModel.metadata.create_all(engine)
    ensure_country_columns(engine)


def ensure_country_columns(engine: Engine) -> None:
    """Add lightweight SQLite MVP columns that may be missing locally."""
    if not inspect(engine).has_table("country"):
        return
    column_names = {column["name"] for column in inspect(engine).get_columns("country")}
    new_columns = {
        "stripe_colors": "VARCHAR DEFAULT '#75aadb|#ffffff|#75aadb'",
        "coach": "VARCHAR",
        "federation_name": "VARCHAR",
        "federation_logo_url": "VARCHAR",
    }
    with engine.begin() as connection:
        for col_name, col_def in new_columns.items():
            if col_name not in column_names:
                connection.exec_driver_sql(f"ALTER TABLE country ADD COLUMN {col_name} {col_def}")


def seed_database(session: Session) -> None:
    """Load deterministic prototype data without duplicating rows."""
    for seed_country in WIKIPEDIA_TEAMS:
        country = session.exec(select(Country).where(Country.code == seed_country.code)).one_or_none()
        if country is None:
            country = Country(
                code=seed_country.code,
                name=seed_country.name,
                wikipedia_url=seed_country.wikipedia_url,
                stripe_colors="|".join(seed_country.stripe_colors),
                coach=seed_country.coach,
                federation_name=seed_country.federation_name,
                federation_logo_url=seed_country.federation_logo_url,
            )
            session.add(country)
            session.flush()
        else:
            country.name = seed_country.name
            country.wikipedia_url = seed_country.wikipedia_url
            country.stripe_colors = "|".join(seed_country.stripe_colors)
            country.coach = seed_country.coach
            country.federation_name = seed_country.federation_name
            country.federation_logo_url = seed_country.federation_logo_url
            session.add(country)

        for seed_player in seed_country.players:
            player = session.exec(
                select(Player).where(Player.country_id == country.id, Player.name == seed_player.name)
            ).one_or_none()
            if player is not None:
                player.position = seed_player.position
                player.scarcity = seed_player.scarcity
                player.image_url = seed_player.image_url
                player.source_url = seed_country.wikipedia_url
                session.add(player)
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

    _seed_questions(session)

    session.commit()


def _seed_questions(session: Session) -> None:
    """Load trivia questions without duplicating rows (matched by text)."""
    existing_texts = {q.text for q in session.exec(select(Question)).all()}
    for seed_q in TRIVIA_QUESTIONS:
        if seed_q.text not in existing_texts:
            session.add(
                Question(
                    text=seed_q.text,
                    correct_answer=seed_q.correct_answer,
                    wrong_answers="|".join(seed_q.wrong_answers),
                    category=seed_q.category,
                )
            )
