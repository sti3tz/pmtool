from __future__ import annotations

"""Widget für die Projektliste."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pmtool.domain.project import Project
from pmtool.services.project_service import ProjectService
from pmtool.ui.dialogs.project_dialog import ProjectDialog


class ProjectListWidget(QWidget):
    """Widget zur Anzeige und Verwaltung der Projektliste.

    Signals:
        project_selected: Wird ausgelöst, wenn ein Projekt ausgewählt wird
        project_deleted: Wird ausgelöst, wenn ein Projekt gelöscht wird
        export_requested: Wird ausgelöst, wenn ein Export angefordert wird
    """

    project_selected = Signal(Project)
    project_deleted = Signal(int)
    export_requested = Signal(Project)

    def __init__(self, project_service: ProjectService) -> None:
        """Initialisiert das Projektlisten-Widget.

        Args:
            project_service: Service für Projektoperationen
        """
        super().__init__()
        self.project_service = project_service
        self._projects: dict[int, Project] = {}
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Richtet die Benutzeroberfläche ein."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("+ Neu")
        self.add_button.setToolTip("Neues Projekt erstellen")
        self.edit_button = QPushButton("Bearbeiten")
        self.edit_button.setEnabled(False)
        self.delete_button = QPushButton("Löschen")
        self.delete_button.setEnabled(False)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Export-Button
        self.export_button = QPushButton("CSV Export")
        self.export_button.setEnabled(False)
        self.export_button.setToolTip("Tasks als CSV exportieren")
        layout.addWidget(self.export_button)

        # Projektliste
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

    def _connect_signals(self) -> None:
        """Verbindet die Signale."""
        self.add_button.clicked.connect(self._on_add_clicked)
        self.edit_button.clicked.connect(self._on_edit_clicked)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.export_button.clicked.connect(self._on_export_clicked)
        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self._on_edit_clicked)

    def refresh(self) -> None:
        """Lädt die Projektliste neu."""
        current_id = self._get_selected_project_id()
        self.list_widget.clear()
        self._projects.clear()

        projects = self.project_service.get_all_projects()
        for project in projects:
            self._add_project_item(project)

        # Vorherige Auswahl wiederherstellen
        if current_id is not None:
            self._select_project_by_id(current_id)

    def _add_project_item(self, project: Project) -> None:
        """Fügt ein Projekt zur Liste hinzu.

        Args:
            project: Das hinzuzufügende Projekt
        """
        item = QListWidgetItem(project.name)
        item.setData(256, project.id)  # Qt.ItemDataRole.UserRole
        self.list_widget.addItem(item)
        self._projects[project.id] = project

    def _get_selected_project_id(self) -> int | None:
        """Gibt die ID des ausgewählten Projekts zurück."""
        item = self.list_widget.currentItem()
        if item:
            return item.data(256)
        return None

    def _get_selected_project(self) -> Project | None:
        """Gibt das ausgewählte Projekt zurück."""
        project_id = self._get_selected_project_id()
        if project_id is not None:
            return self._projects.get(project_id)
        return None

    def _select_project_by_id(self, project_id: int) -> None:
        """Wählt ein Projekt anhand seiner ID aus."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(256) == project_id:
                self.list_widget.setCurrentItem(item)
                break

    def _on_selection_changed(self, current: QListWidgetItem, _previous) -> None:
        """Wird bei Änderung der Auswahl aufgerufen."""
        has_selection = current is not None
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.export_button.setEnabled(has_selection)

        if current:
            project_id = current.data(256)
            project = self._projects.get(project_id)
            if project:
                self.project_selected.emit(project)

    def _on_add_clicked(self) -> None:
        """Wird beim Klick auf 'Neu' aufgerufen."""
        dialog = ProjectDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                project = self.project_service.create_project(**data)
                self.refresh()
                self._select_project_by_id(project.id)
            except ValueError as e:
                QMessageBox.warning(self, "Fehler", str(e))

    def _on_edit_clicked(self) -> None:
        """Wird beim Klick auf 'Bearbeiten' aufgerufen."""
        project = self._get_selected_project()
        if not project:
            return

        dialog = ProjectDialog(self, project)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.project_service.update_project(project.id, **data)
                self.refresh()
            except ValueError as e:
                QMessageBox.warning(self, "Fehler", str(e))

    def _on_delete_clicked(self) -> None:
        """Wird beim Klick auf 'Löschen' aufgerufen."""
        project = self._get_selected_project()
        if not project:
            return

        reply = QMessageBox.question(
            self,
            "Projekt löschen",
            f"Möchten Sie das Projekt '{project.name}' wirklich löschen?\n"
            "Alle zugehörigen Tasks werden ebenfalls gelöscht.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.project_service.delete_project(project.id)
            self.project_deleted.emit(project.id)
            self.refresh()

    def _on_export_clicked(self) -> None:
        """Wird beim Klick auf 'Export' aufgerufen."""
        project = self._get_selected_project()
        if project:
            self.export_requested.emit(project)
