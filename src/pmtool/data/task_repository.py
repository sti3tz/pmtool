from __future__ import annotations

"""Repository für Task-Persistenz."""

from datetime import date

from pmtool.data.database import Database
from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.task import Task


class TaskRepository:
    """Repository für CRUD-Operationen auf Tasks.

    Kapselt alle Datenbankzugriffe für die Task-Entität.

    Attributes:
        db: Datenbankverbindung
    """

    def __init__(self, db: Database) -> None:
        """Initialisiert das Repository mit einer Datenbankverbindung.

        Args:
            db: Aktive Datenbankverbindung
        """
        self.db = db

    def get_by_project(self, project_id: int) -> list[Task]:
        """Gibt alle Tasks eines Projekts zurück.

        Args:
            project_id: ID des Projekts

        Returns:
            Liste der Tasks, sortiert nach Priorität (absteigend) und Startdatum
        """
        cursor = self.db.execute(
            """SELECT id, project_id, title, owner, start_date, end_date,
                      status, priority, progress, notes
               FROM tasks
               WHERE project_id = ?
               ORDER BY
                   CASE priority
                       WHEN 'CRITICAL' THEN 1
                       WHEN 'HIGH' THEN 2
                       WHEN 'MEDIUM' THEN 3
                       WHEN 'LOW' THEN 4
                   END,
                   start_date""",
            (project_id,),
        )
        return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_by_id(self, task_id: int) -> Task | None:
        """Gibt einen Task anhand seiner ID zurück.

        Args:
            task_id: ID des gesuchten Tasks

        Returns:
            Der gefundene Task oder None
        """
        cursor = self.db.execute(
            """SELECT id, project_id, title, owner, start_date, end_date,
                      status, priority, progress, notes
               FROM tasks WHERE id = ?""",
            (task_id,),
        )
        row = cursor.fetchone()
        return self._row_to_task(row) if row else None

    def create(self, task: Task) -> Task:
        """Erstellt einen neuen Task in der Datenbank.

        Args:
            task: Zu erstellender Task (ohne ID)

        Returns:
            Der erstellte Task mit generierter ID
        """
        cursor = self.db.execute(
            """INSERT INTO tasks (project_id, title, owner, start_date, end_date,
                                  status, priority, progress, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                task.project_id,
                task.title,
                task.owner,
                self._date_to_str(task.start_date),
                self._date_to_str(task.end_date),
                task.status.value,
                task.priority.value,
                task.progress,
                task.notes,
            ),
        )
        self.db.commit()

        return Task(
            id=cursor.lastrowid,
            project_id=task.project_id,
            title=task.title,
            owner=task.owner,
            start_date=task.start_date,
            end_date=task.end_date,
            status=task.status,
            priority=task.priority,
            progress=task.progress,
            notes=task.notes,
        )

    def update(self, task: Task) -> Task:
        """Aktualisiert einen bestehenden Task.

        Args:
            task: Zu aktualisierender Task (mit ID)

        Returns:
            Der aktualisierte Task

        Raises:
            ValueError: Wenn der Task keine ID hat
        """
        if task.id is None:
            raise ValueError("Task muss eine ID haben für Update")

        self.db.execute(
            """UPDATE tasks
               SET title = ?, owner = ?, start_date = ?, end_date = ?,
                   status = ?, priority = ?, progress = ?, notes = ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (
                task.title,
                task.owner,
                self._date_to_str(task.start_date),
                self._date_to_str(task.end_date),
                task.status.value,
                task.priority.value,
                task.progress,
                task.notes,
                task.id,
            ),
        )
        self.db.commit()
        return task

    def delete(self, task_id: int) -> bool:
        """Löscht einen Task.

        Args:
            task_id: ID des zu löschenden Tasks

        Returns:
            True wenn gelöscht, False wenn nicht gefunden
        """
        cursor = self.db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db.commit()
        return cursor.rowcount > 0

    def get_count_by_project(self, project_id: int) -> int:
        """Gibt die Anzahl der Tasks eines Projekts zurück.

        Args:
            project_id: ID des Projekts

        Returns:
            Anzahl der Tasks
        """
        cursor = self.db.execute(
            "SELECT COUNT(*) as count FROM tasks WHERE project_id = ?",
            (project_id,),
        )
        row = cursor.fetchone()
        return row["count"] if row else 0

    def get_stats_by_project(self, project_id: int) -> dict[str, int]:
        """Gibt Statistiken zu den Tasks eines Projekts zurück.

        Args:
            project_id: ID des Projekts

        Returns:
            Dict mit Statistiken (total, todo, in_progress, done)
        """
        cursor = self.db.execute(
            """SELECT
                   COUNT(*) as total,
                   SUM(CASE WHEN status = 'TODO' THEN 1 ELSE 0 END) as todo,
                   SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) as in_progress,
                   SUM(CASE WHEN status = 'DONE' THEN 1 ELSE 0 END) as done
               FROM tasks WHERE project_id = ?""",
            (project_id,),
        )
        row = cursor.fetchone()
        return {
            "total": row["total"] or 0,
            "todo": row["todo"] or 0,
            "in_progress": row["in_progress"] or 0,
            "done": row["done"] or 0,
        }

    def _row_to_task(self, row) -> Task:
        """Konvertiert eine Datenbankzeile in ein Task-Objekt.

        Args:
            row: sqlite3.Row-Objekt

        Returns:
            Task-Instanz
        """
        return Task(
            id=row["id"],
            project_id=row["project_id"],
            title=row["title"],
            owner=row["owner"] or "",
            start_date=self._str_to_date(row["start_date"]),
            end_date=self._str_to_date(row["end_date"]),
            status=TaskStatus(row["status"]),
            priority=TaskPriority(row["priority"]),
            progress=row["progress"],
            notes=row["notes"] or "",
        )

    @staticmethod
    def _date_to_str(d: date | None) -> str | None:
        """Konvertiert ein Date-Objekt in einen ISO-String."""
        return d.isoformat() if d else None

    @staticmethod
    def _str_to_date(s: str | None) -> date | None:
        """Konvertiert einen ISO-String in ein Date-Objekt."""
        return date.fromisoformat(s) if s else None
