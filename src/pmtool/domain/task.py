from __future__ import annotations

"""Task Domain-Modell."""

from dataclasses import dataclass, field
from datetime import date

from pmtool.domain.enums import TaskPriority, TaskStatus


@dataclass
class Task:
    """Repräsentiert einen Task innerhalb eines Projekts.

    Attributes:
        id: Eindeutige Task-ID (None bei neuen Tasks)
        project_id: ID des zugehörigen Projekts
        title: Task-Titel (Pflichtfeld)
        owner: Verantwortliche Person
        start_date: Geplanter Task-Start
        end_date: Geplantes Task-Ende
        status: Aktueller Status (TODO, IN_PROGRESS, DONE)
        priority: Prioritätsstufe
        progress: Fortschritt in Prozent (0-100)
        notes: Zusätzliche Notizen
    """

    project_id: int
    title: str
    owner: str = ""
    start_date: date | None = None
    end_date: date | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    progress: int = 0
    notes: str = ""
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        """Validiert die Task-Attribute nach Initialisierung."""
        if not self.title or not self.title.strip():
            raise ValueError("Task-Titel darf nicht leer sein")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Startdatum muss vor oder gleich Enddatum sein")

        if not 0 <= self.progress <= 100:
            raise ValueError("Fortschritt muss zwischen 0 und 100 liegen")

    @property
    def is_new(self) -> bool:
        """Gibt True zurück, wenn der Task noch nicht persistiert wurde."""
        return self.id is None

    @property
    def duration_days(self) -> int | None:
        """Berechnet die Task-Dauer in Tagen."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None

    @property
    def is_completed(self) -> bool:
        """Gibt True zurück, wenn der Task abgeschlossen ist."""
        return self.status == TaskStatus.DONE

    @property
    def is_overdue(self) -> bool:
        """Gibt True zurück, wenn der Task überfällig ist."""
        if self.end_date and not self.is_completed:
            return date.today() > self.end_date
        return False
