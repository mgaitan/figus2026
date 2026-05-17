"""Tests for the FastAPI album MVP."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, func, select

from figus2026.app import create_app
from figus2026.database import build_engine, create_db_and_tables, seed_database
from figus2026.models import Collector, Country, Player
from figus2026.services import get_or_create_collector

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
SEEDED_COUNTRY_COUNT = 3
SEEDED_PLAYERS_PER_COUNTRY = 6
SEEDED_PLAYER_COUNT = 18
STICKERS_PER_PACK = 5


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    with TestClient(create_app(database_url=database_url)) as test_client:
        yield test_client


def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == HTTP_OK
    assert response.json() == {"status": "ok"}


def test_country_list_starts_with_seeded_progress(client: TestClient):
    response = client.get("/api/countries")

    assert response.status_code == HTTP_OK
    countries = response.json()
    assert {country["code"] for country in countries} == {"ARG", "BRA", "FRA"}
    assert all(country["total_stickers"] == SEEDED_PLAYERS_PER_COUNTRY for country in countries)
    assert all(country["owned_stickers"] == 0 for country in countries)


def test_country_sticker_grid_marks_owned_stickers_after_pack(client: TestClient):
    pack_response = client.post("/api/collectors/demo/packs/open")
    assert pack_response.status_code == HTTP_OK

    response = client.get("/api/countries/ARG/stickers")

    assert response.status_code == HTTP_OK
    page = response.json()
    assert page["code"] == "ARG"
    assert len(page["stickers"]) == SEEDED_PLAYERS_PER_COUNTRY
    assert any(sticker["owned"] for sticker in page["stickers"]) or pack_response.json()["stickers"]


def test_missing_country_returns_404(client: TestClient):
    response = client.get("/api/countries/XXX/stickers")

    assert response.status_code == HTTP_NOT_FOUND


def test_collector_can_open_two_daily_packs(client: TestClient):
    first = client.post("/api/collectors/demo/packs/open")
    second = client.post("/api/collectors/demo/packs/open")
    third = client.post("/api/collectors/demo/packs/open")

    assert first.status_code == HTTP_OK
    assert len(first.json()["stickers"]) == STICKERS_PER_PACK
    assert first.json()["remaining_today"] == 1
    assert second.status_code == HTTP_OK
    assert second.json()["remaining_today"] == 0
    assert third.status_code == HTTP_TOO_MANY_REQUESTS
    assert third.json()["detail"]["reason"] == "daily_limit_reached"


def test_seed_database_is_idempotent(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'seed.db'}")
    create_db_and_tables(engine)

    with Session(engine) as session:
        seed_database(session)
        seed_database(session)
        countries = session.exec(select(func.count()).select_from(Country)).one()
        players = session.exec(select(func.count()).select_from(Player)).one()

    engine.dispose()
    assert countries == SEEDED_COUNTRY_COUNT
    assert players == SEEDED_PLAYER_COUNT


def test_get_or_create_collector_creates_new_collectors(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'collector.db'}")
    create_db_and_tables(engine)

    with Session(engine) as session:
        collector = get_or_create_collector(session, "ema-gaitan")
        stored = session.exec(select(Collector).where(Collector.slug == "ema-gaitan")).one()

    engine.dispose()
    assert collector.display_name == "Ema Gaitan"
    assert stored.id == collector.id
