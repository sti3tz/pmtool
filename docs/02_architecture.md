# Architektur

## Übersicht

PMTool folgt einer klassischen Schichtenarchitektur mit vier Ebenen.

```
┌─────────────────────────────────────────────────────────────┐
│                        UI Layer                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ MainWindow  │ │ ProjectView │ │ TaskTableWidget     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      Service Layer                          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐  │
│  │ ProjectService  │ │ TaskService     │ │ ExportService│  │
│  └─────────────────┘ └─────────────────┘ └──────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Repository Layer                         │
│  ┌──────────────────┐ ┌──────────────────┐                 │
│  │ ProjectRepository│ │ TaskRepository   │                 │
│  └──────────────────┘ └──────────────────┘                 │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│  ┌─────────┐ ┌──────┐ ┌────────────┐ ┌────────────────┐    │
│  │ Project │ │ Task │ │ TaskStatus │ │ TaskPriority   │    │
│  └─────────┘ └──────┘ └────────────┘ └────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Schichten im Detail

### Domain Layer (`src/pmtool/domain/`)

Enthält die Kern-Entitäten und Enums:

- **Project**: Projekt-Entität mit ID, Name, Beschreibung, Zeitraum
- **Task**: Task-Entität mit allen Attributen
- **TaskStatus**: Enum (TODO, IN_PROGRESS, DONE)
- **TaskPriority**: Enum (LOW, MEDIUM, HIGH, CRITICAL)

Keine Abhängigkeiten zu anderen Schichten.

### Repository Layer (`src/pmtool/data/`)

Kapselt die SQLite-Datenbankzugriffe:

- **Database**: Connection-Management, Schema-Migration
- **ProjectRepository**: CRUD für Projekte
- **TaskRepository**: CRUD für Tasks

Abhängigkeit: Domain Layer

### Service Layer (`src/pmtool/services/`)

Implementiert die Geschäftslogik:

- **ProjectService**: Projekt-Use-Cases mit Validierung
- **TaskService**: Task-Use-Cases mit Validierung
- **ExportService**: CSV-Export-Funktionalität

Abhängigkeiten: Repository Layer, Domain Layer

### UI Layer (`src/pmtool/ui/`)

PySide6-basierte Benutzeroberfläche:

- **MainWindow**: Hauptfenster mit Navigation
- **ProjectListWidget**: Projektübersicht
- **TaskTableWidget**: Task-Tabelle
- **GanttWidget**: Gantt-Darstellung
- **Dialogs**: Formulare für CRUD-Operationen

Abhängigkeiten: Service Layer, Domain Layer

## Datenfluss

```
User Input
    │
    ▼
┌─────────┐     Signal      ┌─────────────┐
│   UI    │ ───────────────▶│   Service   │
└─────────┘                 └─────────────┘
    ▲                             │
    │                             ▼
    │                       ┌─────────────┐
    │      Domain Object    │ Repository  │
    └───────────────────────└─────────────┘
                                  │
                                  ▼
                            ┌─────────────┐
                            │   SQLite    │
                            └─────────────┘
```

## Verzeichnisstruktur

```
src/pmtool/
├── __init__.py
├── app.py                 # Einstiegspunkt
├── domain/
│   ├── __init__.py
│   ├── project.py         # Project dataclass
│   ├── task.py            # Task dataclass
│   └── enums.py           # Status, Priority
├── data/
│   ├── __init__.py
│   ├── database.py        # DB-Verbindung
│   ├── project_repository.py
│   └── task_repository.py
├── services/
│   ├── __init__.py
│   ├── project_service.py
│   ├── task_service.py
│   └── export_service.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── project_list.py
│   ├── task_table.py
│   ├── gantt_widget.py
│   └── dialogs/
│       ├── __init__.py
│       ├── project_dialog.py
│       └── task_dialog.py
└── util/
    ├── __init__.py
    └── validators.py
```

## Design-Entscheidungen

Siehe [ADR-001: Architektur-Entscheidungen](adr/001-architektur-entscheidungen.md)
