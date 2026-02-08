from __future__ import annotations

"""Widget für die Task-Tabelle."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.project import Project
from pmtool.domain.task import Task
from pmtool.services.task_service import TaskService
from pmtool.ui.dialogs.task_dialog import TaskDialog


class TaskTableWidget(QWidget):
    """Widget zur Anzeige und Verwaltung der Tasks eines Projekts.

    Signals:
        tasks_changed: Wird ausgelöst, wenn Tasks geändert wurden
    """

    tasks_changed = Signal()

    # Spalten-Definitionen
    COLUMNS = ["Titel", "Owner", "Start", "Ende", "Status", "Priorität", "Fortschritt"]

    def __init__(self, task_service: TaskService) -> None:
        """Initialisiert das Task-Tabellen-Widget.

        Args:
            task_service: Service für Taskoperationen
        """
        super().__init__()
        self.task_service = task_service
        self._current_project: Project | None = None
        self._tasks: dict[int, Task] = {}
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Richtet die Benutzeroberfläche ein."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("+ Task")
        self.add_button.setEnabled(False)
        self.edit_button = QPushButton("Bearbeiten")
        self.edit_button.setEnabled(False)
        self.delete_button = QPushButton("Löschen")
        self.delete_button.setEnabled(False)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Tabelle
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # Header-Einstellungen
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Titel
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Owner
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Start
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Ende
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Priorität
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Fortschritt

        layout.addWidget(self.table)

    def _connect_signals(self) -> None:
        """Verbindet die Signale."""
        self.add_button.clicked.connect(self._on_add_clicked)
        self.edit_button.clicked.connect(self._on_edit_clicked)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.cellDoubleClicked.connect(self._on_edit_clicked)

    def load_project(self, project: Project) -> None:
        """Lädt die Tasks eines Projekts.

        Args:
            project: Das Projekt, dessen Tasks geladen werden sollen
        """
        self._current_project = project
        self.add_button.setEnabled(True)
        self._refresh_tasks()

    def clear(self) -> None:
        """Leert die Task-Tabelle."""
        self._current_project = None
        self._tasks.clear()
        self.table.setRowCount(0)
        self.add_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def _refresh_tasks(self) -> None:
        """Aktualisiert die Task-Anzeige."""
        if self._current_project is None or self._current_project.id is None:
            return

        self.table.setRowCount(0)
        self._tasks.clear()

        tasks = self.task_service.get_tasks_by_project(self._current_project.id)
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self._set_task_row(row, task)
            self._tasks[task.id] = task

    def _set_task_row(self, row: int, task: Task) -> None:
        """Setzt die Werte einer Tabellenzeile.

        Args:
            row: Zeilenindex
            task: Task-Daten
        """
        # Titel
        title_item = QTableWidgetItem(task.title)
        title_item.setData(Qt.ItemDataRole.UserRole, task.id)
        if task.is_overdue:
            title_item.setForeground(QColor("#dc3545"))
        self.table.setItem(row, 0, title_item)

        # Owner
        self.table.setItem(row, 1, QTableWidgetItem(task.owner))

        # Start
        start_str = task.start_date.strftime("%d.%m.%Y") if task.start_date else "-"
        self.table.setItem(row, 2, QTableWidgetItem(start_str))

        # Ende
        end_str = task.end_date.strftime("%d.%m.%Y") if task.end_date else "-"
        end_item = QTableWidgetItem(end_str)
        if task.is_overdue:
            end_item.setForeground(QColor("#dc3545"))
        self.table.setItem(row, 3, end_item)

        # Status
        status_item = QTableWidgetItem(task.status.display_name)
        status_colors = {
            TaskStatus.TODO: QColor("#6c757d"),
            TaskStatus.IN_PROGRESS: QColor("#0d6efd"),
            TaskStatus.DONE: QColor("#198754"),
        }
        status_item.setForeground(status_colors.get(task.status, QColor("#000000")))
        self.table.setItem(row, 4, status_item)

        # Priorität
        priority_item = QTableWidgetItem(task.priority.display_name)
        priority_colors = {
            TaskPriority.LOW: QColor("#6c757d"),
            TaskPriority.MEDIUM: QColor("#0d6efd"),
            TaskPriority.HIGH: QColor("#fd7e14"),
            TaskPriority.CRITICAL: QColor("#dc3545"),
        }
        priority_item.setForeground(priority_colors.get(task.priority, QColor("#000000")))
        self.table.setItem(row, 5, priority_item)

        # Fortschritt
        progress_item = QTableWidgetItem(f"{task.progress}%")
        progress_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 6, progress_item)

    def _get_selected_task_id(self) -> int | None:
        """Gibt die ID des ausgewählten Tasks zurück."""
        items = self.table.selectedItems()
        if items:
            return items[0].data(Qt.ItemDataRole.UserRole)
        return None

    def _get_selected_task(self) -> Task | None:
        """Gibt den ausgewählten Task zurück."""
        task_id = self._get_selected_task_id()
        if task_id is not None:
            return self._tasks.get(task_id)
        return None

    def _on_selection_changed(self) -> None:
        """Wird bei Änderung der Auswahl aufgerufen."""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def _on_add_clicked(self) -> None:
        """Wird beim Klick auf 'Task' aufgerufen."""
        if self._current_project is None or self._current_project.id is None:
            QMessageBox.warning(self, "Fehler", "Kein Projekt ausgewählt.")
            return

        dialog = TaskDialog(self, self._current_project)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.task_service.create_task(self._current_project.id, **data)
                self._refresh_tasks()
                self.tasks_changed.emit()
            except Exception as e:
                QMessageBox.warning(self, "Fehler", f"Task konnte nicht erstellt werden: {e}")

    def _on_edit_clicked(self) -> None:
        """Wird beim Klick auf 'Bearbeiten' aufgerufen."""
        task = self._get_selected_task()
        if task is None or self._current_project is None:
            return

        dialog = TaskDialog(self, self._current_project, task)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.task_service.update_task(task.id, **data)
                self._refresh_tasks()
                self.tasks_changed.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Fehler", str(e))

    def _on_delete_clicked(self) -> None:
        """Wird beim Klick auf 'Löschen' aufgerufen."""
        task = self._get_selected_task()
        if not task:
            return

        reply = QMessageBox.question(
            self,
            "Task löschen",
            f"Möchten Sie den Task '{task.title}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.task_service.delete_task(task.id)
            self._refresh_tasks()
            self.tasks_changed.emit()
