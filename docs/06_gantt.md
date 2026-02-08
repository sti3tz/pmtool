# Gantt-Ansicht

## Übersicht

Die Gantt-Light-Ansicht zeigt Tasks als horizontale Zeitbalken auf einer Zeitachse. Sie bietet einen schnellen visuellen Überblick über die Zeitplanung.

## Features

### Zeitbalken

- Jeder Task mit Start- und Enddatum wird als horizontaler Balken dargestellt
- Balkenlänge entspricht der Task-Dauer
- Farbcodierung nach Task-Status

### Fortschrittsanzeige

- Bei Tasks mit Fortschritt 0 < progress < 100 wird ein dunklerer Teil des Balkens angezeigt
- Fortschrittswert als Text im Balken (wenn Balken breit genug)

### Zeitachse

- Automatische Berechnung des Datumsbereichs
- Datum-Labels mit automatischer Skalierung
- Wochenenden (Sa/So) werden grau hinterlegt

### Heute-Linie

- Vertikale gestrichelte Linie in Rot markiert das aktuelle Datum
- Nur sichtbar, wenn das heutige Datum im Anzeigebereich liegt

## Technische Umsetzung

Die Gantt-Ansicht ist als Custom Widget (`QWidget`) implementiert, das im `paintEvent` alle Elemente zeichnet.

### Konstanten

```python
ROW_HEIGHT = 30      # Höhe pro Task-Zeile
HEADER_HEIGHT = 40   # Höhe des Zeitachsen-Headers
LEFT_MARGIN = 200    # Platz für Task-Namen
RIGHT_MARGIN = 20    # Rechter Rand
```

### Zeichenreihenfolge

1. Hintergrund (weiß)
2. Header mit Datum-Labels
3. Grid (Wochenenden, horizontale Linien)
4. Task-Balken mit Fortschritt
5. Heute-Linie

## Einschränkungen

Die aktuelle Implementierung ist eine "Light"-Version:

**Nicht enthalten:**
- Zoom-Funktionalität
- Scrollbare Zeitachse
- Drag & Drop zum Verschieben
- Dependencies zwischen Tasks
- Ressourcen-Zeilen
- Meilensteine

## Erweiterungsmöglichkeiten

Für zukünftige Versionen:

1. **Zoom**: Tages-/Wochen-/Monatsansicht
2. **Scroll**: Bei vielen Tasks oder langem Zeitraum
3. **Interaktion**: Balken per Drag & Drop verschieben
4. **Tooltips**: Details beim Hover

## Beispiel-Darstellung

```
     │ 01.01 │ 08.01 │ 15.01 │ 22.01 │
─────┼───────┼───────┼───────┼───────┤
Task1│ ██████████████│       │       │
     │       │       │       │       │
Task2│       │ ██████│███████│       │
     │       │       │       │       │
Task3│       │       │   ████│███████│
─────┴───────┴───────┴───────┴───────┤
                          ┃
                     Heute-Linie
```
