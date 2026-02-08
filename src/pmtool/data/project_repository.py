"""Repository für Projekt-Persistenz."""

from datetime import date

from pmtool.data.database import Database
from pmtool.domain.project import Project


class ProjectRepository:
    """Repository für CRUD-Operationen auf Projekten.

    Kapselt alle Datenbankzugriffe für die Projekt-Entität.

    Attributes:
        db: Datenbankverbindung
    """

    def __init__(self, db: Database) -> None:
        """Initialisiert das Repository mit einer Datenbankverbindung.

        Args:
            db: Aktive Datenbankverbindung
        """
        self.db = db

    def get_all(self) -> list[Project]:
        """Gibt alle Projekte zurück, sortiert nach Name.

        Returns:
            Liste aller Projekte
        """
        cursor = self.db.execute(
            "SELECT id, name, description, start_date, end_date FROM projects ORDER BY name"
        )
        return [self._row_to_project(row) for row in cursor.fetchall()]

    def get_by_id(self, project_id: int) -> Project | None:
        """Gibt ein Projekt anhand seiner ID zurück.

        Args:
            project_id: ID des gesuchten Projekts

        Returns:
            Das gefundene Projekt oder None
        """
        cursor = self.db.execute(
            "SELECT id, name, description, start_date, end_date FROM projects WHERE id = ?",
            (project_id,),
        )
        row = cursor.fetchone()
        return self._row_to_project(row) if row else None

    def create(self, project: Project) -> Project:
        """Erstellt ein neues Projekt in der Datenbank.

        Args:
            project: Zu erstellendes Projekt (ohne ID)

        Returns:
            Das erstellte Projekt mit generierter ID
        """
        cursor = self.db.execute(
            """INSERT INTO projects (name, description, start_date, end_date)
               VALUES (?, ?, ?, ?)""",
            (
                project.name,
                project.description,
                self._date_to_str(project.start_date),
                self._date_to_str(project.end_date),
            ),
        )
        self.db.commit()

        return Project(
            id=cursor.lastrowid,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
        )

    def update(self, project: Project) -> Project:
        """Aktualisiert ein bestehendes Projekt.

        Args:
            project: Zu aktualisierendes Projekt (mit ID)

        Returns:
            Das aktualisierte Projekt

        Raises:
            ValueError: Wenn das Projekt keine ID hat
        """
        if project.id is None:
            raise ValueError("Projekt muss eine ID haben für Update")

        self.db.execute(
            """UPDATE projects
               SET name = ?, description = ?, start_date = ?, end_date = ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (
                project.name,
                project.description,
                self._date_to_str(project.start_date),
                self._date_to_str(project.end_date),
                project.id,
            ),
        )
        self.db.commit()
        return project

    def delete(self, project_id: int) -> bool:
        """Löscht ein Projekt und alle zugehörigen Tasks.

        Args:
            project_id: ID des zu löschenden Projekts

        Returns:
            True wenn gelöscht, False wenn nicht gefunden
        """
        cursor = self.db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.db.commit()
        return cursor.rowcount > 0

    def _row_to_project(self, row) -> Project:
        """Konvertiert eine Datenbankzeile in ein Project-Objekt.

        Args:
            row: sqlite3.Row-Objekt

        Returns:
            Project-Instanz
        """
        return Project(
            id=row["id"],
            name=row["name"],
            description=row["description"] or "",
            start_date=self._str_to_date(row["start_date"]),
            end_date=self._str_to_date(row["end_date"]),
        )

    @staticmethod
    def _date_to_str(d: date | None) -> str | None:
        """Konvertiert ein Date-Objekt in einen ISO-String."""
        return d.isoformat() if d else None

    @staticmethod
    def _str_to_date(s: str | None) -> date | None:
        """Konvertiert einen ISO-String in ein Date-Objekt."""
        return date.fromisoformat(s) if s else None
