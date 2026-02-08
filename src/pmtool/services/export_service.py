"""Service für Export-Funktionalität."""

from __future__ import annotations

import csv
from pathlib import Path

from pmtool.data.task_repository import TaskRepository
from pmtool.domain.task import Task


class ExportService:
    """Service für Datenexport.

    Implementiert Export-Funktionalitäten für Tasks.

    Attributes:
        task_repo: Repository für Taskzugriffe
    """

    def __init__(self, task_repo: TaskRepository) -> None:
        """Initialisiert den Service mit einem Repository.

        Args:
            task_repo: Repository für Taskzugriffe
        """
        self.task_repo = task_repo

    def export_tasks_to_csv(self, project_id: int, file_path: str | Path) -> int:
        """Exportiert alle Tasks eines Projekts als CSV-Datei.

        Args:
            project_id: ID des Projekts
            file_path: Zielpfad für die CSV-Datei

        Returns:
            Anzahl der exportierten Tasks
        """
        tasks = self.task_repo.get_by_project(project_id)
        file_path = Path(file_path)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)

            # Header
            writer.writerow(
                [
                    "ID",
                    "Titel",
                    "Owner",
                    "Start",
                    "Ende",
                    "Status",
                    "Priorität",
                    "Fortschritt (%)",
                    "Notizen",
                ]
            )

            # Daten
            for task in tasks:
                writer.writerow(self._task_to_row(task))

        return len(tasks)

    def export_tasks_to_string(self, project_id: int) -> str:
        """Exportiert alle Tasks eines Projekts als CSV-String.

        Args:
            project_id: ID des Projekts

        Returns:
            CSV-Daten als String
        """
        tasks = self.task_repo.get_by_project(project_id)
        lines = []

        # Header
        lines.append(
            ";".join(
                [
                    "ID",
                    "Titel",
                    "Owner",
                    "Start",
                    "Ende",
                    "Status",
                    "Priorität",
                    "Fortschritt (%)",
                    "Notizen",
                ]
            )
        )

        # Daten
        for task in tasks:
            row = self._task_to_row(task)
            # Escape Semicolons und Newlines in Notizen
            escaped_row = [str(cell).replace(";", ",").replace("\n", " ") for cell in row]
            lines.append(";".join(escaped_row))

        return "\n".join(lines)

    def _task_to_row(self, task: Task) -> list:
        """Konvertiert einen Task in eine CSV-Zeile.

        Args:
            task: Task-Objekt

        Returns:
            Liste der Feldwerte
        """
        return [
            task.id,
            task.title,
            task.owner,
            task.start_date.isoformat() if task.start_date else "",
            task.end_date.isoformat() if task.end_date else "",
            task.status.display_name,
            task.priority.display_name,
            task.progress,
            task.notes.replace("\n", " "),
        ]
