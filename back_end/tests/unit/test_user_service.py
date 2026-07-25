from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.security import hash_password
from app.domains.users import repository as user_repository
from app.domains.users import service as user_service


def _fake_user(**overrides):
    defaults = dict(
        id="00000000-0000-0000-0000-000000000001",
        email="user@example.com",
        password_hash=hash_password("senha12345"),
        is_active=True,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestCreateUser:
    def test_delegates_to_repository_and_returns_its_result(self, monkeypatch):
        expected = SimpleNamespace(id="new-user")
        monkeypatch.setattr(user_repository, "create_user", lambda data: expected)

        result = user_service.create_user({"email": "a@b.com"})

        assert result is expected

    def test_raises_409_when_repository_reports_duplicate_email(self, monkeypatch):
        def raise_duplicate(_data):
            raise ValueError("Já existe um usuário com este e-mail.")

        monkeypatch.setattr(user_repository, "create_user", raise_duplicate)

        with pytest.raises(HTTPException) as exc_info:
            user_service.create_user({"email": "a@b.com"})

        assert exc_info.value.status_code == 409

    def test_raises_500_on_unexpected_repository_error(self, monkeypatch):
        def raise_unexpected(_data):
            raise RuntimeError("boom")

        monkeypatch.setattr(user_repository, "create_user", raise_unexpected)

        with pytest.raises(HTTPException) as exc_info:
            user_service.create_user({"email": "a@b.com"})

        assert exc_info.value.status_code == 500


class TestLoginUser:
    def test_raises_400_when_user_is_not_found(self, monkeypatch):
        monkeypatch.setattr(user_repository, "find_by_email", lambda email: None)

        with pytest.raises(HTTPException) as exc_info:
            user_service.login_user("missing@example.com", "senha12345")

        assert exc_info.value.status_code == 400

    def test_raises_400_when_password_is_wrong(self, monkeypatch):
        monkeypatch.setattr(user_repository, "find_by_email", lambda email: _fake_user())

        with pytest.raises(HTTPException) as exc_info:
            user_service.login_user("user@example.com", "senha_errada")

        assert exc_info.value.status_code == 400

    def test_raises_400_when_user_is_inactive(self, monkeypatch):
        monkeypatch.setattr(
            user_repository, "find_by_email", lambda email: _fake_user(is_active=False)
        )

        with pytest.raises(HTTPException) as exc_info:
            user_service.login_user("user@example.com", "senha12345")

        assert exc_info.value.status_code == 400
        assert "inativo" in exc_info.value.detail

    def test_returns_access_and_refresh_tokens_on_success(self, monkeypatch):
        monkeypatch.setattr(user_repository, "find_by_email", lambda email: _fake_user())

        token_response = user_service.login_user("user@example.com", "senha12345")

        assert token_response.token_type == "bearer"
        assert token_response.access_token
        assert token_response.refresh_token


class TestRefreshAccessToken:
    def test_raises_400_for_invalid_refresh_token(self):
        with pytest.raises(HTTPException) as exc_info:
            user_service.refresh_access_token("not-a-valid-token")

        assert exc_info.value.status_code == 400

    def test_raises_400_when_payload_is_missing_required_claims(self, monkeypatch):
        monkeypatch.setattr(
            "app.domains.users.service.verify_access_token", lambda token: {}
        )

        with pytest.raises(HTTPException) as exc_info:
            user_service.refresh_access_token("some-token")

        assert exc_info.value.status_code == 400

    def test_issues_new_access_token_and_keeps_the_same_refresh_token(self):
        from app.core.security import create_refresh_token, verify_access_token

        refresh_token = create_refresh_token(data={"sub": "user-id", "email": "user@example.com"})

        token_response = user_service.refresh_access_token(refresh_token)

        assert token_response.refresh_token == refresh_token
        new_payload = verify_access_token(token_response.access_token)
        assert new_payload["sub"] == "user-id"
        assert new_payload["email"] == "user@example.com"
