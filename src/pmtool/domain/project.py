"""Project Domain-Modell."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Project:
    """Repräsentiert ein Projekt mit grundlegenden Metadaten.

    Attributes:
        id: Eindeutige Projekt-ID (None bei neuen Projekten)
        name: Projektname (Pflichtfeld)
        description: Optionale Projektbeschreibung
        start_date: Geplanter Projektstart
        end_date: Geplantes Projektende
    """

    name: str
    description: str = ""
    start_date: date | None = None
    end_date: date | None = None
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        """Validiert die Projekt-Attribute nach Initialisierung."""
        if not self.name or not self.name.strip():
            raise ValueError("Projektname darf nicht leer sein")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Startdatum muss vor oder gleich Enddatum sein")

    @property
    def is_new(self) -> bool:
        """Gibt True zurück, wenn das Projekt noch nicht persistiert wurde."""
        return self.id is None

    @property
    def duration_days(self) -> int | None:
        """Berechnet die Projektdauer in Tagen."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None
