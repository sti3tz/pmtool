# Lokale Einrichtung

## Voraussetzungen

- Python >= 3.11
- pip (Python Package Manager)
- Git

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/your-org/pmtool.git
cd pmtool
```

### 2. Virtual Environment erstellen

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
# Produktions-Abhängigkeiten
pip install -e .

# Mit Entwicklungs-Abhängigkeiten
pip install -e ".[dev]"
```

## Anwendung starten

```bash
pmtool
```

Oder direkt:

```bash
python -m pmtool.app
```

## Entwicklungsworkflow

### Linting

```bash
# Code prüfen
ruff check src tests

# Code formatieren
ruff format src tests
```

### Tests

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Report
pytest --cov=pmtool --cov-report=html

# Nur bestimmte Tests
pytest tests/test_domain.py
pytest tests/test_services.py -k "test_create"
```

### GUI-Tests

Für GUI-Tests wird `pytest-qt` verwendet. Unter Linux muss die Umgebungsvariable gesetzt werden:

```bash
export QT_QPA_PLATFORM=offscreen
pytest
```

## Datenbank

Die SQLite-Datenbank wird automatisch beim ersten Start erstellt:

| Betriebssystem | Pfad |
|----------------|------|
| macOS | `~/Library/Application Support/PMTool/pmtool.db` |
| Windows | `%LOCALAPPDATA%/PMTool/pmtool.db` |
| Linux | `~/.local/share/pmtool/pmtool.db` |

### Datenbank zurücksetzen

Löschen Sie einfach die Datenbankdatei, um neu zu starten.

## Troubleshooting

### PySide6 Installation schlägt fehl

```bash
# Ggf. System-Abhängigkeiten installieren (Ubuntu/Debian)
sudo apt-get install libgl1 libegl1 libxkbcommon0

# Oder auf macOS
brew install qt
```

### Tests schlagen unter Linux fehl

```bash
# X11/Wayland-Umgebung emulieren
sudo apt-get install libegl1 libxcb-cursor0
export QT_QPA_PLATFORM=offscreen
```
