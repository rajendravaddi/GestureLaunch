from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.utils.gnome_shortcut_manager import (
    install_gnome_shortcut,
    is_gnome_shortcut_installed,
    remove_gnome_shortcut,
)
from app.widgets.toggle_switch import ToggleSwitch


class SettingsPage(QWidget):
    """Page 1: Settings Page for displaying activation shortcut & managing GNOME custom keybinding integration."""

    def __init__(
        self,
        nav_controller=None,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
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
        self.shortcut_badge = QLabel()

        # Service Group Card
        self.service_card = QFrame()
        self.service_card_title = QLabel()
        self.service_card_desc = QLabel()
        self.service_toggle = ToggleSwitch()

        # Navigation Action Button
        self.continue_button = QPushButton()

    def _configure_widgets(self) -> None:
        self.title_label.setText("Settings")
        self.title_label.setObjectName("HeaderTitle")

        self.subtitle_label.setText("Configure global activation key and gesture launch service")
        self.subtitle_label.setObjectName("Subtitle")

        # Cards setup
        self.shortcut_card.setObjectName("CardFrame")
        self.shortcut_card_title.setText("Global Activation Shortcut")
        self.shortcut_card_title.setObjectName("SectionTitle")
        self.shortcut_card_desc.setText("Press this shortcut anywhere on your desktop to open the gesture recognition overlay.")
        self.shortcut_card_desc.setObjectName("Subtitle")

        self.shortcut_badge.setText("Ctrl + Shift + G")
        self.shortcut_badge.setStyleSheet(
            "background-color: #313244; color: #89b4fa; font-weight: bold; "
            "font-size: 15px; padding: 8px 16px; border-radius: 8px; border: 1px solid #45475a;"
        )

        self.service_card.setObjectName("CardFrame")
        self.service_card_title.setText("Gesture Launch service")
        self.service_card_title.setObjectName("SectionTitle")
        self.service_card_desc.setText("Enable or disable system-wide custom keyboard shortcut integration.")
        self.service_card_desc.setObjectName("Subtitle")

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

        badge_box = QHBoxLayout()
        badge_box.setContentsMargins(0, 4, 0, 4)
        badge_box.addWidget(self.shortcut_badge, 0, Qt.AlignmentFlag.AlignLeft)
        badge_box.addStretch()
        shortcut_layout.addLayout(badge_box)

        # Service Card Layout
        service_layout = QHBoxLayout(self.service_card)
        service_layout.setContentsMargins(16, 16, 16, 16)
        service_layout.setSpacing(16)

        service_info_box = QVBoxLayout()
        service_info_box.setSpacing(4)
        service_info_box.addWidget(self.service_card_title)
        service_info_box.addWidget(self.service_card_desc)

        service_layout.addLayout(service_info_box, 1)
        service_layout.addWidget(self.service_toggle, 0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

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
        self.service_toggle.toggledSignal.connect(self._on_service_toggled)
        self.continue_button.clicked.connect(self._on_continue_clicked)

    def _load_data(self) -> None:
        # Load current GNOME custom keybinding status
        installed = is_gnome_shortcut_installed()
        self.service_toggle.setChecked(installed)

    def _on_service_toggled(self, enabled: bool) -> None:
        if enabled:
            install_gnome_shortcut()
        else:
            remove_gnome_shortcut()

    def _on_continue_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_applications()