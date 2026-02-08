"""Service für Projekt-bezogene Geschäftslogik."""

from datetime import date

from pmtool.data.project_repository import ProjectRepository
from pmtool.data.task_repository import TaskRepository
from pmtool.domain.project import Project


class ProjectService:
    """Service für Projekt-Use-Cases.

    Implementiert die Geschäftslogik für Projektverwaltung
    und koordiniert Zugriffe auf Repositories.

    Attributes:
        project_repo: Repository für Projektzugriffe
        task_repo: Repository für Taskzugriffe
    """

    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
    ) -> None:
        """Initialisiert den Service mit Repositories.

        Args:
            project_repo: Repository für Projektzugriffe
            task_repo: Repository für Taskzugriffe
        """
        self.project_repo = project_repo
        self.task_repo = task_repo

    def get_all_projects(self) -> list[Project]:
        """Gibt alle Projekte zurück.

        Returns:
            Liste aller Projekte, sortiert nach Name
        """
        return self.project_repo.get_all()

    def get_project(self, project_id: int) -> Project | None:
        """Gibt ein Projekt anhand seiner ID zurück.

        Args:
            project_id: ID des gesuchten Projekts

        Returns:
            Das gefundene Projekt oder None
        """
        return self.project_repo.get_by_id(project_id)

    def create_project(
        self,
        name: str,
        description: str = "",
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Project:
        """Erstellt ein neues Projekt.

        Args:
            name: Projektname (Pflichtfeld)
            description: Optionale Beschreibung
            start_date: Optionales Startdatum
            end_date: Optionales Enddatum

        Returns:
            Das erstellte Projekt mit ID

        Raises:
            ValueError: Bei ungültigen Eingaben
        """
        # Validierung erfolgt im Domain-Modell
        project = Project(
            name=name.strip(),
            description=description.strip(),
            start_date=start_date,
            end_date=end_date,
        )
        return self.project_repo.create(project)

    def update_project(
        self,
        project_id: int,
        name: str,
        description: str = "",
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Project:
        """Aktualisiert ein bestehendes Projekt.

        Args:
            project_id: ID des zu aktualisierenden Projekts
            name: Neuer Projektname
            description: Neue Beschreibung
            start_date: Neues Startdatum
            end_date: Neues Enddatum

        Returns:
            Das aktualisierte Projekt

        Raises:
            ValueError: Bei ungültigen Eingaben oder wenn Projekt nicht existiert
        """
        existing = self.project_repo.get_by_id(project_id)
        if existing is None:
            raise ValueError(f"Projekt mit ID {project_id} nicht gefunden")

        # Validierung erfolgt im Domain-Modell
        project = Project(
            id=project_id,
            name=name.strip(),
            description=description.strip(),
            start_date=start_date,
            end_date=end_date,
        )
        return self.project_repo.update(project)

    def delete_project(self, project_id: int) -> bool:
        """Löscht ein Projekt und alle zugehörigen Tasks.

        Args:
            project_id: ID des zu löschenden Projekts

        Returns:
            True wenn gelöscht, False wenn nicht gefunden
        """
        return self.project_repo.delete(project_id)

    def get_project_stats(self, project_id: int) -> dict:
        """Gibt Statistiken zu einem Projekt zurück.

        Args:
            project_id: ID des Projekts

        Returns:
            Dict mit Statistiken (task_count, task_stats, etc.)
        """
        project = self.project_repo.get_by_id(project_id)
        if project is None:
            raise ValueError(f"Projekt mit ID {project_id} nicht gefunden")

        task_stats = self.task_repo.get_stats_by_project(project_id)

        return {
            "project": project,
            "task_count": task_stats["total"],
            "task_stats": task_stats,
            "duration_days": project.duration_days,
        }
