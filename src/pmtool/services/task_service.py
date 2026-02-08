from __future__ import annotations

"""Service für Task-bezogene Geschäftslogik."""

from datetime import date

from pmtool.data.task_repository import TaskRepository
from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.task import Task


class TaskService:
    """Service für Task-Use-Cases.

    Implementiert die Geschäftslogik für Taskverwaltung.

    Attributes:
        task_repo: Repository für Taskzugriffe
    """

    def __init__(self, task_repo: TaskRepository) -> None:
        """Initialisiert den Service mit einem Repository.

        Args:
            task_repo: Repository für Taskzugriffe
        """
        self.task_repo = task_repo

    def get_tasks_by_project(self, project_id: int) -> list[Task]:
        """Gibt alle Tasks eines Projekts zurück.

        Args:
            project_id: ID des Projekts

        Returns:
            Liste der Tasks, sortiert nach Priorität und Startdatum
        """
        return self.task_repo.get_by_project(project_id)

    def get_task(self, task_id: int) -> Task | None:
        """Gibt einen Task anhand seiner ID zurück.

        Args:
            task_id: ID des gesuchten Tasks

        Returns:
            Der gefundene Task oder None
        """
        return self.task_repo.get_by_id(task_id)

    def create_task(
        self,
        project_id: int,
        title: str,
        owner: str = "",
        start_date: date | None = None,
        end_date: date | None = None,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        progress: int = 0,
        notes: str = "",
    ) -> Task:
        """Erstellt einen neuen Task.

        Args:
            project_id: ID des zugehörigen Projekts
            title: Task-Titel (Pflichtfeld)
            owner: Verantwortliche Person
            start_date: Startdatum
            end_date: Enddatum
            status: Initialer Status
            priority: Prioritätsstufe
            progress: Initialer Fortschritt (0-100)
            notes: Notizen

        Returns:
            Der erstellte Task mit ID

        Raises:
            ValueError: Bei ungültigen Eingaben
        """
        # Validierung erfolgt im Domain-Modell
        task = Task(
            project_id=project_id,
            title=title.strip(),
            owner=owner.strip(),
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            progress=progress,
            notes=notes.strip(),
        )
        return self.task_repo.create(task)

    def update_task(
        self,
        task_id: int,
        title: str,
        owner: str = "",
        start_date: date | None = None,
        end_date: date | None = None,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        progress: int = 0,
        notes: str = "",
    ) -> Task:
        """Aktualisiert einen bestehenden Task.

        Args:
            task_id: ID des zu aktualisierenden Tasks
            title: Neuer Titel
            owner: Neue verantwortliche Person
            start_date: Neues Startdatum
            end_date: Neues Enddatum
            status: Neuer Status
            priority: Neue Priorität
            progress: Neuer Fortschritt (0-100)
            notes: Neue Notizen

        Returns:
            Der aktualisierte Task

        Raises:
            ValueError: Bei ungültigen Eingaben oder wenn Task nicht existiert
        """
        existing = self.task_repo.get_by_id(task_id)
        if existing is None:
            raise ValueError(f"Task mit ID {task_id} nicht gefunden")

        # Validierung erfolgt im Domain-Modell
        task = Task(
            id=task_id,
            project_id=existing.project_id,
            title=title.strip(),
            owner=owner.strip(),
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            progress=progress,
            notes=notes.strip(),
        )
        return self.task_repo.update(task)

    def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        """Aktualisiert nur den Status eines Tasks.

        Args:
            task_id: ID des Tasks
            status: Neuer Status

        Returns:
            Der aktualisierte Task

        Raises:
            ValueError: Wenn Task nicht existiert
        """
        existing = self.task_repo.get_by_id(task_id)
        if existing is None:
            raise ValueError(f"Task mit ID {task_id} nicht gefunden")

        task = Task(
            id=task_id,
            project_id=existing.project_id,
            title=existing.title,
            owner=existing.owner,
            start_date=existing.start_date,
            end_date=existing.end_date,
            status=status,
            priority=existing.priority,
            progress=existing.progress if status != TaskStatus.DONE else 100,
            notes=existing.notes,
        )
        return self.task_repo.update(task)

    def update_task_progress(self, task_id: int, progress: int) -> Task:
        """Aktualisiert nur den Fortschritt eines Tasks.

        Args:
            task_id: ID des Tasks
            progress: Neuer Fortschritt (0-100)

        Returns:
            Der aktualisierte Task

        Raises:
            ValueError: Bei ungültigem Fortschritt oder wenn Task nicht existiert
        """
        if not 0 <= progress <= 100:
            raise ValueError("Fortschritt muss zwischen 0 und 100 liegen")

        existing = self.task_repo.get_by_id(task_id)
        if existing is None:
            raise ValueError(f"Task mit ID {task_id} nicht gefunden")

        # Status automatisch anpassen
        new_status = existing.status
        if progress == 100 and existing.status != TaskStatus.DONE:
            new_status = TaskStatus.DONE
        elif progress > 0 and existing.status == TaskStatus.TODO:
            new_status = TaskStatus.IN_PROGRESS

        task = Task(
            id=task_id,
            project_id=existing.project_id,
            title=existing.title,
            owner=existing.owner,
            start_date=existing.start_date,
            end_date=existing.end_date,
            status=new_status,
            priority=existing.priority,
            progress=progress,
            notes=existing.notes,
        )
        return self.task_repo.update(task)

    def delete_task(self, task_id: int) -> bool:
        """Löscht einen Task.

        Args:
            task_id: ID des zu löschenden Tasks

        Returns:
            True wenn gelöscht, False wenn nicht gefunden
        """
        return self.task_repo.delete(task_id)
