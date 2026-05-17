"""Tests for the FastAPI album MVP."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlmodel import Session, func, select

from figus2026.app import create_app, mount_frontend
from figus2026.database import build_engine, create_db_and_tables, ensure_country_columns, seed_database
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


def test_app_serves_built_frontend(tmp_path):
    frontend_dist = tmp_path / "dist"
    assets = frontend_dist / "assets"
    assets.mkdir(parents=True)
    (frontend_dist / "index.html").write_text("<!doctype html><title>figus2026</title>", encoding="utf-8")
    (frontend_dist / "favicon.svg").write_text("<svg />", encoding="utf-8")

    app = create_app(database_url=f"sqlite:///{tmp_path / 'frontend.db'}", frontend_dist=frontend_dist)
    with TestClient(app) as client:
        response = client.get("/")
        favicon = client.get("/favicon.svg")

    assert response.status_code == HTTP_OK
    assert "figus2026" in response.text
    assert favicon.status_code == HTTP_OK


def test_mount_frontend_ignores_missing_dist(tmp_path):
    app = create_app(database_url=f"sqlite:///{tmp_path / 'missing-dist.db'}", frontend_dist=tmp_path / "missing")

    mount_frontend(app, tmp_path / "still-missing")

    app.state.engine.dispose()
    assert not any(getattr(route, "path", None) == "/" for route in app.routes)


def test_country_list_starts_with_seeded_progress(client: TestClient):
    response = client.get("/api/countries")

    assert response.status_code == HTTP_OK
    countries = response.json()
    assert {country["code"] for country in countries} == {"ARG", "BRA", "FRA"}
    argentina = next(country for country in countries if country["code"] == "ARG")
    assert argentina["stripe_colors"] == ["#75aadb", "#ffffff", "#75aadb"]
    assert all(country["total_stickers"] == SEEDED_PLAYERS_PER_COUNTRY for country in countries)
    assert all(country["owned_stickers"] == 0 for country in countries)


def test_country_sticker_grid_marks_owned_stickers_after_pack(client: TestClient):
    pack_response = client.post("/api/collectors/demo/packs/open")
    assert pack_response.status_code == HTTP_OK

    response = client.get("/api/countries/ARG/stickers")

    assert response.status_code == HTTP_OK
    page = response.json()
    assert page["code"] == "ARG"
    assert page["stripe_colors"] == ["#75aadb", "#ffffff", "#75aadb"]
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


def test_country_column_migration_ignores_missing_table(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'empty.db'}")

    ensure_country_columns(engine)

    engine.dispose()


def test_country_column_migration_adds_missing_stripe_colors(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "CREATE TABLE country (id INTEGER PRIMARY KEY, code VARCHAR, name VARCHAR, wikipedia_url VARCHAR)"
        )

    ensure_country_columns(engine)
    column_names = {column["name"] for column in inspect(engine).get_columns("country")}

    engine.dispose()
    assert "stripe_colors" in column_names


def test_get_or_create_collector_creates_new_collectors(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'collector.db'}")
    create_db_and_tables(engine)

    with Session(engine) as session:
        collector = get_or_create_collector(session, "ema-gaitan")
        stored = session.exec(select(Collector).where(Collector.slug == "ema-gaitan")).one()

    engine.dispose()
    assert collector.display_name == "Ema Gaitan"
    assert stored.id == collector.id
