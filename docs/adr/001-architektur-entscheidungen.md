# ADR-001: Architektur-Entscheidungen

**Status:** Akzeptiert
**Datum:** 2024-01-01
**Entscheider:** PMTool Team

## Kontext

Wir entwickeln ein lokales Projektmanagement-Tool mit GUI. Das Tool soll:
- Projekte und Tasks verwalten
- Eine Gantt-Darstellung bieten
- Daten lokal persistieren
- Wartbar und erweiterbar sein

## Entscheidungen

### 1. Schichtenarchitektur

**Entscheidung:** Vier-Schichten-Architektur mit strikter Abhängigkeitsrichtung.

```
┌─────────────────────────────────────┐
│              UI Layer               │ ← PySide6 Widgets
├─────────────────────────────────────┤
│           Service Layer             │ ← Use-Cases, Geschäftslogik
├─────────────────────────────────────┤
│          Repository Layer           │ ← Datenzugriff
├─────────────────────────────────────┤
│           Domain Layer              │ ← Modelle, Enums
└─────────────────────────────────────┘
```

**Begründung:**
- Klare Trennung der Verantwortlichkeiten
- Testbarkeit durch Isolation der Schichten
- UI kann ausgetauscht werden ohne Business-Logik zu ändern
- Datenbank kann gewechselt werden ohne Service-Änderungen

**Regeln:**
- UI greift nur auf Services zu
- Services nutzen Repositories, niemals direkte DB-Zugriffe
- Repositories arbeiten nur mit Domain-Modellen
- Domain hat keine Abhängigkeiten zu anderen Schichten

### 2. Domain-Modelle als Dataclasses

**Entscheidung:** Alle Domain-Entitäten als Python dataclasses implementieren.

**Begründung:**
- Immutability per Default möglich (frozen=True wo sinnvoll)
- Automatische `__init__`, `__repr__`, `__eq__`
- Type Hints sind integraler Bestandteil
- Leichtgewichtig, keine ORM-Abhängigkeit

**Beispiel:**
```python
@dataclass
class Task:
    id: int
    project_id: int
    title: str
    status: TaskStatus
    # ...
```

### 3. PySide6 als GUI-Framework

**Entscheidung:** PySide6 (Qt for Python) als GUI-Framework.

**Begründung:**
- Native Look & Feel auf allen Plattformen
- Mächtige Widgets (Table, Tree, Custom Painting für Gantt)
- Gute Python-Integration mit Signals/Slots
- LGPL-Lizenz erlaubt kommerzielle Nutzung
- Aktive Entwicklung durch Qt Company

**Alternativen betrachtet:**
- Tkinter: Zu limitiert für komplexe UIs
- PyQt6: GPL-Lizenz problematisch
- Kivy: Nicht-native UI, eher für Mobile

### 4. SQLite als Persistenz

**Entscheidung:** SQLite als eingebettete Datenbank.

**Begründung:**
- Keine separate Serverinstallation nötig
- Datei-basiert, einfaches Backup
- Ausreichend performant für Einzelbenutzer
- In Python-Standardbibliothek enthalten

**Schema-Management:**
- Versionierte Migrationen im Code
- Schema-Version in DB gespeichert

### 5. Repository Pattern

**Entscheidung:** Repository-Klassen kapseln alle Datenbankzugriffe.

**Begründung:**
- Abstraktion der Persistenz-Technologie
- Einfaches Mocking in Tests
- Zentralisierte SQL-Queries
- Konsistente API für CRUD-Operationen

**Interface:**
```python
class ProjectRepository:
    def get_all() -> list[Project]
    def get_by_id(id: int) -> Project | None
    def create(project: Project) -> Project
    def update(project: Project) -> Project
    def delete(id: int) -> bool
```

### 6. Service Layer für Geschäftslogik

**Entscheidung:** Services implementieren Use-Cases und Validierung.

**Begründung:**
- Zentrale Stelle für Geschäftsregeln
- Unabhängig von UI und Persistenz testbar
- Koordiniert Repository-Aufrufe
- Validiert Eingaben vor Persistierung

**Beispiel Use-Cases:**
- `create_project()` - validiert und speichert Projekt
- `update_task_progress()` - prüft Bereich 0-100
- `export_tasks_csv()` - aggregiert und exportiert

## Konsequenzen

### Positiv
- Hohe Testbarkeit durch Isolation
- Flexibilität bei Technologie-Änderungen
- Klare Code-Organisation

### Negativ
- Mehr Boilerplate-Code durch Schichten
- Mapping zwischen Schichten nötig
- Lernkurve für Entwickler

## Compliance

Diese Entscheidungen sind verbindlich für alle Entwickler. Abweichungen erfordern ein neues ADR.
