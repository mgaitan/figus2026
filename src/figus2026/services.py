"""Album and pack-opening application services."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import UTC, date, datetime

from sqlmodel import Session, col, func, select

from figus2026.models import (
    Collector,
    Country,
    OwnedSticker,
    PackOpening,
    PackSticker,
    Player,
    Question,
    TriviaAttempt,
)

DAILY_PACK_LIMIT = 2
STICKERS_PER_PACK = 5
TRIVIA_MAX_BONUS = 3  # max extra packs per day from trivia


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
    """Return country progress for a collector, skipping countries with no players."""
    collector = get_or_create_collector(session, collector_slug)
    countries = session.exec(select(Country).order_by(Country.name)).all()
    summaries: list[dict[str, int | str | list[str]]] = []
    for country in countries:
        total = session.exec(select(func.count()).select_from(Player).where(Player.country_id == country.id)).one()
        if total == 0:
            continue
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
                "coach": country.coach or "",
                "federation_name": country.federation_name or "",
                "federation_logo_url": country.federation_logo_url or "",
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
    return {
        "code": country.code,
        "name": country.name,
        "stripe_colors": stripe_colors(country),
        "coach": country.coach,
        "federation_name": country.federation_name,
        "federation_logo_url": country.federation_logo_url,
        "stickers": stickers,
    }


def open_daily_pack(session: Session, collector_slug: str, current_date: date | None = None) -> dict[str, object]:
    """Open one pack if the collector still has a daily allowance.

    Each correct trivia answer grants one extra pack, up to {TRIVIA_MAX_BONUS} per day.
    """
    opened_on = current_date or today()
    collector = get_or_create_collector(session, collector_slug)
    opened_count = session.exec(
        select(func.count())
        .select_from(PackOpening)
        .where(PackOpening.collector_id == collector.id, PackOpening.opened_on == opened_on)
    ).one()

    correct_today = session.exec(
        select(func.count())
        .select_from(TriviaAttempt)
        .where(
            TriviaAttempt.collector_id == collector.id,
            TriviaAttempt.answered_correctly == True,  # noqa: E712
            func.date(TriviaAttempt.attempted_at) == str(opened_on),
        )
    ).one()
    effective_limit = DAILY_PACK_LIMIT + min(correct_today, TRIVIA_MAX_BONUS)

    if opened_count >= effective_limit:
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
        "remaining_today": effective_limit - opened_count - 1,
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


def get_trivia_question(session: Session, collector_slug: str) -> dict[str, object] | None:
    """Return a random question the collector has not yet answered today.

    Options are shuffled so the correct answer position is unpredictable.
    Returns None when all questions have been answered today.
    """
    collector = get_or_create_collector(session, collector_slug)
    answered_today = set(
        session.exec(
            select(TriviaAttempt.question_id).where(
                TriviaAttempt.collector_id == collector.id,
                func.date(TriviaAttempt.attempted_at) == str(today()),
            )
        ).all()
    )
    all_questions = session.exec(select(Question)).all()
    unanswered = [q for q in all_questions if q.id not in answered_today]
    if not unanswered:
        return None

    question = random.choice(unanswered)
    wrong = question.wrong_answers.split("|")
    options = [question.correct_answer, *wrong]
    random.shuffle(options)
    return {
        "id": question.id,
        "text": question.text,
        "options": options,
        "category": question.category,
    }


def submit_trivia_answer(
    session: Session,
    question_id: int,
    answer: str,
    collector_slug: str,
) -> dict[str, object]:
    """Record the collector's answer and award an extra pack slot if correct.

    Returns whether the answer was correct and how many bonus packs remain today.
    """
    question = session.exec(select(Question).where(Question.id == question_id)).one_or_none()
    if question is None:
        return {"error": "question_not_found"}

    collector = get_or_create_collector(session, collector_slug)
    is_correct = answer.strip() == question.correct_answer

    session.add(
        TriviaAttempt(
            collector_id=collector.id or 0,
            question_id=question_id,
            answered_correctly=is_correct,
        )
    )
    session.commit()

    correct_today = session.exec(
        select(func.count())
        .select_from(TriviaAttempt)
        .where(
            TriviaAttempt.collector_id == collector.id,
            TriviaAttempt.answered_correctly == True,  # noqa: E712
            func.date(TriviaAttempt.attempted_at) == str(today()),
        )
    ).one()
    bonus_remaining = max(0, min(correct_today, TRIVIA_MAX_BONUS))

    return {
        "correct": is_correct,
        "correct_answer": question.correct_answer,
        "extra_pack_awarded": is_correct and correct_today <= TRIVIA_MAX_BONUS,
        "bonus_packs_today": bonus_remaining,
    }
