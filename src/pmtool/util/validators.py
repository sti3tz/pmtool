"""Validierungsfunktionen für Eingabedaten."""

from datetime import date


def validate_required(value: str | None, field_name: str) -> str:
    """Validiert, dass ein Pflichtfeld nicht leer ist.

    Args:
        value: Zu validierender Wert
        field_name: Name des Feldes für Fehlermeldung

    Returns:
        Der getrimmte Wert

    Raises:
        ValueError: Wenn der Wert leer ist
    """
    if value is None or not value.strip():
        raise ValueError(f"{field_name} darf nicht leer sein")
    return value.strip()


def validate_date_range(
    start_date: date | None,
    end_date: date | None,
    allow_none: bool = True,
) -> tuple[date | None, date | None]:
    """Validiert, dass Startdatum vor Enddatum liegt.

    Args:
        start_date: Startdatum
        end_date: Enddatum
        allow_none: Ob None-Werte erlaubt sind

    Returns:
        Tuple mit (start_date, end_date)

    Raises:
        ValueError: Bei ungültigem Datumsbereich
    """
    if not allow_none:
        if start_date is None:
            raise ValueError("Startdatum ist erforderlich")
        if end_date is None:
            raise ValueError("Enddatum ist erforderlich")

    if start_date and end_date and start_date > end_date:
        raise ValueError("Startdatum muss vor oder gleich Enddatum sein")

    return start_date, end_date


def validate_progress(value: int) -> int:
    """Validiert den Fortschrittswert.

    Args:
        value: Fortschritt in Prozent

    Returns:
        Der validierte Wert

    Raises:
        ValueError: Wenn der Wert nicht zwischen 0 und 100 liegt
    """
    if not isinstance(value, int):
        raise ValueError("Fortschritt muss eine Ganzzahl sein")
    if not 0 <= value <= 100:
        raise ValueError("Fortschritt muss zwischen 0 und 100 liegen")
    return value
