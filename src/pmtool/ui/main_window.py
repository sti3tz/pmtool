"""Hauptfenster der Anwendung."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QWidget,
)

from pmtool.domain.project import Project
from pmtool.services.export_service import ExportService
from pmtool.services.project_service import ProjectService
from pmtool.services.task_service import TaskService
from pmtool.ui.gantt_widget import GanttWidget
from pmtool.ui.project_list import ProjectListWidget
from pmtool.ui.task_table import TaskTableWidget


class MainWindow(QMainWindow):
    """Hauptfenster der PMTool-Anwendung.

    Zeigt eine dreigeteilte Ansicht mit Projektliste, Task-Tabelle und Gantt-Chart.

    Attributes:
        project_service: Service für Projektoperationen
        task_service: Service für Taskoperationen
        export_service: Service für Exportoperationen
    """

    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
        export_service: ExportService,
    ) -> None:
        """Initialisiert das Hauptfenster.

        Args:
            project_service: Service für Projektoperationen
            task_service: Service für Taskoperationen
            export_service: Service für Exportoperationen
        """
        super().__init__()
        self.project_service = project_service
        self.task_service = task_service
        self.export_service = export_service

        self._current_project: Project | None = None
        self._setup_ui()
        self._connect_signals()
        self._load_projects()

    def _setup_ui(self) -> None:
        """Richtet die Benutzeroberfläche ein."""
        self.setWindowTitle("PMTool - Projektmanagement")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 800)

        # Zentrales Widget mit Splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Hauptsplitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        # Projektliste (links)
        self.project_list = ProjectListWidget(self.project_service)
        self.splitter.addWidget(self.project_list)

        # Rechter Bereich mit Task-Tabelle und Gantt
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(right_splitter)

        # Task-Tabelle
        self.task_table = TaskTableWidget(self.task_service)
        right_splitter.addWidget(self.task_table)

        # Gantt-Widget
        self.gantt_widget = GanttWidget()
        right_splitter.addWidget(self.gantt_widget)

        # Splitter-Proportionen
        right_splitter.setSizes([400, 300])
        self.splitter.setSizes([250, 950])

        # Statusbar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Bereit")

    def _connect_signals(self) -> None:
        """Verbindet die Signale der Widgets."""
        # Projekt ausgewählt
        self.project_list.project_selected.connect(self._on_project_selected)
        self.project_list.project_deleted.connect(self._on_project_deleted)
        self.project_list.export_requested.connect(self._on_export_requested)

        # Tasks geändert
        self.task_table.tasks_changed.connect(self._on_tasks_changed)

    def _load_projects(self) -> None:
        """Lädt die Projektliste."""
        self.project_list.refresh()

    def _on_project_selected(self, project: Project) -> None:
        """Wird aufgerufen, wenn ein Projekt ausgewählt wurde.

        Args:
            project: Das ausgewählte Projekt
        """
        self._current_project = project
        self.task_table.load_project(project)
        self._update_gantt()
        self.status_bar.showMessage(f"Projekt: {project.name}")

    def _on_project_deleted(self, project_id: int) -> None:
        """Wird aufgerufen, wenn ein Projekt gelöscht wurde.

        Args:
            project_id: ID des gelöschten Projekts
        """
        if self._current_project and self._current_project.id == project_id:
            self._current_project = None
            self.task_table.clear()
            self.gantt_widget.clear()
        self.status_bar.showMessage("Projekt gelöscht")

    def _on_tasks_changed(self) -> None:
        """Wird aufgerufen, wenn Tasks geändert wurden."""
        self._update_gantt()

    def _update_gantt(self) -> None:
        """Aktualisiert die Gantt-Ansicht."""
        if self._current_project is not None and self._current_project.id is not None:
            tasks = self.task_service.get_tasks_by_project(self._current_project.id)
            self.gantt_widget.set_tasks(tasks, self._current_project)

    def _on_export_requested(self, project: Project) -> None:
        """Wird aufgerufen, wenn ein CSV-Export angefordert wird.

        Args:
            project: Das zu exportierende Projekt
        """
        from PySide6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Tasks exportieren",
            f"{project.name}_tasks.csv",
            "CSV-Dateien (*.csv)",
        )

        if file_path:
            try:
                count = self.export_service.export_tasks_to_csv(project.id, file_path)
                QMessageBox.information(
                    self,
                    "Export erfolgreich",
                    f"{count} Tasks wurden exportiert.",
                )
                self.status_bar.showMessage(f"Export: {count} Tasks nach {file_path}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export fehlgeschlagen",
                    f"Fehler beim Export: {e}",
                )
