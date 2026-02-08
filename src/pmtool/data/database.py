"""Datenbank-Verbindungsmanagement und Schema-Migration."""

import sqlite3
from pathlib import Path
from typing import Self

# Aktuelles Schema-Version
SCHEMA_VERSION = 1

# SQL-Statements für Schema-Erstellung
CREATE_SCHEMA = """
-- Metadaten-Tabelle für Schema-Version
CREATE TABLE IF NOT EXISTS schema_info (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Projekte-Tabelle
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    start_date TEXT,
    end_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tasks-Tabelle
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    owner TEXT DEFAULT '',
    start_date TEXT,
    end_date TEXT,
    status TEXT DEFAULT 'TODO',
    priority TEXT DEFAULT 'MEDIUM',
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    notes TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Indizes für Performance
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
"""


class Database:
    """Verwaltet die SQLite-Datenbankverbindung und Schema-Migration.

    Diese Klasse ist als Context Manager verwendbar und stellt sicher,
    dass Verbindungen ordnungsgemäß geschlossen werden.

    Attributes:
        db_path: Pfad zur SQLite-Datenbankdatei
    """

    def __init__(self, db_path: str | Path = "pmtool.db") -> None:
        """Initialisiert die Datenbankverbindung.

        Args:
            db_path: Pfad zur Datenbankdatei. Standard: 'pmtool.db' im aktuellen Verzeichnis.
                    Kann ':memory:' für In-Memory-Datenbank sein.
        """
        self.db_path = Path(db_path) if isinstance(db_path, str) else db_path
        self._connection: sqlite3.Connection | None = None

    def __enter__(self) -> Self:
        """Context Manager Entry - öffnet die Datenbankverbindung."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager Exit - schließt die Datenbankverbindung."""
        self.close()

    @property
    def connection(self) -> sqlite3.Connection:
        """Gibt die aktive Datenbankverbindung zurück.

        Raises:
            RuntimeError: Wenn keine Verbindung besteht.
        """
        if self._connection is None:
            raise RuntimeError("Keine Datenbankverbindung aktiv. Rufe connect() auf.")
        return self._connection

    def connect(self) -> None:
        """Öffnet die Datenbankverbindung und initialisiert das Schema."""
        if self._connection is not None:
            return

        self._connection = sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def close(self) -> None:
        """Schließt die Datenbankverbindung."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def _initialize_schema(self) -> None:
        """Erstellt oder migriert das Datenbankschema."""
        cursor = self.connection.cursor()

        # Prüfe, ob schema_info existiert
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_info'")
        if cursor.fetchone() is None:
            # Neues Schema erstellen
            cursor.executescript(CREATE_SCHEMA)
            cursor.execute(
                "INSERT INTO schema_info (key, value) VALUES (?, ?)",
                ("version", str(SCHEMA_VERSION)),
            )
            self.connection.commit()
        else:
            # Schema-Migration falls nötig
            cursor.execute("SELECT value FROM schema_info WHERE key = 'version'")
            row = cursor.fetchone()
            if row:
                current_version = int(row["value"])
                if current_version < SCHEMA_VERSION:
                    self._migrate_schema(current_version)

    def _migrate_schema(self, _from_version: int) -> None:
        """Führt Schema-Migrationen durch.

        Args:
            from_version: Aktuelle Schema-Version in der Datenbank
        """
        cursor = self.connection.cursor()

        # Migrations-Logik für zukünftige Versionen
        # if from_version < 2:
        #     cursor.execute("ALTER TABLE ...")
        #     from_version = 2

        cursor.execute(
            "UPDATE schema_info SET value = ? WHERE key = 'version'",
            (str(SCHEMA_VERSION),),
        )
        self.connection.commit()

    def execute(self, sql: str, parameters: tuple = ()) -> sqlite3.Cursor:
        """Führt ein SQL-Statement aus.

        Args:
            sql: SQL-Statement
            parameters: Parameter für das Statement

        Returns:
            Cursor mit Ergebnissen
        """
        return self.connection.execute(sql, parameters)

    def executemany(self, sql: str, parameters: list[tuple]) -> sqlite3.Cursor:
        """Führt ein SQL-Statement für mehrere Datensätze aus.

        Args:
            sql: SQL-Statement
            parameters: Liste von Parameter-Tupeln

        Returns:
            Cursor mit Ergebnissen
        """
        return self.connection.executemany(sql, parameters)

    def commit(self) -> None:
        """Bestätigt die aktuelle Transaktion."""
        self.connection.commit()

    def rollback(self) -> None:
        """Macht die aktuelle Transaktion rückgängig."""
        self.connection.rollback()
