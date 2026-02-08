# Testing & Qualitätssicherung

## Test-Framework

PMTool verwendet pytest mit folgenden Erweiterungen:

- **pytest**: Test-Framework
- **pytest-cov**: Coverage-Reporting
- **pytest-qt**: GUI-Testing mit Qt

## Test-Struktur

```
tests/
├── __init__.py
├── conftest.py         # Pytest-Fixtures
├── test_domain.py      # Domain-Modell-Tests
├── test_repositories.py # Repository-Tests
├── test_services.py    # Service-Tests
└── test_ui.py          # GUI-Tests (optional)
```

## Fixtures

In `conftest.py` definierte Fixtures:

```python
@pytest.fixture
def db():
    """In-Memory-Datenbank für Tests."""

@pytest.fixture
def project_repo(db):
    """ProjectRepository mit Test-DB."""

@pytest.fixture
def task_repo(db):
    """TaskRepository mit Test-DB."""

@pytest.fixture
def project_service(project_repo, task_repo):
    """ProjectService mit Test-Repositories."""

@pytest.fixture
def task_service(task_repo):
    """TaskService mit Test-Repository."""
```

## Test-Kategorien

### Unit-Tests

Testen isolierte Komponenten:

- **Domain-Tests**: Validierung, Properties
- **Repository-Tests**: CRUD-Operationen
- **Service-Tests**: Geschäftslogik

### Integrations-Tests

Testen das Zusammenspiel:

- Service + Repository
- Cascade-Deletes
- Transaktionen

## Tests ausführen

```bash
# Alle Tests
pytest

# Mit Verbose-Output
pytest -v

# Bestimmte Datei
pytest tests/test_domain.py

# Bestimmter Test
pytest tests/test_services.py::TestTaskService::test_create_task

# Mit Pattern-Matching
pytest -k "create"

# Mit Coverage
pytest --cov=pmtool --cov-report=html
```

## Coverage

Ziel: >= 80% Coverage

Coverage-Report generieren:

```bash
pytest --cov=pmtool --cov-report=html
open htmlcov/index.html
```

## Linting

PMTool verwendet ruff für Linting und Formatierung.

### Prüfen

```bash
ruff check src tests
```

### Automatische Fixes

```bash
ruff check --fix src tests
```

### Formatierung

```bash
ruff format src tests
```

### Konfiguration

In `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
```

## CI/CD

GitHub Actions führt bei jedem Push/PR aus:

1. **Lint-Job**: `ruff check` und `ruff format --check`
2. **Test-Job**: `pytest` auf Python 3.11 und 3.12

Konfiguration: `.github/workflows/ci.yml`

## Qualitäts-Checkliste

Vor jedem Commit:

- [ ] Tests bestehen (`pytest`)
- [ ] Linting fehlerfrei (`ruff check`)
- [ ] Formatierung korrekt (`ruff format --check`)
- [ ] Coverage nicht gesunken
- [ ] Keine neuen Warnungen
