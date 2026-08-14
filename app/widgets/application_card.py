from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.models.application import Application


class ApplicationCard(QFrame):
    """Card widget representing an installed application."""

    clicked = Signal(str)  # Emits app.id when clicked

    def __init__(self, app: Application, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.app = app

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.icon_label = QLabel()
        self.name_label = QLabel()
        self.desc_label = QLabel()
        self.badge_label = QLabel()

    def _configure_widgets(self) -> None:
        self.setObjectName("CardFrame")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(90)

        self.icon_label.setFixedSize(48, 48)
        self.icon_label.setScaledContents(True)

        self.name_label.setObjectName("SectionTitle")

        self.desc_label.setObjectName("Subtitle")
        self.desc_label.setWordWrap(True)
        self.desc_label.setMaximumHeight(36)

    def _create_layouts(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.desc_label)

        main_layout.addWidget(self.icon_label)
        main_layout.addLayout(text_layout, 1)
        main_layout.addWidget(self.badge_label, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

    def _create_connections(self) -> None:
        pass

    def _load_data(self) -> None:
        self.name_label.setText(self.app.name)
        self.desc_label.setText(self.app.description if self.app.description else self.app.exec_command)

        # Set icon from theme or fallback
        icon = QIcon.fromTheme(self.app.icon_name)
        if not icon.isNull():
            pixmap = icon.pixmap(48, 48)
            self.icon_label.setPixmap(pixmap)
        else:
            fallback = QIcon.fromTheme("application-x-executable")
            self.icon_label.setPixmap(fallback.pixmap(48, 48))

        # Gesture Status Badge
        if self.app.has_gesture:
            self.badge_label.setText("✓ Gesture Configured")
            self.badge_label.setObjectName("BadgeConfigured")
        else:
            self.badge_label.setText("No Gesture")
            self.badge_label.setObjectName("BadgeEmpty")

        self.badge_label.setStyle(self.badge_label.style())

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.app.id)
        super().mousePressEvent(event)
