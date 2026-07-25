from datetime import timedelta

from app.core import security


def test_hash_password_produces_a_different_string_than_the_plain_password():
    hashed = security.hash_password("senha12345")

    assert hashed != "senha12345"
    assert security.verify_password("senha12345", hashed)


def test_verify_password_rejects_wrong_password():
    hashed = security.hash_password("senha12345")

    assert security.verify_password("outrasenha", hashed) is False


def test_verify_password_returns_false_for_malformed_hash_instead_of_raising():
    assert security.verify_password("senha12345", "not-a-valid-hash") is False


def test_create_access_token_round_trips_through_verify_access_token():
    token = security.create_access_token(data={"sub": "user-id", "email": "a@b.com"})

    payload = security.verify_access_token(token)

    assert payload["sub"] == "user-id"
    assert payload["email"] == "a@b.com"
    assert "exp" in payload


def test_verify_access_token_rejects_garbage_token():
    assert security.verify_access_token("not.a.jwt") is None


def test_verify_access_token_rejects_expired_token():
    token = security.create_access_token(
        data={"sub": "user-id"},
        expires_delta=timedelta(minutes=-1),
    )

    assert security.verify_access_token(token) is None


def test_create_refresh_token_is_valid_and_longer_lived_than_access_token():
    refresh_token = security.create_refresh_token(data={"sub": "user-id"})

    payload = security.verify_access_token(refresh_token)

    assert payload["sub"] == "user-id"
