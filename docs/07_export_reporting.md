# Export & Reporting

## CSV-Export

### Funktionalität

Der CSV-Export ermöglicht das Exportieren aller Tasks eines Projekts in eine CSV-Datei.

### Aufruf

1. Projekt in der Projektliste auswählen
2. Auf "CSV Export" klicken
3. Zieldatei im Dialog wählen
4. Export wird durchgeführt

### Dateiformat

- Trennzeichen: Semikolon (`;`)
- Encoding: UTF-8
- Zeilenende: Plattformabhängig

### Spalten

| Spalte | Beschreibung |
|--------|--------------|
| ID | Task-ID |
| Titel | Task-Titel |
| Owner | Verantwortliche Person |
| Start | Startdatum (ISO-Format) |
| Ende | Enddatum (ISO-Format) |
| Status | Anzeigename (Offen/In Arbeit/Erledigt) |
| Priorität | Anzeigename (Niedrig/Mittel/Hoch/Kritisch) |
| Fortschritt (%) | Fortschritt als Zahl |
| Notizen | Notizen (Zeilenumbrüche entfernt) |

### Beispiel-Export

```csv
ID;Titel;Owner;Start;Ende;Status;Priorität;Fortschritt (%);Notizen
1;Anforderungen sammeln;Max;2024-01-01;2024-01-10;Erledigt;Hoch;100;Abgeschlossen
2;Prototyp erstellen;Anna;2024-01-05;2024-01-20;In Arbeit;Mittel;60;UI-Design fehlt noch
3;Tests schreiben;Tim;2024-01-15;2024-01-25;Offen;Niedrig;0;
```

## API

### ExportService

```python
class ExportService:
    def export_tasks_to_csv(
        self,
        project_id: int,
        file_path: str | Path
    ) -> int:
        """Exportiert Tasks als CSV-Datei.

        Returns:
            Anzahl exportierter Tasks
        """

    def export_tasks_to_string(
        self,
        project_id: int
    ) -> str:
        """Exportiert Tasks als CSV-String.

        Returns:
            CSV-Daten als String
        """
```

## Zukünftige Erweiterungen

Mögliche Erweiterungen für spätere Versionen:

### Weitere Formate
- Excel (XLSX) mit openpyxl
- PDF-Report mit reportlab
- JSON-Export

### Report-Funktionen
- Projekt-Übersichtsreport
- Fortschritts-Zusammenfassung
- Überfällige Tasks

### Import
- CSV-Import für Bulk-Erstellung
- Import aus anderen Tools
