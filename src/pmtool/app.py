"""Einstiegspunkt der PMTool-Anwendung."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from pmtool.data.database import Database
from pmtool.data.project_repository import ProjectRepository
from pmtool.data.task_repository import TaskRepository
from pmtool.services.export_service import ExportService
from pmtool.services.project_service import ProjectService
from pmtool.services.task_service import TaskService
from pmtool.ui.main_window import MainWindow


def get_db_path() -> Path:
    """Ermittelt den Pfad zur Datenbankdatei.

    Die Datenbank wird im Benutzer-Datenverzeichnis gespeichert.

    Returns:
        Pfad zur Datenbankdatei
    """
    # Benutzer-Datenverzeichnis ermitteln
    if sys.platform == "darwin":
        base_path = Path.home() / "Library" / "Application Support" / "PMTool"
    elif sys.platform == "win32":
        base_path = Path.home() / "AppData" / "Local" / "PMTool"
    else:
        base_path = Path.home() / ".local" / "share" / "pmtool"

    base_path.mkdir(parents=True, exist_ok=True)
    return base_path / "pmtool.db"


def main() -> int:
    """Hauptfunktion der Anwendung.

    Returns:
        Exit-Code (0 für Erfolg)
    """
    # Qt-Anwendung erstellen
    app = QApplication(sys.argv)
    app.setApplicationName("PMTool")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("PMTool")

    # Datenbank initialisieren
    db_path = get_db_path()
    db = Database(db_path)
    db.connect()

    try:
        # Repositories erstellen
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)

        # Services erstellen
        project_service = ProjectService(project_repo, task_repo)
        task_service = TaskService(task_repo)
        export_service = ExportService(task_repo)

        # Hauptfenster erstellen und anzeigen
        window = MainWindow(project_service, task_service, export_service)
        window.show()

        # Event-Loop starten
        return app.exec()
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
