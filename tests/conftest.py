"""Pytest-Konfiguration und Fixtures."""

import pytest

from pmtool.data.database import Database
from pmtool.data.project_repository import ProjectRepository
from pmtool.data.task_repository import TaskRepository
from pmtool.services.export_service import ExportService
from pmtool.services.project_service import ProjectService
from pmtool.services.task_service import TaskService


@pytest.fixture
def db():
    """Erstellt eine In-Memory-Datenbank für Tests."""
    database = Database(":memory:")
    database.connect()
    yield database
    database.close()


@pytest.fixture
def project_repo(db):
    """Erstellt ein ProjectRepository mit Test-Datenbank."""
    return ProjectRepository(db)


@pytest.fixture
def task_repo(db):
    """Erstellt ein TaskRepository mit Test-Datenbank."""
    return TaskRepository(db)


@pytest.fixture
def project_service(project_repo, task_repo):
    """Erstellt einen ProjectService mit Test-Repositories."""
    return ProjectService(project_repo, task_repo)


@pytest.fixture
def task_service(task_repo):
    """Erstellt einen TaskService mit Test-Repository."""
    return TaskService(task_repo)


@pytest.fixture
def export_service(task_repo):
    """Erstellt einen ExportService mit Test-Repository."""
    return ExportService(task_repo)
