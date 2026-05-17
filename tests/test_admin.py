"""Tests for the admin authentication and panel setup."""

from __future__ import annotations

import asyncio

import pytest

from figus2026.admin import _AdminAuth, check_admin_credentials


def test_check_admin_credentials_rejects_empty_password(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    assert check_admin_credentials("admin", "") is False


def test_check_admin_credentials_accepts_correct(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "secret123")

    assert check_admin_credentials("admin", "secret123") is True


def test_check_admin_credentials_rejects_wrong_password(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "secret123")

    assert check_admin_credentials("admin", "wrong") is False


def test_check_admin_credentials_rejects_wrong_username(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "secret123")

    assert check_admin_credentials("hacker", "secret123") is False


def _run(coro):  # type: ignore[no-untyped-def]
    return asyncio.run(coro)


class _MockSession(dict):
    def clear(self) -> None:
        super().clear()


class _MockRequest:
    def __init__(self, form_data: dict[str, str] | None = None, session_data: dict[str, str] | None = None) -> None:
        self._form = form_data or {}
        self.session: dict[str, str] = _MockSession(session_data or {})

    async def form(self) -> dict[str, str]:
        return self._form


@pytest.fixture
def auth() -> _AdminAuth:
    return _AdminAuth(secret_key="test-secret")


def test_admin_auth_login_success(auth: _AdminAuth, monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "pass")
    request = _MockRequest(form_data={"username": "admin", "password": "pass"})

    ok = _run(auth.login(request))

    assert ok is True
    assert request.session["admin_authenticated"] == "1"


def test_admin_auth_login_failure(auth: _AdminAuth, monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "pass")
    request = _MockRequest(form_data={"username": "admin", "password": "bad"})

    ok = _run(auth.login(request))

    assert ok is False
    assert "admin_authenticated" not in request.session


def test_admin_auth_logout_clears_session(auth: _AdminAuth):
    request = _MockRequest(session_data={"admin_authenticated": "1"})

    result = _run(auth.logout(request))

    assert result is True
    assert "admin_authenticated" not in request.session


def test_admin_auth_authenticate_with_valid_session(auth: _AdminAuth):
    request = _MockRequest(session_data={"admin_authenticated": "1"})

    result = _run(auth.authenticate(request))

    assert result is True


def test_admin_auth_authenticate_without_session(auth: _AdminAuth):
    request = _MockRequest()

    result = _run(auth.authenticate(request))

    assert result is False
