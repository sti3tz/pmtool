# Requirements

## Zweck

Dieses Dokument definiert die funktionalen und nicht-funktionalen Anforderungen für PMTool.

## Scope

PMTool ist ein lokales Projektmanagement-Tool für Einzelbenutzer zur Verwaltung von Projekten und Tasks mit einfacher Gantt-Darstellung.

## Funktionale Anforderungen

### F1: Projektverwaltung

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| F1.1 | Benutzer kann neue Projekte anlegen | Must |
| F1.2 | Benutzer kann Projekte bearbeiten | Must |
| F1.3 | Benutzer kann Projekte löschen | Must |
| F1.4 | Projekt hat Name (Pflicht), Beschreibung, Start-/Enddatum | Must |

### F2: Task-Management

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| F2.1 | Tasks sind einem Projekt zugeordnet | Must |
| F2.2 | Task hat Titel (Pflicht), Owner | Must |
| F2.3 | Task hat Start- und Enddatum | Must |
| F2.4 | Task hat Status: TODO, IN_PROGRESS, DONE | Must |
| F2.5 | Task hat Priorität: LOW, MEDIUM, HIGH, CRITICAL | Must |
| F2.6 | Task hat Fortschritt 0-100% | Must |
| F2.7 | Task kann Notizen haben | Should |

### F3: Ansichten

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| F3.1 | Projektliste als Übersicht | Must |
| F3.2 | Task-Tabelle je Projekt | Must |
| F3.3 | Gantt-Light-Ansicht mit Zeitbalken | Must |

### F4: Export

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| F4.1 | CSV-Export der Tasks eines Projekts | Must |

### F5: Validierung

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| F5.1 | Pflichtfelder werden validiert | Must |
| F5.2 | Startdatum <= Enddatum | Must |
| F5.3 | Fortschritt im Bereich 0-100 | Must |

## Nicht-funktionale Anforderungen

| ID | Anforderung | Kategorie |
|----|-------------|-----------|
| NF1 | Python >= 3.11 | Technologie |
| NF2 | PySide6 für GUI | Technologie |
| NF3 | SQLite für Persistenz | Technologie |
| NF4 | Testabdeckung >= 80% | Qualität |
| NF5 | Response-Zeit < 200ms für UI-Operationen | Performance |

## Explizite Nicht-Ziele

- Multi-User-Funktionalität
- Cloud-Synchronisation
- Rechte- und Rollenkonzepte
- Ressourcen- oder Kostenplanung
- Dependency-Tracking zwischen Tasks

## Definition of Done

Eine Anforderung gilt als erfüllt, wenn:
1. Feature implementiert und funktional
2. Unit-Tests vorhanden und grün
3. Code-Review durchgeführt
4. Dokumentation aktualisiert
