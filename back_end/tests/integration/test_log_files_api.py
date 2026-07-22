def test_upload_requires_authentication(client, storage_dir):
    response = client.post(
        "/log_files/upload",
        files={"file": ("app.log", b"log content", "text/plain")},
    )

    assert response.status_code == 401


def test_upload_rejects_wrong_extension(client, auth_headers, storage_dir):
    response = client.post(
        "/log_files/upload",
        headers=auth_headers,
        files={"file": ("app.txt", b"log content", "text/plain")},
    )

    assert response.status_code == 400
    assert list(storage_dir.iterdir()) == []


def test_upload_rejects_file_over_5mb(client, auth_headers, storage_dir):
    content = b"x" * (5 * 1024 * 1024 + 1)

    response = client.post(
        "/log_files/upload",
        headers=auth_headers,
        files={"file": ("app.log", content, "text/plain")},
    )

    assert response.status_code == 400
    assert list(storage_dir.iterdir()) == []


def test_upload_stores_file_and_returns_metadata(client, auth_headers, storage_dir, existing_user):
    user, _ = existing_user
    content = b"2026-01-01 INFO something happened\n"

    response = client.post(
        "/log_files/upload",
        headers=auth_headers,
        files={"file": ("app.log", content, "text/plain")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["original_filename"] == "app.log"
    assert body["file_size"] == len(content)
    assert body["status"] == "uploaded"
    assert body["user_id"] == str(user.id)

    stored_files = list(storage_dir.iterdir())
    assert len(stored_files) == 1
    assert stored_files[0].read_bytes() == content
