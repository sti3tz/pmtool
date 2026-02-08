# PMTool - Lokales Projektmanagement-Tool

Ein einfaches, lokales Projektmanagement-Tool mit GUI zur Verwaltung von Projekten und Tasks.

## Features

- **Projektverwaltung**: Anlegen, Bearbeiten und Löschen von Projekten
- **Task-Management**: Tasks mit Status, Priorität, Owner und Fortschritt
- **Gantt-Ansicht**: Einfache Zeitbalken-Darstellung
- **CSV-Export**: Export der Tasks je Projekt

## Technologie-Stack

- Python ≥ 3.11
- PySide6 (Qt GUI)
- SQLite (lokale Persistenz)
- pytest (Tests)

## Installation

```bash
# Repository klonen
git clone https://github.com/your-org/pmtool.git
cd pmtool

# Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oder: .venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -e ".[dev]"
```

## Verwendung

```bash
# Anwendung starten
pmtool
```

## Entwicklung

```bash
# Linting
ruff check src tests

# Tests ausführen
pytest

# Tests mit Coverage
pytest --cov=pmtool --cov-report=html
```

## Projektstruktur

```
src/pmtool/
├── app.py          # Einstiegspunkt
├── domain/         # Domain-Modelle (dataclasses)
├── data/           # Repository-Layer (SQLite)
├── services/       # Business-Logik / Use-Cases
├── ui/             # PySide6 GUI-Komponenten
└── util/           # Hilfsfunktionen
```

## Dokumentation

Siehe [docs/](docs/) für ausführliche Dokumentation:

- [Requirements](docs/01_requirements.md)
- [Architektur](docs/02_architecture.md)
- [Setup](docs/03_setup_local.md)

## Lizenz

MIT License - siehe [LICENSE](LICENSE)
