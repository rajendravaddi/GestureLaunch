import time
from typing import List, Optional

from PySide6.QtCore import QPointF, QRectF, QTimer, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from app.models.gesture import Gesture, Point, Stroke


class GestureCanvas(QWidget):
    """Custom canvas widget for drawing, recording, and previewing touchpad/mouse gestures."""

    gestureRecorded = Signal(list)  # List[Stroke]

    def __init__(self, parent: QWidget = None, readonly: bool = False) -> None:
        super().__init__(parent)
        self.readonly = readonly
        self.strokes: List[Stroke] = []
        self.current_stroke: Optional[Stroke] = None

        self._playback_index = 0
        self._playback_timer = QTimer(self)
        self._playback_timer.timeout.connect(self._update_playback)
        self._playback_points: List[Point] = []
        self._playback_render_count = 0

        self.setMinimumSize(300, 300)
        self.setMouseTracking(True)
        self.setObjectName("CardFrame")

    def clear(self) -> None:
        self.strokes = []
        self.current_stroke = None
        self._playback_timer.stop()
        self._playback_points = []
        self.update()

    def set_strokes(self, strokes: List[Stroke]) -> None:
        self.strokes = strokes
        self.current_stroke = None
        self.update()

    def play_preview(self) -> None:
        """Animates playback of existing gesture strokes."""
        all_points = []
        for stroke in self.strokes:
            all_points.extend(stroke.points)

        if not all_points:
            return

        self._playback_points = all_points
        self._playback_render_count = 0
        self._playback_timer.start(25)  # 40 fps animation

    def _update_playback(self) -> None:
        if self._playback_render_count < len(self._playback_points):
            self._playback_render_count += 1
            self.update()
        else:
            self._playback_timer.stop()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.readonly or event.button() != Qt.MouseButton.LeftButton:
            return

        w, h = self.width(), self.height()
        norm_x = event.position().x() / w
        norm_y = event.position().y() / h

        self.current_stroke = Stroke(points=[Point(x=norm_x, y=norm_y, timestamp=time.time())])
        self.strokes.append(self.current_stroke)
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.readonly or not (event.buttons() & Qt.MouseButton.LeftButton) or not self.current_stroke:
            return

        w, h = self.width(), self.height()
        norm_x = max(0.0, min(1.0, event.position().x() / w))
        norm_y = max(0.0, min(1.0, event.position().y() / h))

        self.current_stroke.points.append(Point(x=norm_x, y=norm_y, timestamp=time.time()))
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.readonly or event.button() != Qt.MouseButton.LeftButton:
            return

        if self.current_stroke:
            self.current_stroke = None
            self.gestureRecorded.emit(self.strokes)
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Canvas background grid/border
        painter.fillRect(self.rect(), QColor("#181825"))

        # Subtle crosshair pattern
        painter.setPen(QPen(QColor("#313244"), 1, Qt.PenStyle.DashLine))
        painter.drawLine(int(w / 2), 0, int(w / 2), h)
        painter.drawLine(0, int(h / 2), w, int(h / 2))

        # Check if running playback preview
        if self._playback_timer.isActive() and self._playback_points:
            self._draw_playback(painter, w, h)
        else:
            self._draw_strokes(painter, w, h)

        if not self.strokes and not self._playback_timer.isActive():
            painter.setPen(QColor("#6c7086"))
            msg = "Click & Drag here to draw gesture" if not self.readonly else "No gesture recorded"
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, msg)

    def _draw_strokes(self, painter: QPainter, w: float, h: float) -> None:
        # Glow outer stroke
        glow_pen = QPen(QColor(137, 180, 250, 60), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        # Main vibrant inner stroke
        main_pen = QPen(QColor("#89b4fa"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

        for stroke in self.strokes:
            if len(stroke.points) < 2:
                continue

            path = QPainterPath()
            path.moveTo(stroke.points[0].x * w, stroke.points[0].y * h)
            for pt in stroke.points[1:]:
                path.lineTo(pt.x * w, pt.y * h)

            painter.setPen(glow_pen)
            painter.drawPath(path)

            painter.setPen(main_pen)
            painter.drawPath(path)

            # Draw start point marker
            start = stroke.points[0]
            painter.setBrush(QColor("#a6e3a1"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(start.x * w, start.y * h), 5, 5)

    def _draw_playback(self, painter: QPainter, w: float, h: float) -> None:
        pts = self._playback_points[: self._playback_render_count]
        if len(pts) < 2:
            return

        path = QPainterPath()
        path.moveTo(pts[0].x * w, pts[0].y * h)
        for pt in pts[1:]:
            path.lineTo(pt.x * w, pt.y * h)

        # Glow outer stroke
        painter.setPen(QPen(QColor(249, 226, 175, 80), 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)

        # Vibrant gold playback stroke
        painter.setPen(QPen(QColor("#f9e2af"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)

        # Lead point animation dot
        lead = pts[-1]
        painter.setBrush(QColor("#fab387"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(lead.x * w, lead.y * h), 7, 7)
