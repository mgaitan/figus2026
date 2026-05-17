"""Tests for the FastAPI album MVP."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlmodel import Session, func, select

from figus2026.app import create_app, mount_frontend
from figus2026.database import build_engine, create_db_and_tables, ensure_country_columns, seed_database
from figus2026.models import Collector, Country, OwnedSticker, Player, Question, TriviaAttempt
from figus2026.services import get_or_create_collector, get_trivia_question, open_daily_pack, submit_trivia_answer

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
SEEDED_COUNTRY_COUNT = 12
SEEDED_PLAYERS_PER_COUNTRY = 6
SEEDED_PLAYER_COUNT = 72
SEEDED_QUESTION_COUNT = 50
STICKERS_PER_PACK = 5
TRIVIA_OPTIONS_COUNT = 4


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    with TestClient(create_app(database_url=database_url)) as test_client:
        yield test_client


@pytest.fixture
def engine(tmp_path):
    e = build_engine(f"sqlite:///{tmp_path / 'svc.db'}")
    create_db_and_tables(e)
    with Session(e) as session:
        seed_database(session)
    yield e
    e.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as s:
        yield s


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


def test_country_list_returns_seeded_countries(client: TestClient):
    response = client.get("/api/countries")

    assert response.status_code == HTTP_OK
    countries = response.json()
    codes = {country["code"] for country in countries}
    assert {"ARG", "BRA", "FRA"}.issubset(codes)
    assert len(countries) == SEEDED_COUNTRY_COUNT
    argentina = next(country for country in countries if country["code"] == "ARG")
    assert argentina["stripe_colors"] == ["#75aadb", "#ffffff", "#75aadb"]
    assert argentina["coach"] == "Lionel Scaloni"
    assert argentina["federation_name"] == "Asociación del Fútbol Argentino"
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
    assert page["coach"] == "Lionel Scaloni"
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
        questions = session.exec(select(func.count()).select_from(Question)).one()

    engine.dispose()
    assert countries == SEEDED_COUNTRY_COUNT
    assert players == SEEDED_PLAYER_COUNT
    assert questions == SEEDED_QUESTION_COUNT


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
    assert "coach" in column_names
    assert "federation_name" in column_names
    assert "federation_logo_url" in column_names


def test_get_or_create_collector_creates_new_collectors(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'collector.db'}")
    create_db_and_tables(engine)

    with Session(engine) as session:
        collector = get_or_create_collector(session, "ema-gaitan")
        stored = session.exec(select(Collector).where(Collector.slug == "ema-gaitan")).one()

    engine.dispose()
    assert collector.display_name == "Ema Gaitan"
    assert stored.id == collector.id


def test_trivia_question_returns_shuffled_options(session: Session):
    question = get_trivia_question(session, "demo")

    assert question is not None
    assert "id" in question
    assert "text" in question
    assert len(question["options"]) == TRIVIA_OPTIONS_COUNT


def test_trivia_correct_answer_grants_bonus_pack(session: Session, engine):
    question = get_trivia_question(session, "demo")
    assert question is not None

    q = session.exec(select(Question).where(Question.id == question["id"])).one()
    result = submit_trivia_answer(session, q.id or 0, q.correct_answer, "demo")

    assert result["correct"] is True
    assert result["extra_pack_awarded"] is True
    assert result["bonus_packs_today"] == 1


def test_trivia_wrong_answer_gives_no_bonus(session: Session):
    question = get_trivia_question(session, "demo")
    assert question is not None

    q = session.exec(select(Question).where(Question.id == question["id"])).one()
    result = submit_trivia_answer(session, q.id or 0, "wrong answer xyz", "demo")

    assert result["correct"] is False
    assert result["extra_pack_awarded"] is False
    assert result["bonus_packs_today"] == 0


def test_trivia_api_returns_question(client: TestClient):
    response = client.get("/api/trivia/question")

    assert response.status_code == HTTP_OK
    data = response.json()
    assert "id" in data
    assert "text" in data
    assert len(data["options"]) == TRIVIA_OPTIONS_COUNT


def test_trivia_api_accepts_answer(client: TestClient):
    q_response = client.get("/api/trivia/question")
    assert q_response.status_code == HTTP_OK
    question = q_response.json()

    response = client.post(
        f"/api/trivia/question/{question['id']}/answer",
        json={"answer": "anything", "collector_slug": "demo"},
    )

    assert response.status_code == HTTP_OK
    data = response.json()
    assert "correct" in data
    assert "correct_answer" in data


def test_duplicate_sticker_increments_copies(session: Session, mocker):
    player = session.exec(select(Player)).first()
    mocker.patch("figus2026.services.random.choices", return_value=[player] * STICKERS_PER_PACK)
    open_daily_pack(session, "demo")
    open_daily_pack(session, "demo")

    owned = session.exec(select(OwnedSticker).where(OwnedSticker.player_id == player.id)).one()
    # pack 1: 1 new + 4 duplicates → copies=5; pack 2: 5 more duplicates → copies=10
    assert owned.copies == STICKERS_PER_PACK * 2


def test_country_list_skips_countries_with_no_players(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'skip.db'}")
    create_db_and_tables(engine)
    with Session(engine) as s:
        seed_database(s)
        s.add(Country(code="TST", name="Test Nation", wikipedia_url="http://example.com", stripe_colors=""))
        s.commit()
    app = create_app(database_url=f"sqlite:///{tmp_path / 'skip.db'}", seed=False)
    with TestClient(app) as c:
        response = c.get("/api/countries")
    app.state.engine.dispose()
    codes = {country["code"] for country in response.json()}
    assert "TST" not in codes


def test_trivia_question_returns_404_when_all_answered(session: Session):
    all_questions = session.exec(select(Question)).all()
    for q in all_questions:
        session.add(TriviaAttempt(collector_id=1, question_id=q.id or 0, answered_correctly=True))
    session.commit()

    result = get_trivia_question(session, "demo")

    assert result is None


def test_trivia_api_returns_404_when_all_answered(client: TestClient):
    engine = client.app.state.engine  # type: ignore[attr-defined]
    with Session(engine) as s:
        collector = get_or_create_collector(s, "demo")
        all_qs = s.exec(select(Question)).all()
        for q in all_qs:
            s.add(TriviaAttempt(collector_id=collector.id or 0, question_id=q.id or 0, answered_correctly=False))
        s.commit()

    response = client.get("/api/trivia/question?collector_slug=demo")

    assert response.status_code == HTTP_NOT_FOUND


def test_trivia_api_returns_404_for_invalid_question(client: TestClient):
    response = client.post(
        "/api/trivia/question/99999/answer",
        json={"answer": "anything", "collector_slug": "demo"},
    )

    assert response.status_code == HTTP_NOT_FOUND


def test_trivia_correct_answer_allows_extra_pack(client: TestClient):
    q_response = client.get("/api/trivia/question")
    question = q_response.json()

    engine = client.app.state.engine  # type: ignore[attr-defined]
    with Session(engine) as s:
        db_q = s.exec(select(Question).where(Question.id == question["id"])).one()
        correct = db_q.correct_answer

    client.post(f"/api/trivia/question/{question['id']}/answer", json={"answer": correct, "collector_slug": "demo"})

    # open base 2 packs + 1 trivia bonus = 3 total
    for _ in range(3):
        r = client.post("/api/collectors/demo/packs/open")
        assert r.status_code == HTTP_OK

    fourth = client.post("/api/collectors/demo/packs/open")
    assert fourth.status_code == HTTP_TOO_MANY_REQUESTS
