# Datenbankschema

## Übersicht

PMTool verwendet SQLite als eingebettete Datenbank. Das Schema ist einfach und besteht aus zwei Haupttabellen.

## Entity-Relationship-Diagramm

```
┌──────────────────────────────────┐
│            projects              │
├──────────────────────────────────┤
│ id (PK)        INTEGER          │
│ name           TEXT NOT NULL     │
│ description    TEXT              │
│ start_date     TEXT              │
│ end_date       TEXT              │
│ created_at     TEXT              │
│ updated_at     TEXT              │
└──────────────────────────────────┘
         │
         │ 1:n
         ▼
┌──────────────────────────────────┐
│             tasks                │
├──────────────────────────────────┤
│ id (PK)        INTEGER          │
│ project_id (FK) INTEGER NOT NULL│
│ title          TEXT NOT NULL     │
│ owner          TEXT              │
│ start_date     TEXT              │
│ end_date       TEXT              │
│ status         TEXT              │
│ priority       TEXT              │
│ progress       INTEGER           │
│ notes          TEXT              │
│ created_at     TEXT              │
│ updated_at     TEXT              │
└──────────────────────────────────┘
```

## Tabellen

### projects

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| id | INTEGER | Primärschlüssel, Auto-Increment |
| name | TEXT NOT NULL | Projektname |
| description | TEXT | Optionale Beschreibung |
| start_date | TEXT | ISO-Datum (YYYY-MM-DD) |
| end_date | TEXT | ISO-Datum (YYYY-MM-DD) |
| created_at | TEXT | Erstellungszeitpunkt |
| updated_at | TEXT | Letzte Änderung |

### tasks

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| id | INTEGER | Primärschlüssel, Auto-Increment |
| project_id | INTEGER NOT NULL | Fremdschlüssel auf projects.id |
| title | TEXT NOT NULL | Task-Titel |
| owner | TEXT | Verantwortliche Person |
| start_date | TEXT | ISO-Datum |
| end_date | TEXT | ISO-Datum |
| status | TEXT | TODO, IN_PROGRESS, DONE |
| priority | TEXT | LOW, MEDIUM, HIGH, CRITICAL |
| progress | INTEGER | 0-100 (CHECK-Constraint) |
| notes | TEXT | Zusätzliche Notizen |
| created_at | TEXT | Erstellungszeitpunkt |
| updated_at | TEXT | Letzte Änderung |

## Constraints

- `tasks.progress` muss zwischen 0 und 100 liegen
- `tasks.project_id` referenziert `projects.id` mit CASCADE DELETE
- Foreign Keys sind aktiviert (`PRAGMA foreign_keys = ON`)

## Indizes

| Index | Tabelle | Spalten | Zweck |
|-------|---------|---------|-------|
| idx_tasks_project_id | tasks | project_id | Schnelle Abfrage nach Projekt |
| idx_tasks_status | tasks | status | Filterung nach Status |

## Schema-Migration

Die Schema-Version wird in der Tabelle `schema_info` gespeichert:

```sql
CREATE TABLE schema_info (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

Bei Änderungen am Schema wird die Version inkrementiert und Migrations-Skripte ausgeführt.

## Backup

Die Datenbank kann durch einfaches Kopieren der `.db`-Datei gesichert werden:

```bash
# macOS
cp ~/Library/Application\ Support/PMTool/pmtool.db ~/backup/pmtool_backup.db

# Linux
cp ~/.local/share/pmtool/pmtool.db ~/backup/pmtool_backup.db
```
