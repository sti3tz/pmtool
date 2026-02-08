"""Widget für die Gantt-Darstellung."""

from datetime import date, timedelta

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from pmtool.domain.enums import TaskStatus
from pmtool.domain.project import Project
from pmtool.domain.task import Task


class GanttWidget(QWidget):
    """Widget zur Darstellung eines einfachen Gantt-Charts.

    Zeigt Tasks als horizontale Balken auf einer Zeitachse.
    """

    # Farben für Task-Status
    STATUS_COLORS = {
        TaskStatus.TODO: QColor("#6c757d"),
        TaskStatus.IN_PROGRESS: QColor("#0d6efd"),
        TaskStatus.DONE: QColor("#198754"),
    }

    # Konstanten für Layout
    ROW_HEIGHT = 30
    HEADER_HEIGHT = 40
    LEFT_MARGIN = 200
    RIGHT_MARGIN = 20
    TOP_MARGIN = 10

    def __init__(self) -> None:
        """Initialisiert das Gantt-Widget."""
        super().__init__()
        self._tasks: list[Task] = []
        self._project: Project | None = None
        self._date_range: tuple[date, date] | None = None
        self.setMinimumHeight(200)

    def set_tasks(self, tasks: list[Task], project: Project) -> None:
        """Setzt die anzuzeigenden Tasks.

        Args:
            tasks: Liste der Tasks
            project: Zugehöriges Projekt
        """
        self._tasks = [t for t in tasks if t.start_date and t.end_date]
        self._project = project
        self._calculate_date_range()
        self.update()

    def clear(self) -> None:
        """Leert die Gantt-Anzeige."""
        self._tasks = []
        self._project = None
        self._date_range = None
        self.update()

    def _calculate_date_range(self) -> None:
        """Berechnet den anzuzeigenden Datumsbereich."""
        if not self._tasks:
            self._date_range = None
            return

        all_dates = []
        for task in self._tasks:
            if task.start_date:
                all_dates.append(task.start_date)
            if task.end_date:
                all_dates.append(task.end_date)

        if self._project:
            if self._project.start_date:
                all_dates.append(self._project.start_date)
            if self._project.end_date:
                all_dates.append(self._project.end_date)

        if all_dates:
            min_date = min(all_dates)
            max_date = max(all_dates)
            # Etwas Puffer hinzufügen
            self._date_range = (
                min_date - timedelta(days=1),
                max_date + timedelta(days=1),
            )
        else:
            self._date_range = None

    def paintEvent(self, _event) -> None:
        """Zeichnet das Gantt-Chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Hintergrund
        painter.fillRect(self.rect(), QColor("#ffffff"))

        if not self._tasks or not self._date_range:
            self._draw_empty_message(painter)
            return

        self._draw_header(painter)
        self._draw_grid(painter)
        self._draw_tasks(painter)
        self._draw_today_line(painter)

    def _draw_empty_message(self, painter: QPainter) -> None:
        """Zeichnet eine Nachricht wenn keine Tasks vorhanden sind."""
        painter.setPen(QColor("#6c757d"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "Keine Tasks mit Datumsangaben vorhanden",
        )

    def _draw_header(self, painter: QPainter) -> None:
        """Zeichnet den Zeitachsen-Header."""
        if not self._date_range:
            return

        start_date, end_date = self._date_range
        total_days = (end_date - start_date).days + 1
        chart_width = self.width() - self.LEFT_MARGIN - self.RIGHT_MARGIN

        if total_days <= 0 or chart_width <= 0:
            return

        day_width = chart_width / total_days

        # Header-Hintergrund
        painter.fillRect(
            QRectF(self.LEFT_MARGIN, 0, chart_width, self.HEADER_HEIGHT),
            QColor("#f8f9fa"),
        )

        painter.setPen(QColor("#495057"))
        painter.setFont(QFont("Arial", 9))

        # Datum-Labels (nicht jeden Tag bei vielen Tagen)
        step = max(1, total_days // 15)
        for i in range(0, total_days, step):
            current_date = start_date + timedelta(days=i)
            x = self.LEFT_MARGIN + i * day_width

            painter.drawText(
                QRectF(x - 25, self.HEADER_HEIGHT - 20, 50, 20),
                Qt.AlignmentFlag.AlignCenter,
                current_date.strftime("%d.%m"),
            )

    def _draw_grid(self, painter: QPainter) -> None:
        """Zeichnet das Hintergrund-Grid."""
        if not self._date_range:
            return

        start_date, end_date = self._date_range
        total_days = (end_date - start_date).days + 1
        chart_width = self.width() - self.LEFT_MARGIN - self.RIGHT_MARGIN
        chart_height = len(self._tasks) * self.ROW_HEIGHT

        if total_days <= 0 or chart_width <= 0:
            return

        day_width = chart_width / total_days

        # Vertikale Linien (Wochenenden markieren)
        for i in range(total_days + 1):
            current_date = start_date + timedelta(days=i)
            x = self.LEFT_MARGIN + i * day_width

            if current_date.weekday() >= 5:  # Samstag oder Sonntag
                painter.fillRect(
                    QRectF(
                        x,
                        self.HEADER_HEIGHT,
                        day_width,
                        chart_height + self.TOP_MARGIN,
                    ),
                    QColor("#f1f3f4"),
                )

        # Horizontale Linien
        pen = QPen(QColor("#dee2e6"))
        pen.setWidth(1)
        painter.setPen(pen)

        for i in range(len(self._tasks) + 1):
            y = self.HEADER_HEIGHT + self.TOP_MARGIN + i * self.ROW_HEIGHT
            painter.drawLine(self.LEFT_MARGIN, y, self.width() - self.RIGHT_MARGIN, y)

    def _draw_tasks(self, painter: QPainter) -> None:
        """Zeichnet die Task-Balken."""
        if not self._date_range:
            return

        start_date, end_date = self._date_range
        total_days = (end_date - start_date).days + 1
        chart_width = self.width() - self.LEFT_MARGIN - self.RIGHT_MARGIN

        if total_days <= 0 or chart_width <= 0:
            return

        day_width = chart_width / total_days

        for i, task in enumerate(self._tasks):
            y = self.HEADER_HEIGHT + self.TOP_MARGIN + i * self.ROW_HEIGHT

            # Task-Name
            painter.setPen(QColor("#212529"))
            painter.setFont(QFont("Arial", 10))
            name_rect = QRectF(5, y + 5, self.LEFT_MARGIN - 10, self.ROW_HEIGHT - 10)
            painter.drawText(
                name_rect,
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                task.title[:25] + ("..." if len(task.title) > 25 else ""),
            )

            # Task-Balken
            if task.start_date and task.end_date:
                task_start = (task.start_date - start_date).days
                task_duration = (task.end_date - task.start_date).days + 1

                x = self.LEFT_MARGIN + task_start * day_width
                width = task_duration * day_width
                bar_height = self.ROW_HEIGHT - 10

                # Hintergrund
                color = self.STATUS_COLORS.get(task.status, QColor("#6c757d"))
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(
                    QRectF(x, y + 5, width, bar_height),
                    3,
                    3,
                )

                # Fortschrittsbalken
                if task.progress > 0 and task.progress < 100:
                    progress_width = width * (task.progress / 100)
                    darker_color = color.darker(120)
                    painter.setBrush(QBrush(darker_color))
                    painter.drawRoundedRect(
                        QRectF(x, y + 5, progress_width, bar_height),
                        3,
                        3,
                    )

                # Fortschrittstext
                if width > 30:
                    painter.setPen(QColor("#ffffff"))
                    painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                    painter.drawText(
                        QRectF(x, y + 5, width, bar_height),
                        Qt.AlignmentFlag.AlignCenter,
                        f"{task.progress}%",
                    )

    def _draw_today_line(self, painter: QPainter) -> None:
        """Zeichnet eine Linie für das heutige Datum."""
        if not self._date_range:
            return

        today = date.today()
        start_date, end_date = self._date_range

        if not (start_date <= today <= end_date):
            return

        total_days = (end_date - start_date).days + 1
        chart_width = self.width() - self.LEFT_MARGIN - self.RIGHT_MARGIN

        if total_days <= 0 or chart_width <= 0:
            return

        day_width = chart_width / total_days
        days_from_start = (today - start_date).days
        x = self.LEFT_MARGIN + days_from_start * day_width + day_width / 2

        pen = QPen(QColor("#dc3545"))
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)

        chart_height = len(self._tasks) * self.ROW_HEIGHT + self.TOP_MARGIN
        painter.drawLine(
            int(x),
            self.HEADER_HEIGHT,
            int(x),
            self.HEADER_HEIGHT + chart_height,
        )
