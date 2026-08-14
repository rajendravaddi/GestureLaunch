import time
from typing import List, Optional

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QMouseEvent, QPaintEvent, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from app.models.gesture import Point, Stroke


class GestureOverlayWindow(QWidget):
    """Fullscreen transparent overlay canvas displaying real-time gesture stroke trails on screen."""

    gestureCaptured = Signal(list)  # Emits List[Stroke]

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, False)

        self.strokes: List[Stroke] = []
        self.current_stroke: Optional[Stroke] = None
        self.is_drawing = False

    def activate_overlay(self) -> None:
        """Shows fullscreen gesture canvas overlay."""
        self.strokes = []
        self.current_stroke = None
        self.is_drawing = True

        # Position over active screen
        screen = self.screen()
        if screen:
            self.setGeometry(screen.geometry())

        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.update()

    def deactivate_overlay(self) -> None:
        """Hides overlay and emits captured gesture strokes."""
        self.hide()
        if self.strokes:
            self.gestureCaptured.emit(self.strokes)
        self.strokes = []
        self.current_stroke = None
        self.is_drawing = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = True
            w, h = self.width(), self.height()
            norm_x = event.position().x() / w
            norm_y = event.position().y() / h

            self.current_stroke = Stroke(points=[Point(x=norm_x, y=norm_y)])
            self.strokes.append(self.current_stroke)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # If drawing mode is active, append points as mouse/touchpad moves
        if self.is_drawing:
            w, h = self.width(), self.height()
            norm_x = max(0.0, min(1.0, event.position().x() / w))
            norm_y = max(0.0, min(1.0, event.position().y() / h))

            if not self.current_stroke:
                self.current_stroke = Stroke(points=[Point(x=norm_x, y=norm_y)])
                self.strokes.append(self.current_stroke)
            else:
                self.current_stroke.points.append(Point(x=norm_x, y=norm_y))
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            self.is_drawing = False
            self.current_stroke = None
            self.deactivate_overlay()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        # Pressing ESC cancels overlay cleanly
        if event.key() == Qt.Key.Key_Escape:
            self.strokes = []
            self.current_stroke = None
            self.hide()
        super().keyReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Semi-transparent dark overlay tint (indicates drawing mode)
        painter.fillRect(self.rect(), QColor(17, 17, 27, 110))

        # Instructions Header Banner
        painter.setPen(QColor("#f5e0dc"))
        font = painter.font()
        font.setPointSize(16)
        font.setBold(True)
        painter.setFont(font)

        banner_rect = self.rect()
        banner_rect.setHeight(90)
        painter.drawText(
            banner_rect,
            Qt.AlignmentFlag.AlignCenter,
            "✨ Gesture Launcher — Draw Gesture on Screen (ESC to Cancel)",
        )

        w, h = self.width(), self.height()

        # Render vibrant cyan/gold glowing gesture path
        glow_pen = QPen(QColor(137, 180, 250, 110), 16, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        main_pen = QPen(QColor("#89b4fa"), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

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

            # Start point green indicator dot
            start = stroke.points[0]
            painter.setBrush(QColor("#a6e3a1"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(start.x * w, start.y * h), 6, 6)
