"""Enumerationen für Task-Status und -Priorität."""

from enum import StrEnum


class TaskStatus(StrEnum):
    """Status eines Tasks im Lebenszyklus."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    def __str__(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        """Benutzerfreundlicher Anzeigename."""
        names = {
            TaskStatus.TODO: "Offen",
            TaskStatus.IN_PROGRESS: "In Arbeit",
            TaskStatus.DONE: "Erledigt",
        }
        return names[self]


class TaskPriority(StrEnum):
    """Prioritätsstufen eines Tasks."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    def __str__(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        """Benutzerfreundlicher Anzeigename."""
        names = {
            TaskPriority.LOW: "Niedrig",
            TaskPriority.MEDIUM: "Mittel",
            TaskPriority.HIGH: "Hoch",
            TaskPriority.CRITICAL: "Kritisch",
        }
        return names[self]

    @property
    def sort_order(self) -> int:
        """Sortierreihenfolge (höhere Zahl = höhere Priorität)."""
        order = {
            TaskPriority.LOW: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.HIGH: 3,
            TaskPriority.CRITICAL: 4,
        }
        return order[self]
