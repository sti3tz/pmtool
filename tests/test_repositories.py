"""Tests für Repository-Klassen."""

from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.project import Project
from pmtool.domain.task import Task


class TestProjectRepository:
    """Tests für ProjectRepository."""

    def test_create_and_get(self, project_repo):
        """Projekt erstellen und abrufen."""
        project = Project(name="Test Projekt", description="Beschreibung")
        created = project_repo.create(project)

        assert created.id is not None
        assert created.name == "Test Projekt"

        fetched = project_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.name == "Test Projekt"
        assert fetched.description == "Beschreibung"

    def test_get_all(self, project_repo):
        """Alle Projekte abrufen."""
        project_repo.create(Project(name="Projekt A"))
        project_repo.create(Project(name="Projekt B"))

        projects = project_repo.get_all()
        assert len(projects) == 2
        # Sortiert nach Name
        assert projects[0].name == "Projekt A"
        assert projects[1].name == "Projekt B"

    def test_update(self, project_repo):
        """Projekt aktualisieren."""
        project = project_repo.create(Project(name="Original"))
        project = Project(
            id=project.id,
            name="Aktualisiert",
            description="Neue Beschreibung",
        )
        updated = project_repo.update(project)

        assert updated.name == "Aktualisiert"

        fetched = project_repo.get_by_id(project.id)
        assert fetched.name == "Aktualisiert"
        assert fetched.description == "Neue Beschreibung"

    def test_delete(self, project_repo):
        """Projekt löschen."""
        project = project_repo.create(Project(name="Zum Löschen"))

        result = project_repo.delete(project.id)
        assert result is True

        fetched = project_repo.get_by_id(project.id)
        assert fetched is None

    def test_delete_nonexistent(self, project_repo):
        """Nicht-existierendes Projekt löschen."""
        result = project_repo.delete(9999)
        assert result is False

    def test_get_nonexistent(self, project_repo):
        """Nicht-existierendes Projekt abrufen."""
        fetched = project_repo.get_by_id(9999)
        assert fetched is None


class TestTaskRepository:
    """Tests für TaskRepository."""

    def test_create_and_get(self, project_repo, task_repo):
        """Task erstellen und abrufen."""
        project = project_repo.create(Project(name="Test Projekt"))
        task = Task(
            project_id=project.id,
            title="Test Task",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
        )
        created = task_repo.create(task)

        assert created.id is not None
        assert created.title == "Test Task"

        fetched = task_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.title == "Test Task"
        assert fetched.status == TaskStatus.TODO
        assert fetched.priority == TaskPriority.HIGH

    def test_get_by_project(self, project_repo, task_repo):
        """Tasks eines Projekts abrufen."""
        project = project_repo.create(Project(name="Test Projekt"))

        task_repo.create(Task(project_id=project.id, title="Task 1", priority=TaskPriority.LOW))
        task_repo.create(Task(project_id=project.id, title="Task 2", priority=TaskPriority.HIGH))

        tasks = task_repo.get_by_project(project.id)
        assert len(tasks) == 2
        # Sortiert nach Priorität (HIGH zuerst)
        assert tasks[0].priority == TaskPriority.HIGH
        assert tasks[1].priority == TaskPriority.LOW

    def test_update(self, project_repo, task_repo):
        """Task aktualisieren."""
        project = project_repo.create(Project(name="Test Projekt"))
        task = task_repo.create(Task(project_id=project.id, title="Original"))

        updated_task = Task(
            id=task.id,
            project_id=project.id,
            title="Aktualisiert",
            status=TaskStatus.IN_PROGRESS,
            progress=50,
        )
        task_repo.update(updated_task)

        fetched = task_repo.get_by_id(task.id)
        assert fetched.title == "Aktualisiert"
        assert fetched.status == TaskStatus.IN_PROGRESS
        assert fetched.progress == 50

    def test_delete(self, project_repo, task_repo):
        """Task löschen."""
        project = project_repo.create(Project(name="Test Projekt"))
        task = task_repo.create(Task(project_id=project.id, title="Zum Löschen"))

        result = task_repo.delete(task.id)
        assert result is True

        fetched = task_repo.get_by_id(task.id)
        assert fetched is None

    def test_cascade_delete(self, project_repo, task_repo):
        """Tasks werden beim Löschen des Projekts mitgelöscht."""
        project = project_repo.create(Project(name="Test Projekt"))
        task = task_repo.create(Task(project_id=project.id, title="Test Task"))

        project_repo.delete(project.id)

        fetched = task_repo.get_by_id(task.id)
        assert fetched is None

    def test_get_stats_by_project(self, project_repo, task_repo):
        """Statistiken zu Projekt-Tasks."""
        project = project_repo.create(Project(name="Test Projekt"))

        task_repo.create(Task(project_id=project.id, title="Task 1", status=TaskStatus.TODO))
        task_repo.create(Task(project_id=project.id, title="Task 2", status=TaskStatus.IN_PROGRESS))
        task_repo.create(Task(project_id=project.id, title="Task 3", status=TaskStatus.DONE))
        task_repo.create(Task(project_id=project.id, title="Task 4", status=TaskStatus.DONE))

        stats = task_repo.get_stats_by_project(project.id)
        assert stats["total"] == 4
        assert stats["todo"] == 1
        assert stats["in_progress"] == 1
        assert stats["done"] == 2
