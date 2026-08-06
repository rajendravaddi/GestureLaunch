from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.background_service import BackgroundService
from app.services.shortcut_service import ShortcutService
from app.widgets.shortcut_selector import ShortcutSelector


class SettingsPage(QWidget):
    """Page 1: Settings Page for configuring global activation shortcut & service state."""

    def __init__(
        self,
        shortcut_service: ShortcutService = None,
        background_service: BackgroundService = None,
        nav_controller=None,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.shortcut_service = shortcut_service
        self.background_service = background_service
        self.nav_controller = nav_controller

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.title_label = QLabel()
        self.subtitle_label = QLabel()

        # Shortcut Group Card
        self.shortcut_card = QFrame()
        self.shortcut_card_title = QLabel()
        self.shortcut_card_desc = QLabel()
        self.shortcut_selector = ShortcutSelector()

        # Service Group Card
        self.service_card = QFrame()
        self.service_card_title = QLabel()
        self.service_card_desc = QLabel()
        self.service_toggle = QCheckBox()
        self.status_badge = QLabel()

        # Navigation Action Button
        self.continue_button = QPushButton()

    def _configure_widgets(self) -> None:
        self.title_label.setText("Settings")
        self.title_label.setObjectName("HeaderTitle")

        self.subtitle_label.setText("Configure global activation key and gesture background service")
        self.subtitle_label.setObjectName("Subtitle")

        # Cards setup
        self.shortcut_card.setObjectName("CardFrame")
        self.shortcut_card_title.setText("Global Activation Shortcut")
        self.shortcut_card_title.setObjectName("SectionTitle")
        self.shortcut_card_desc.setText("Press this shortcut anywhere on your desktop to activate gesture recognition overlay.")
        self.shortcut_card_desc.setObjectName("Subtitle")

        self.service_card.setObjectName("CardFrame")
        self.service_card_title.setText("Gesture Recognition Daemon")
        self.service_card_title.setObjectName("SectionTitle")
        self.service_card_desc.setText("Enable or disable background touchpad gesture monitoring.")
        self.service_card_desc.setObjectName("Subtitle")

        self.service_toggle.setText("Enable Gesture Service")
        self.service_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        self.continue_button.setText("Continue to Applications →")
        self.continue_button.setObjectName("PrimaryButton")
        self.continue_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def _create_layouts(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(24)

        # Header
        header_box = QVBoxLayout()
        header_box.setSpacing(4)
        header_box.addWidget(self.title_label)
        header_box.addWidget(self.subtitle_label)

        # Shortcut Card Layout
        shortcut_layout = QVBoxLayout(self.shortcut_card)
        shortcut_layout.setSpacing(12)
        shortcut_layout.addWidget(self.shortcut_card_title)
        shortcut_layout.addWidget(self.shortcut_card_desc)
        shortcut_layout.addWidget(self.shortcut_selector)

        # Service Card Layout
        service_layout = QVBoxLayout(self.service_card)
        service_layout.setSpacing(12)
        service_layout.addWidget(self.service_card_title)
        service_layout.addWidget(self.service_card_desc)

        toggle_box = QHBoxLayout()
        toggle_box.addWidget(self.service_toggle)
        toggle_box.addStretch()
        toggle_box.addWidget(self.status_badge)
        service_layout.addLayout(toggle_box)

        # Action layout
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        action_layout.addWidget(self.continue_button)

        main_layout.addLayout(header_box)
        main_layout.addWidget(self.shortcut_card)
        main_layout.addWidget(self.service_card)
        main_layout.addLayout(action_layout)
        main_layout.addStretch()

    def _create_connections(self) -> None:
        self.shortcut_selector.shortcutChanged.connect(self._on_shortcut_changed)
        self.service_toggle.toggled.connect(self._on_service_toggled)
        self.continue_button.clicked.connect(self._on_continue_clicked)

    def _load_data(self) -> None:
        if self.shortcut_service:
            current_sc = self.shortcut_service.get_current_shortcut()
            self.shortcut_selector.set_shortcut(current_sc)

        if self.background_service:
            enabled = self.background_service.is_enabled()
            self.service_toggle.setChecked(enabled)
            self._update_status_badge(self.background_service.is_running())

    def _update_status_badge(self, is_running: bool) -> None:
        if is_running:
            self.status_badge.setText("🟢 Background Service Running")
            self.status_badge.setObjectName("BadgeConfigured")
        else:
            self.status_badge.setText("🔴 Service Stopped")
            self.status_badge.setObjectName("BadgeEmpty")
        self.status_badge.setStyle(self.status_badge.style())

    def _on_shortcut_changed(self, new_shortcut: str) -> None:
        if self.shortcut_service:
            self.shortcut_service.update_shortcut(new_shortcut)

    def _on_service_toggled(self, enabled: bool) -> None:
        if self.background_service:
            self.background_service.set_enabled(enabled)
            self._update_status_badge(enabled)

    def _on_continue_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_applications()