from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models.application import Application
from app.services.application_service import ApplicationService
from app.services.gesture_service import GestureService
from app.widgets.gesture_canvas import GestureCanvas


class ApplicationPage(QWidget):
    """Page 3: Application Details & Gesture Studio page."""

    def __init__(
        self,
        application_service: ApplicationService = None,
        gesture_service: GestureService = None,
        nav_controller=None,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.application_service = application_service
        self.gesture_service = gesture_service
        self.nav_controller = nav_controller
        self.current_app: Optional[Application] = None

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.back_button = QPushButton()

        # Header Info Card
        self.header_card = QFrame()
        self.app_icon_label = QLabel()
        self.app_name_label = QLabel()
        self.app_exec_label = QLabel()
        self.badge_label = QLabel()

        # Gesture Studio Frame
        self.studio_card = QFrame()
        self.studio_title = QLabel()
        self.canvas = GestureCanvas()

        # Control Action Buttons
        self.preview_button = QPushButton()
        self.clear_button = QPushButton()
        self.save_button = QPushButton()
        self.delete_button = QPushButton()

    def _configure_widgets(self) -> None:
        self.back_button.setText("← Back to Applications")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.header_card.setObjectName("CardFrame")
        self.app_icon_label.setFixedSize(64, 64)
        self.app_icon_label.setScaledContents(True)

        self.app_name_label.setObjectName("HeaderTitle")
        self.app_exec_label.setObjectName("Subtitle")

        self.studio_card.setObjectName("CardFrame")
        self.studio_title.setText("Gesture Studio")
        self.studio_title.setObjectName("SectionTitle")

        self.preview_button.setText("▶ Play Preview")
        self.preview_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.clear_button.setText("🧹 Clear Canvas")
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.save_button.setText("💾 Save Gesture")
        self.save_button.setObjectName("PrimaryButton")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.delete_button.setText("🗑 Delete Gesture")
        self.delete_button.setObjectName("DangerButton")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def _create_layouts(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)

        # Top Bar
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()

        # Header Info Card Layout
        header_layout = QHBoxLayout(self.header_card)
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(16)

        info_box = QVBoxLayout()
        info_box.setSpacing(4)
        info_box.addWidget(self.app_name_label)
        info_box.addWidget(self.app_exec_label)

        header_layout.addWidget(self.app_icon_label)
        header_layout.addLayout(info_box, 1)
        header_layout.addWidget(self.badge_label, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Studio Card Layout
        studio_layout = QVBoxLayout(self.studio_card)
        studio_layout.setContentsMargins(16, 16, 16, 16)
        studio_layout.setSpacing(16)
        studio_layout.addWidget(self.studio_title)
        studio_layout.addWidget(self.canvas, 1)

        # Action Buttons Layout
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        action_layout.addWidget(self.preview_button)
        action_layout.addWidget(self.clear_button)
        action_layout.addStretch()
        action_layout.addWidget(self.delete_button)
        action_layout.addWidget(self.save_button)

        studio_layout.addLayout(action_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.header_card)
        main_layout.addWidget(self.studio_card, 1)

    def _create_connections(self) -> None:
        self.back_button.clicked.connect(self._on_back_clicked)
        self.preview_button.clicked.connect(self.canvas.play_preview)
        self.clear_button.clicked.connect(self.canvas.clear)
        self.save_button.clicked.connect(self._on_save_gesture)
        self.delete_button.clicked.connect(self._on_delete_gesture)

    def _load_data(self) -> None:
        pass

    def load_application(self, app_id: str) -> None:
        if not self.application_service:
            return

        self.current_app = self.application_service.get_application_by_id(app_id)
        if not self.current_app:
            return

        self.app_name_label.setText(self.current_app.name)
        self.app_exec_label.setText(self.current_app.exec_command)

        icon = QIcon.fromTheme(self.current_app.icon_name)
        if not icon.isNull():
            self.app_icon_label.setPixmap(icon.pixmap(64, 64))
        else:
            fallback = QIcon.fromTheme("application-x-executable")
            self.app_icon_label.setPixmap(fallback.pixmap(64, 64))

        # Check existing gesture
        gesture = None
        if self.gesture_service:
            gesture = self.gesture_service.get_gesture_for_app(app_id)

        if gesture and not gesture.is_empty():
            self.badge_label.setText("✓ Gesture Configured")
            self.badge_label.setObjectName("BadgeConfigured")
            self.canvas.set_strokes(gesture.strokes)
            self.delete_button.show()
        else:
            self.badge_label.setText("No Gesture")
            self.badge_label.setObjectName("BadgeEmpty")
            self.canvas.clear()
            self.delete_button.hide()

        self.badge_label.setStyle(self.badge_label.style())

    def _on_save_gesture(self) -> None:
        if not self.current_app or not self.gesture_service:
            return

        if not self.canvas.strokes:
            return

        self.gesture_service.save_gesture(
            app_id=self.current_app.id,
            app_name=self.current_app.name,
            strokes=self.canvas.strokes,
        )
        self.load_application(self.current_app.id)

    def _on_delete_gesture(self) -> None:
        if not self.current_app or not self.gesture_service:
            return

        self.gesture_service.delete_gesture_for_app(self.current_app.id)
        self.load_application(self.current_app.id)

    def _on_back_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_applications()
