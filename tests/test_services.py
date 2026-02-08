"""Tests für Service-Klassen."""

from datetime import date

import pytest

from pmtool.domain.enums import TaskPriority, TaskStatus


class TestProjectService:
    """Tests für ProjectService."""

    def test_create_project(self, project_service):
        """Projekt erstellen."""
        project = project_service.create_project(
            name="Test Projekt",
            description="Beschreibung",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )

        assert project.id is not None
        assert project.name == "Test Projekt"

    def test_create_project_strips_whitespace(self, project_service):
        """Whitespace wird entfernt."""
        project = project_service.create_project(name="  Test  ")
        assert project.name == "Test"

    def test_get_all_projects(self, project_service):
        """Alle Projekte abrufen."""
        project_service.create_project(name="Projekt 1")
        project_service.create_project(name="Projekt 2")

        projects = project_service.get_all_projects()
        assert len(projects) == 2

    def test_update_project(self, project_service):
        """Projekt aktualisieren."""
        project = project_service.create_project(name="Original")
        updated = project_service.update_project(project.id, name="Aktualisiert")

        assert updated.name == "Aktualisiert"

    def test_update_nonexistent_project(self, project_service):
        """Nicht-existierendes Projekt aktualisieren wirft Fehler."""
        with pytest.raises(ValueError, match="nicht gefunden"):
            project_service.update_project(9999, name="Test")

    def test_delete_project(self, project_service):
        """Projekt löschen."""
        project = project_service.create_project(name="Zum Löschen")

        result = project_service.delete_project(project.id)
        assert result is True

        assert project_service.get_project(project.id) is None

    def test_get_project_stats(self, project_service, task_service):
        """Projekt-Statistiken abrufen."""
        project = project_service.create_project(
            name="Test",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
        )

        task_service.create_task(project.id, title="Task 1", status=TaskStatus.TODO)
        task_service.create_task(project.id, title="Task 2", status=TaskStatus.DONE)

        stats = project_service.get_project_stats(project.id)
        assert stats["task_count"] == 2
        assert stats["task_stats"]["todo"] == 1
        assert stats["task_stats"]["done"] == 1
        assert stats["duration_days"] == 10


class TestTaskService:
    """Tests für TaskService."""

    def test_create_task(self, project_service, task_service):
        """Task erstellen."""
        project = project_service.create_project(name="Test Projekt")

        task = task_service.create_task(
            project_id=project.id,
            title="Test Task",
            owner="Max",
            priority=TaskPriority.HIGH,
        )

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.owner == "Max"
        assert task.priority == TaskPriority.HIGH

    def test_get_tasks_by_project(self, project_service, task_service):
        """Tasks eines Projekts abrufen."""
        project = project_service.create_project(name="Test Projekt")

        task_service.create_task(project.id, title="Task 1")
        task_service.create_task(project.id, title="Task 2")

        tasks = task_service.get_tasks_by_project(project.id)
        assert len(tasks) == 2

    def test_update_task(self, project_service, task_service):
        """Task aktualisieren."""
        project = project_service.create_project(name="Test Projekt")
        task = task_service.create_task(project.id, title="Original")

        updated = task_service.update_task(
            task.id,
            title="Aktualisiert",
            status=TaskStatus.IN_PROGRESS,
            progress=50,
        )

        assert updated.title == "Aktualisiert"
        assert updated.status == TaskStatus.IN_PROGRESS
        assert updated.progress == 50

    def test_update_task_status(self, project_service, task_service):
        """Task-Status aktualisieren."""
        project = project_service.create_project(name="Test Projekt")
        task = task_service.create_task(project.id, title="Test")

        updated = task_service.update_task_status(task.id, TaskStatus.DONE)
        assert updated.status == TaskStatus.DONE
        assert updated.progress == 100  # Automatisch auf 100 gesetzt

    def test_update_task_progress(self, project_service, task_service):
        """Task-Fortschritt aktualisieren."""
        project = project_service.create_project(name="Test Projekt")
        task = task_service.create_task(project.id, title="Test")

        # Fortschritt > 0 setzt Status auf IN_PROGRESS
        updated = task_service.update_task_progress(task.id, 50)
        assert updated.progress == 50
        assert updated.status == TaskStatus.IN_PROGRESS

        # Fortschritt 100 setzt Status auf DONE
        updated = task_service.update_task_progress(task.id, 100)
        assert updated.progress == 100
        assert updated.status == TaskStatus.DONE

    def test_update_task_progress_invalid(self, project_service, task_service):
        """Ungültiger Fortschritt wirft Fehler."""
        project = project_service.create_project(name="Test Projekt")
        task = task_service.create_task(project.id, title="Test")

        with pytest.raises(ValueError, match="zwischen 0 und 100"):
            task_service.update_task_progress(task.id, 150)

    def test_delete_task(self, project_service, task_service):
        """Task löschen."""
        project = project_service.create_project(name="Test Projekt")
        task = task_service.create_task(project.id, title="Zum Löschen")

        result = task_service.delete_task(task.id)
        assert result is True

        assert task_service.get_task(task.id) is None


class TestExportService:
    """Tests für ExportService."""

    def test_export_tasks_to_string(self, project_service, task_service, export_service):
        """Tasks als CSV-String exportieren."""
        project = project_service.create_project(name="Test Projekt")
        task_service.create_task(
            project.id,
            title="Task 1",
            owner="Max",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            progress=50,
        )

        csv_content = export_service.export_tasks_to_string(project.id)

        assert "ID;Titel;Owner" in csv_content
        assert "Task 1" in csv_content
        assert "Max" in csv_content
        assert "In Arbeit" in csv_content
        assert "Hoch" in csv_content
        assert "50" in csv_content

    def test_export_empty_project(self, project_service, export_service):
        """Export eines Projekts ohne Tasks."""
        project = project_service.create_project(name="Leeres Projekt")

        csv_content = export_service.export_tasks_to_string(project.id)

        # Nur Header
        lines = csv_content.strip().split("\n")
        assert len(lines) == 1
        assert "ID;Titel" in lines[0]
