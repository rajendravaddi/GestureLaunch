from PySide6.QtCore import QPropertyAnimation, QRectF, QSize, Qt, Signal, Property
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtWidgets import QAbstractButton


class ToggleSwitch(QAbstractButton):
    """Custom LibAdwaita style toggle switch widget."""

    toggledSignal = Signal(bool)

    def __init__(self, checked: bool = False, parent=None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(48, 26)

        self._handle_position = 1.0 if checked else 0.0
        self.setChecked(checked)

        self._anim = QPropertyAnimation(self, b"handle_position", self)
        self._anim.setDuration(160)

        self.clicked.connect(self._on_clicked)

    def _get_handle_position(self) -> float:
        return self._handle_position

    def _set_handle_position(self, pos: float) -> None:
        self._handle_position = pos
        self.update()

    handle_position = Property(float, _get_handle_position, _set_handle_position)

    def setChecked(self, checked: bool) -> None:
        super().setChecked(checked)
        self._handle_position = 1.0 if checked else 0.0
        self.update()

    def _on_clicked(self) -> None:
        checked = self.isChecked()
        self._anim.stop()
        self._anim.setStartValue(self._handle_position)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()
        self.toggledSignal.emit(checked)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        radius = h / 2.0

        # Background color
        bg_color = QColor("#89b4fa") if self.isChecked() else QColor("#363a4f")
        if not self.isEnabled():
            bg_color = bg_color.darker(150)

        # Draw track
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, radius, radius)
        painter.fillPath(path, bg_color)

        # Handle color and rect
        handle_color = QColor("#11111b") if self.isChecked() else QColor("#cdd6f4")
        handle_size = h - 6
        x_start = 3.0
        x_end = w - handle_size - 3.0
        x_pos = x_start + (x_end - x_start) * self._handle_position

        handle_rect = QRectF(x_pos, 3.0, handle_size, handle_size)
        painter.setBrush(handle_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(handle_rect)

        painter.end()

    def sizeHint(self) -> QSize:
        return QSize(48, 26)
