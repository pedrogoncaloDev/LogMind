class TestCreateUser:
    def test_returns_the_created_user_without_leaking_the_password(self, client):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "password": "senha12345",
        }

        response = client.post("/users", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Ada Lovelace"
        assert body["email"] == "ada@example.com"
        assert body["is_active"] is True
        assert "password" not in body
        assert "password_hash" not in body

    def test_rejects_password_shorter_than_8_characters(self, client):
        payload = {"name": "Ada", "email": "ada@example.com", "password": "1234567"}

        response = client.post("/users", json=payload)

        assert response.status_code == 422

    def test_rejects_invalid_email(self, client):
        payload = {"name": "Ada", "email": "not-an-email", "password": "senha12345"}

        response = client.post("/users", json=payload)

        assert response.status_code == 422

    def test_rejects_duplicate_email(self, client, existing_user):
        user, _ = existing_user
        payload = {"name": "Outro Nome", "email": user.email, "password": "senha12345"}

        response = client.post("/users", json=payload)

        assert response.status_code == 409


class TestLogin:
    def test_returns_access_and_refresh_tokens_for_valid_credentials(self, client, existing_user):
        user, plain_password = existing_user

        response = client.post(
            "/users/login", json={"email": user.email, "password": plain_password}
        )

        assert response.status_code == 200
        body = response.json()
        assert body["token_type"] == "bearer"
        assert body["access_token"]
        assert body["refresh_token"]

    def test_rejects_wrong_password(self, client, existing_user):
        user, _ = existing_user

        response = client.post(
            "/users/login", json={"email": user.email, "password": "senha_errada"}
        )

        assert response.status_code == 400

    def test_rejects_unknown_email(self, client):
        response = client.post(
            "/users/login",
            json={"email": "nobody@example.com", "password": "senha12345"},
        )

        assert response.status_code == 400

    def test_rejects_inactive_user(self, client, inactive_user):
        user, plain_password = inactive_user

        response = client.post(
            "/users/login", json={"email": user.email, "password": plain_password}
        )

        assert response.status_code == 400


class TestRefreshToken:
    def test_issues_a_new_access_token_and_keeps_the_refresh_token(self, client, existing_user):
        user, plain_password = existing_user
        login_response = client.post(
            "/users/login", json={"email": user.email, "password": plain_password}
        )
        refresh_token = login_response.json()["refresh_token"]

        response = client.post("/users/token/refresh", json={"refresh_token": refresh_token})

        assert response.status_code == 200
        body = response.json()
        assert body["refresh_token"] == refresh_token
        assert body["access_token"]

    def test_rejects_invalid_refresh_token(self, client):
        response = client.post("/users/token/refresh", json={"refresh_token": "not-a-token"})

        assert response.status_code == 400
