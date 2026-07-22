import asyncio
import io
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, UploadFile

from app.domains.log_files import repository as log_file_repository
from app.domains.log_files.service import LogFileService
from app.infrastructure.storage.local_storage import LocalStorage


def _upload_file(filename: str, content: bytes) -> UploadFile:
    return UploadFile(io.BytesIO(content), filename=filename)


class TestValidateFileExtension:
    def test_accepts_dot_log_extension(self):
        LogFileService.validate_file_extension(_upload_file("app.log", b"data"))

    def test_accepts_extension_case_insensitively(self):
        LogFileService.validate_file_extension(_upload_file("app.LOG", b"data"))

    def test_rejects_other_extensions(self):
        with pytest.raises(HTTPException) as exc_info:
            LogFileService.validate_file_extension(_upload_file("app.txt", b"data"))

        assert exc_info.value.status_code == 400


class TestValidateFileSize:
    def test_accepts_content_within_the_5mb_limit(self):
        LogFileService.validate_file_size(b"x" * 100)

    def test_rejects_content_over_the_5mb_limit(self):
        content = b"x" * (5 * 1024 * 1024 + 1)

        with pytest.raises(HTTPException) as exc_info:
            LogFileService.validate_file_size(content)

        assert exc_info.value.status_code == 400


class TestUpload:
    def test_rejects_invalid_extension_before_touching_storage_or_repository(self, monkeypatch):
        calls = {"storage": False, "repository": False}

        async def fake_storage_upload(file, content):
            calls["storage"] = True
            return {}

        def fake_create_log_file(**kwargs):
            calls["repository"] = True

        monkeypatch.setattr(LocalStorage, "upload", fake_storage_upload)
        monkeypatch.setattr(log_file_repository, "create_log_file", fake_create_log_file)

        file = _upload_file("app.txt", b"data")
        current_user = SimpleNamespace(id="user-id")

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(LogFileService.upload(file, current_user))

        assert exc_info.value.status_code == 400
        assert calls == {"storage": False, "repository": False}

    def test_rejects_oversized_file_before_calling_storage(self, monkeypatch):
        calls = {"storage": False}

        async def fake_storage_upload(file, content):
            calls["storage"] = True
            return {}

        monkeypatch.setattr(LocalStorage, "upload", fake_storage_upload)

        content = b"x" * (5 * 1024 * 1024 + 1)
        file = _upload_file("app.log", content)
        current_user = SimpleNamespace(id="user-id")

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(LogFileService.upload(file, current_user))

        assert exc_info.value.status_code == 400
        assert calls["storage"] is False

    def test_stores_file_and_persists_metadata_on_success(self, monkeypatch):
        storage_calls = []
        repository_calls = []

        async def fake_storage_upload(file, content):
            storage_calls.append((file.filename, content))
            return {
                "original_filename": file.filename,
                "stored_filename": "generated-uuid.log",
                "file_size": len(content),
            }

        def fake_create_log_file(**kwargs):
            repository_calls.append(kwargs)
            return SimpleNamespace(id="log-file-id", **kwargs)

        monkeypatch.setattr(LocalStorage, "upload", fake_storage_upload)
        monkeypatch.setattr(log_file_repository, "create_log_file", fake_create_log_file)

        content = b"log line 1\nlog line 2\n"
        file = _upload_file("app.log", content)
        current_user = SimpleNamespace(id="user-id-123")

        result = asyncio.run(LogFileService.upload(file, current_user))

        assert storage_calls == [("app.log", content)]
        assert repository_calls == [
            {
                "user_id": "user-id-123",
                "original_filename": "app.log",
                "stored_filename": "generated-uuid.log",
                "file_size": len(content),
            }
        ]
        assert result.stored_filename == "generated-uuid.log"
