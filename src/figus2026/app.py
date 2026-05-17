"""FastAPI application for the figus2026 album."""

from __future__ import annotations

from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from figus2026.database import (
    DEFAULT_DATABASE_URL,
    DEMO_COLLECTOR_SLUG,
    build_engine,
    create_db_and_tables,
    seed_database,
)
from figus2026.services import country_stickers, country_summaries, open_daily_pack


def create_app(database_url: str = DEFAULT_DATABASE_URL, seed: bool = True) -> FastAPI:
    """Create the FastAPI app and initialize the local database."""
    engine = build_engine(database_url)
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
    app.state.engine = engine

    def session_dependency() -> Generator[Session]:
        with Session(engine) as session:
            yield session

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/countries")
    def list_countries(
        collector_slug: str = DEMO_COLLECTOR_SLUG,
        session: Session = Depends(session_dependency),  # noqa: B008
    ) -> list[dict[str, int | str]]:
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

    return app


app = create_app()
