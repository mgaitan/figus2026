"""Album and pack-opening application services."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import UTC, date, datetime

from sqlmodel import Session, col, func, select

from figus2026.models import Collector, Country, OwnedSticker, PackOpening, PackSticker, Player

DAILY_PACK_LIMIT = 2
STICKERS_PER_PACK = 5


@dataclass(frozen=True)
class PulledSticker:
    player: Player
    country: Country
    is_new: bool


def stripe_colors(country: Country) -> list[str]:
    """Return editable country stripe colors for the album guard."""
    return [color for color in country.stripe_colors.split("|") if color]


def today() -> date:
    """Return the date used to enforce daily pack limits."""
    return datetime.now(UTC).date()


def get_or_create_collector(session: Session, slug: str) -> Collector:
    """Return a collector, creating demo-style collectors on first use."""
    collector = session.exec(select(Collector).where(Collector.slug == slug)).one_or_none()
    if collector is not None:
        return collector

    collector = Collector(slug=slug, display_name=slug.replace("-", " ").title())
    session.add(collector)
    session.commit()
    session.refresh(collector)
    return collector


def country_summaries(session: Session, collector_slug: str) -> list[dict[str, int | str | list[str]]]:
    """Return country progress for a collector."""
    collector = get_or_create_collector(session, collector_slug)
    countries = session.exec(select(Country).order_by(Country.name)).all()
    summaries: list[dict[str, int | str | list[str]]] = []
    for country in countries:
        total = session.exec(select(func.count()).select_from(Player).where(Player.country_id == country.id)).one()
        owned = session.exec(
            select(func.count())
            .select_from(OwnedSticker)
            .join(Player, col(OwnedSticker.player_id) == col(Player.id))
            .where(OwnedSticker.collector_id == collector.id, Player.country_id == country.id)
        ).one()
        summaries.append(
            {
                "code": country.code,
                "name": country.name,
                "stripe_colors": stripe_colors(country),
                "total_stickers": total,
                "owned_stickers": owned,
                "missing_stickers": total - owned,
            }
        )
    return summaries


def country_stickers(session: Session, country_code: str, collector_slug: str) -> dict[str, object] | None:
    """Return the sticker grid for one country."""
    collector = get_or_create_collector(session, collector_slug)
    country = session.exec(select(Country).where(Country.code == country_code.upper())).one_or_none()
    if country is None:
        return None

    owned_player_ids = set(
        session.exec(select(OwnedSticker.player_id).where(OwnedSticker.collector_id == collector.id)).all()
    )
    players = session.exec(select(Player).where(Player.country_id == country.id).order_by(Player.name)).all()
    stickers = [
        {
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "image_url": player.image_url,
            "scarcity": player.scarcity,
            "owned": player.id in owned_player_ids,
        }
        for player in players
    ]
    return {"code": country.code, "name": country.name, "stripe_colors": stripe_colors(country), "stickers": stickers}


def open_daily_pack(session: Session, collector_slug: str, current_date: date | None = None) -> dict[str, object]:
    """Open one pack if the collector still has a daily allowance."""
    opened_on = current_date or today()
    collector = get_or_create_collector(session, collector_slug)
    opened_count = session.exec(
        select(func.count())
        .select_from(PackOpening)
        .where(PackOpening.collector_id == collector.id, PackOpening.opened_on == opened_on)
    ).one()
    if opened_count >= DAILY_PACK_LIMIT:
        return {
            "opened": False,
            "reason": "daily_limit_reached",
            "remaining_today": 0,
            "stickers": [],
        }

    players = session.exec(select(Player).order_by(col(Player.id))).all()
    countries_by_id = {country.id: country for country in session.exec(select(Country)).all()}
    pulled_players = random.choices(players, weights=[player.scarcity for player in players], k=STICKERS_PER_PACK)

    pack = PackOpening(collector_id=collector.id or 0, opened_on=opened_on)
    session.add(pack)
    session.flush()

    pulled: list[PulledSticker] = []
    for player in pulled_players:
        owned = session.exec(
            select(OwnedSticker).where(OwnedSticker.collector_id == collector.id, OwnedSticker.player_id == player.id)
        ).one_or_none()
        is_new = owned is None
        if owned is None:
            session.add(OwnedSticker(collector_id=collector.id or 0, player_id=player.id or 0))
        else:
            owned.copies += 1
            session.add(owned)
        session.add(PackSticker(pack_opening_id=pack.id or 0, player_id=player.id or 0, is_new=is_new))
        pulled.append(PulledSticker(player=player, country=countries_by_id[player.country_id], is_new=is_new))

    session.commit()
    return {
        "opened": True,
        "remaining_today": DAILY_PACK_LIMIT - opened_count - 1,
        "stickers": [
            {
                "id": sticker.player.id,
                "name": sticker.player.name,
                "country_code": sticker.country.code,
                "country_name": sticker.country.name,
                "position": sticker.player.position,
                "image_url": sticker.player.image_url,
                "is_new": sticker.is_new,
            }
            for sticker in pulled
        ],
    }
