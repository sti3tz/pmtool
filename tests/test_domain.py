"""Tests für Domain-Modelle."""

from datetime import date

import pytest

from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.project import Project
from pmtool.domain.task import Task


class TestProject:
    """Tests für das Project-Modell."""

    def test_create_project(self):
        """Projekt mit Pflichtfeldern erstellen."""
        project = Project(name="Test Projekt")
        assert project.name == "Test Projekt"
        assert project.description == ""
        assert project.id is None
        assert project.is_new is True

    def test_create_project_with_all_fields(self):
        """Projekt mit allen Feldern erstellen."""
        project = Project(
            id=1,
            name="Test Projekt",
            description="Beschreibung",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )
        assert project.id == 1
        assert project.name == "Test Projekt"
        assert project.description == "Beschreibung"
        assert project.start_date == date(2024, 1, 1)
        assert project.end_date == date(2024, 12, 31)
        assert project.is_new is False

    def test_empty_name_raises_error(self):
        """Leerer Projektname wirft Fehler."""
        with pytest.raises(ValueError, match="Projektname darf nicht leer sein"):
            Project(name="")

    def test_whitespace_name_raises_error(self):
        """Projektname nur aus Whitespace wirft Fehler."""
        with pytest.raises(ValueError, match="Projektname darf nicht leer sein"):
            Project(name="   ")

    def test_invalid_date_range_raises_error(self):
        """Ungültiger Datumsbereich wirft Fehler."""
        with pytest.raises(ValueError, match="Startdatum muss vor oder gleich Enddatum"):
            Project(
                name="Test",
                start_date=date(2024, 12, 31),
                end_date=date(2024, 1, 1),
            )

    def test_duration_days(self):
        """Berechnung der Projektdauer."""
        project = Project(
            name="Test",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
        )
        assert project.duration_days == 10

    def test_duration_days_without_dates(self):
        """Keine Dauer ohne Datumsangaben."""
        project = Project(name="Test")
        assert project.duration_days is None


class TestTask:
    """Tests für das Task-Modell."""

    def test_create_task(self):
        """Task mit Pflichtfeldern erstellen."""
        task = Task(project_id=1, title="Test Task")
        assert task.title == "Test Task"
        assert task.project_id == 1
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.MEDIUM
        assert task.progress == 0

    def test_empty_title_raises_error(self):
        """Leerer Task-Titel wirft Fehler."""
        with pytest.raises(ValueError, match="Task-Titel darf nicht leer sein"):
            Task(project_id=1, title="")

    def test_invalid_progress_raises_error(self):
        """Ungültiger Fortschritt wirft Fehler."""
        with pytest.raises(ValueError, match="Fortschritt muss zwischen 0 und 100"):
            Task(project_id=1, title="Test", progress=101)

        with pytest.raises(ValueError, match="Fortschritt muss zwischen 0 und 100"):
            Task(project_id=1, title="Test", progress=-1)

    def test_is_completed(self):
        """Prüfung ob Task abgeschlossen ist."""
        task_done = Task(project_id=1, title="Test", status=TaskStatus.DONE)
        task_todo = Task(project_id=1, title="Test", status=TaskStatus.TODO)

        assert task_done.is_completed is True
        assert task_todo.is_completed is False

    def test_is_overdue(self):
        """Prüfung ob Task überfällig ist."""
        from datetime import timedelta

        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        task_overdue = Task(project_id=1, title="Test", end_date=yesterday)
        task_not_overdue = Task(project_id=1, title="Test", end_date=tomorrow)
        task_done = Task(project_id=1, title="Test", end_date=yesterday, status=TaskStatus.DONE)

        assert task_overdue.is_overdue is True
        assert task_not_overdue.is_overdue is False
        assert task_done.is_overdue is False


class TestEnums:
    """Tests für Enumerationen."""

    def test_task_status_display_names(self):
        """Task-Status Anzeigenamen."""
        assert TaskStatus.TODO.display_name == "Offen"
        assert TaskStatus.IN_PROGRESS.display_name == "In Arbeit"
        assert TaskStatus.DONE.display_name == "Erledigt"

    def test_task_priority_display_names(self):
        """Task-Priorität Anzeigenamen."""
        assert TaskPriority.LOW.display_name == "Niedrig"
        assert TaskPriority.MEDIUM.display_name == "Mittel"
        assert TaskPriority.HIGH.display_name == "Hoch"
        assert TaskPriority.CRITICAL.display_name == "Kritisch"

    def test_task_priority_sort_order(self):
        """Task-Priorität Sortierreihenfolge."""
        assert TaskPriority.LOW.sort_order < TaskPriority.MEDIUM.sort_order
        assert TaskPriority.MEDIUM.sort_order < TaskPriority.HIGH.sort_order
        assert TaskPriority.HIGH.sort_order < TaskPriority.CRITICAL.sort_order
