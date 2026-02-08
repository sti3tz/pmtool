"""Dialog für Projekt-Erstellung und -Bearbeitung."""

from datetime import date

from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pmtool.domain.project import Project


class ProjectDialog(QDialog):
    """Dialog zum Erstellen oder Bearbeiten eines Projekts."""

    def __init__(self, parent: QWidget, project: Project | None = None) -> None:
        """Initialisiert den Dialog.

        Args:
            parent: Eltern-Widget
            project: Bestehendes Projekt für Bearbeitung (None für Neuanlage)
        """
        super().__init__(parent)
        self._project = project
        self._setup_ui()

        if project:
            self._load_project(project)

    def _setup_ui(self) -> None:
        """Richtet die Benutzeroberfläche ein."""
        self.setWindowTitle("Projekt bearbeiten" if self._project else "Neues Projekt")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Formular
        form_layout = QFormLayout()

        # Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Projektname eingeben...")
        form_layout.addRow("Name *:", self.name_edit)

        # Beschreibung
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Optionale Beschreibung...")
        form_layout.addRow("Beschreibung:", self.description_edit)

        # Startdatum
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(date.today())
        self.start_date_edit.setSpecialValueText("Nicht gesetzt")
        self.start_date_edit.setMinimumDate(date(2000, 1, 1))
        form_layout.addRow("Startdatum:", self.start_date_edit)

        # Enddatum
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(date.today())
        self.end_date_edit.setSpecialValueText("Nicht gesetzt")
        self.end_date_edit.setMinimumDate(date(2000, 1, 1))
        form_layout.addRow("Enddatum:", self.end_date_edit)

        layout.addLayout(form_layout)

        # Buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _load_project(self, project: Project) -> None:
        """Lädt die Projekt-Daten in das Formular.

        Args:
            project: Das zu ladende Projekt
        """
        self.name_edit.setText(project.name)
        self.description_edit.setPlainText(project.description)

        if project.start_date:
            self.start_date_edit.setDate(project.start_date)
        if project.end_date:
            self.end_date_edit.setDate(project.end_date)

    def _on_accept(self) -> None:
        """Validiert und akzeptiert den Dialog."""
        name = self.name_edit.text().strip()

        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Projektnamen ein.")
            self.name_edit.setFocus()
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
            Dict mit Projekt-Attributen
        """
        return {
            "name": self.name_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "start_date": self.start_date_edit.date().toPython(),
            "end_date": self.end_date_edit.date().toPython(),
        }
