"""Admin panel powered by sqladmin."""

from __future__ import annotations

import os
import secrets
from typing import ClassVar

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.engine import Engine
from starlette.requests import Request

from figus2026.models import Collector, Country, OwnedSticker, Player, Question, TriviaAttempt


def check_admin_credentials(username: str, password: str) -> bool:
    """Validate admin credentials against environment variables."""
    expected_user = os.environ.get("ADMIN_USERNAME", "admin")
    expected_pass = os.environ.get("ADMIN_PASSWORD", "")
    if not expected_pass:
        return False
    return secrets.compare_digest(username, expected_user) and secrets.compare_digest(password, expected_pass)


class _AdminAuth(AuthenticationBackend):
    """Simple username/password authentication for the admin panel."""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        ok = check_admin_credentials(str(form.get("username", "")), str(form.get("password", "")))
        if ok:
            request.session["admin_authenticated"] = "1"
        return ok

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_authenticated") == "1"


class CountryAdmin(ModelView, model=Country):
    column_list: ClassVar = [Country.code, Country.name, Country.coach, Country.federation_name]
    column_searchable_list: ClassVar = [Country.code, Country.name]
    column_sortable_list: ClassVar = [Country.code, Country.name]
    name = "Country"
    name_plural = "Countries"
    icon = "fa-solid fa-flag"


class PlayerAdmin(ModelView, model=Player):
    column_list: ClassVar = [Player.name, Player.country_id, Player.position, Player.scarcity, Player.image_url]
    column_searchable_list: ClassVar = [Player.name]
    column_sortable_list: ClassVar = [Player.name, Player.scarcity, Player.country_id]
    name = "Player"
    name_plural = "Players"
    icon = "fa-solid fa-person-running"


class QuestionAdmin(ModelView, model=Question):
    column_list: ClassVar = [Question.text, Question.correct_answer, Question.category]
    column_searchable_list: ClassVar = [Question.text, Question.category]
    column_sortable_list: ClassVar = [Question.category]
    name = "Question"
    name_plural = "Questions"
    icon = "fa-solid fa-circle-question"


class CollectorAdmin(ModelView, model=Collector):
    column_list: ClassVar = [Collector.slug, Collector.display_name, Collector.created_at]
    column_searchable_list: ClassVar = [Collector.slug, Collector.display_name]
    can_create = False
    can_delete = False
    name = "Collector"
    name_plural = "Collectors"
    icon = "fa-solid fa-users"


class TriviaAttemptAdmin(ModelView, model=TriviaAttempt):
    column_list: ClassVar = [
        TriviaAttempt.collector_id,
        TriviaAttempt.question_id,
        TriviaAttempt.answered_correctly,
        TriviaAttempt.attempted_at,
    ]
    can_create = False
    can_edit = False
    name = "Trivia Attempt"
    name_plural = "Trivia Attempts"
    icon = "fa-solid fa-chart-bar"


class OwnedStickerAdmin(ModelView, model=OwnedSticker):
    column_list: ClassVar = [
        OwnedSticker.collector_id,
        OwnedSticker.player_id,
        OwnedSticker.copies,
        OwnedSticker.acquired_at,
    ]
    can_create = False
    can_edit = False
    name = "Owned Sticker"
    name_plural = "Owned Stickers"
    icon = "fa-solid fa-star"


def create_admin(app: object, engine: Engine) -> Admin:
    """Mount the sqladmin panel at /admin with session-based auth."""
    secret_key = os.environ.get("ADMIN_SECRET_KEY", "change-me-in-production")
    authentication_backend = _AdminAuth(secret_key=secret_key)
    admin = Admin(app, engine, authentication_backend=authentication_backend)  # type: ignore[arg-type]
    admin.add_view(CountryAdmin)
    admin.add_view(PlayerAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(CollectorAdmin)
    admin.add_view(TriviaAttemptAdmin)
    admin.add_view(OwnedStickerAdmin)
    return admin
