"""Dialog für Task-Erstellung und -Bearbeitung."""

from datetime import date

from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pmtool.domain.enums import TaskPriority, TaskStatus
from pmtool.domain.project import Project
from pmtool.domain.task import Task


class TaskDialog(QDialog):
    """Dialog zum Erstellen oder Bearbeiten eines Tasks."""

    def __init__(
        self,
        parent: QWidget,
        project: Project,
        task: Task | None = None,
    ) -> None:
        """Initialisiert den Dialog.

        Args:
            parent: Eltern-Widget
            project: Zugehöriges Projekt
            task: Bestehender Task für Bearbeitung (None für Neuanlage)
        """
        super().__init__(parent)
        self._project = project
        self._task = task
        self._setup_ui()

        if task:
            self._load_task(task)

    def _setup_ui(self) -> None:
        """Richtet die Benutzeroberfläche ein."""
        self.setWindowTitle("Task bearbeiten" if self._task else "Neuer Task")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        # Formular
        form_layout = QFormLayout()

        # Titel
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Task-Titel eingeben...")
        form_layout.addRow("Titel *:", self.title_edit)

        # Owner
        self.owner_edit = QLineEdit()
        self.owner_edit.setPlaceholderText("Verantwortliche Person...")
        form_layout.addRow("Owner:", self.owner_edit)

        # Startdatum
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(date.today())
        self.start_date_edit.setMinimumDate(date(2000, 1, 1))
        form_layout.addRow("Startdatum:", self.start_date_edit)

        # Enddatum
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(date.today())
        self.end_date_edit.setMinimumDate(date(2000, 1, 1))
        form_layout.addRow("Enddatum:", self.end_date_edit)

        # Status
        self.status_combo = QComboBox()
        for status in TaskStatus:
            self.status_combo.addItem(status.display_name, status)
        form_layout.addRow("Status:", self.status_combo)

        # Priorität
        self.priority_combo = QComboBox()
        for priority in TaskPriority:
            self.priority_combo.addItem(priority.display_name, priority)
        self.priority_combo.setCurrentIndex(1)  # MEDIUM als Default
        form_layout.addRow("Priorität:", self.priority_combo)

        # Fortschritt
        self.progress_spin = QSpinBox()
        self.progress_spin.setRange(0, 100)
        self.progress_spin.setSuffix(" %")
        self.progress_spin.setValue(0)
        form_layout.addRow("Fortschritt:", self.progress_spin)

        # Notizen
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Zusätzliche Notizen...")
        form_layout.addRow("Notizen:", self.notes_edit)

        layout.addLayout(form_layout)

        # Buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _load_task(self, task: Task) -> None:
        """Lädt die Task-Daten in das Formular.

        Args:
            task: Der zu ladende Task
        """
        self.title_edit.setText(task.title)
        self.owner_edit.setText(task.owner)

        if task.start_date:
            self.start_date_edit.setDate(task.start_date)
        if task.end_date:
            self.end_date_edit.setDate(task.end_date)

        # Status setzen
        for i in range(self.status_combo.count()):
            if self.status_combo.itemData(i) == task.status:
                self.status_combo.setCurrentIndex(i)
                break

        # Priorität setzen
        for i in range(self.priority_combo.count()):
            if self.priority_combo.itemData(i) == task.priority:
                self.priority_combo.setCurrentIndex(i)
                break

        self.progress_spin.setValue(task.progress)
        self.notes_edit.setPlainText(task.notes)

    def _on_accept(self) -> None:
        """Validiert und akzeptiert den Dialog."""
        title = self.title_edit.text().strip()

        if not title:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Task-Titel ein.")
            self.title_edit.setFocus()
            return

        start_date = self.start_date_edit.date().toPython()
        end_date = self.end_date_edit.date().toPython()

        if start_date > end_date:
            QMessageBox.warning(
                self, "Fehler", "Das Startdatum muss vor oder gleich dem Enddatum sein."
            )
            self.start_date_edit.setFocus()
            return

        self.accept()

    def get_data(self) -> dict:
        """Gibt die eingegebenen Daten zurück.

        Returns:
            Dict mit Task-Attributen
        """
        return {
            "title": self.title_edit.text().strip(),
            "owner": self.owner_edit.text().strip(),
            "start_date": self.start_date_edit.date().toPython(),
            "end_date": self.end_date_edit.date().toPython(),
            "status": self.status_combo.currentData(),
            "priority": self.priority_combo.currentData(),
            "progress": self.progress_spin.value(),
            "notes": self.notes_edit.toPlainText().strip(),
        }
