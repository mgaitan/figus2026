"""FastAPI application for the figus2026 album."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import Session

from figus2026.admin import create_admin
from figus2026.database import (
    DEFAULT_DATABASE_URL,
    DEMO_COLLECTOR_SLUG,
    build_engine,
    create_db_and_tables,
    seed_database,
)
from figus2026.services import (
    country_stickers,
    country_summaries,
    get_trivia_question,
    open_daily_pack,
    submit_trivia_answer,
)

load_dotenv()

_DEFAULT_CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


def _cors_origins() -> list[str]:
    """Return allowed CORS origins from env var or local dev defaults."""
    raw = os.environ.get("ALLOWED_ORIGINS", "")
    extra = [o.strip() for o in raw.split(",") if o.strip()]
    return _DEFAULT_CORS_ORIGINS + extra


def mount_frontend(app: FastAPI, frontend_dist: Path | None = None) -> None:
    """Serve the built Vite album when `frontend/dist` is available."""
    dist_path = frontend_dist or Path("frontend/dist")
    if not dist_path.exists():
        return

    app.mount("/assets", StaticFiles(directory=dist_path / "assets"), name="frontend-assets")

    @app.get("/")
    def frontend_index() -> FileResponse:
        return FileResponse(dist_path / "index.html")

    @app.get("/favicon.svg")
    def frontend_favicon() -> FileResponse:
        return FileResponse(dist_path / "favicon.svg")


class TriviaAnswerBody(BaseModel):
    answer: str
    collector_slug: str = DEMO_COLLECTOR_SLUG


def _register_album_routes(app: FastAPI, session_dependency: Generator[Session]) -> None:  # type: ignore[type-arg]
    """Attach album and pack routes."""

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/countries")
    def list_countries(
        collector_slug: str = DEMO_COLLECTOR_SLUG,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> list[dict[str, int | str | list[str]]]:
        return country_summaries(session, collector_slug)

    @app.get("/api/countries/{country_code}/stickers")
    def list_country_stickers(
        country_code: str,
        collector_slug: str = DEMO_COLLECTOR_SLUG,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> dict[str, object]:
        album_page = country_stickers(session, country_code, collector_slug)
        if album_page is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return album_page

    @app.post("/api/collectors/{collector_slug}/packs/open")
    def open_pack(
        collector_slug: str,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> dict[str, object]:
        result = open_daily_pack(session, collector_slug)
        if not result["opened"]:
            raise HTTPException(status_code=429, detail=result)
        return result


def _register_trivia_routes(app: FastAPI, session_dependency: Generator[Session]) -> None:  # type: ignore[type-arg]
    """Attach trivia question routes."""

    @app.get("/api/trivia/question")
    def trivia_question(
        collector_slug: str = DEMO_COLLECTOR_SLUG,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> dict[str, object]:
        question = get_trivia_question(session, collector_slug)
        if question is None:
            raise HTTPException(status_code=404, detail="No questions available today")
        return question

    @app.post("/api/trivia/question/{question_id}/answer")
    def answer_trivia(
        question_id: int,
        body: TriviaAnswerBody,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> dict[str, object]:
        result = submit_trivia_answer(session, question_id, body.answer, body.collector_slug)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result


def _register_routes(app: FastAPI, session_dependency: Generator[Session]) -> None:  # type: ignore[type-arg]
    """Attach all API routes to the app."""
    _register_album_routes(app, session_dependency)
    _register_trivia_routes(app, session_dependency)


def create_app(
    database_url: str | None = None,
    seed: bool = True,
    frontend_dist: Path | None = None,
) -> FastAPI:
    """Create the FastAPI app and initialize the local database."""
    resolved_url = database_url or os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    engine = build_engine(resolved_url)
    create_db_and_tables(engine)
    if seed:
        with Session(engine) as session:
            seed_database(session)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        engine.dispose()

    app = FastAPI(
        title="figus2026",
        summary="Cloud sticker album for the 2026 World Cup",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.engine = engine
    mount_frontend(app, frontend_dist)
    create_admin(app, engine)

    def session_dependency() -> Generator[Session]:
        with Session(engine) as session:
            yield session

    _register_routes(app, session_dependency)
    return app


app = create_app()
