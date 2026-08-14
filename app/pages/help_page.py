from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class HelpPage(QWidget):
    """Page 4: Help & Guide Page providing step-by-step setup and gesture guide."""

    def __init__(self, nav_controller=None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.nav_controller = nav_controller

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self) -> None:
        self.title_label = QLabel()
        self.back_button = QPushButton()

        self.scroll_area = QScrollArea()
        self.content_widget = QWidget()

        # Section 1: Overview
        self.card_overview = QFrame()
        self.title_overview = QLabel()
        self.body_overview = QLabel()

        # Section 2: Step-by-Step Setup
        self.card_steps = QFrame()
        self.title_steps = QLabel()
        self.body_steps = QLabel()

        # Section 3: Gesture Tips
        self.card_tips = QFrame()
        self.title_tips = QLabel()
        self.body_tips = QLabel()

        # Section 4: Troubleshooting
        self.card_faq = QFrame()
        self.title_faq = QLabel()
        self.body_faq = QLabel()

    def _configure_widgets(self) -> None:
        self.title_label.setText("Help & User Guide")
        self.title_label.setObjectName("HeaderTitle")

        self.back_button.setText("← Back to Applications")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("AppScrollArea")
        self.content_widget.setStyleSheet("background: transparent;")

        # Section Cards
        for card in (self.card_overview, self.card_steps, self.card_tips, self.card_faq):
            card.setObjectName("CardFrame")

        self.title_overview.setText("What is Gesture Launcher?")
        self.title_overview.setObjectName("SectionTitle")
        self.body_overview.setText(
            "Gesture Launcher allows Ubuntu / Linux desktop users to instantly launch installed applications "
            "using touchpad or mouse gesture strokes triggered via a global shortcut."
        )
        self.body_overview.setWordWrap(True)

        self.title_steps.setText("Step-by-Step Setup Guide")
        self.title_steps.setObjectName("SectionTitle")
        self.body_steps.setText(
            "1. Navigate to Settings and configure your global activation key (Default: Super+Shift+G).\n"
            "2. Ensure the Gesture Recognition Daemon toggle is turned ON.\n"
            "3. Select any application from the Applications grid.\n"
            "4. Draw a distinctive gesture template on the Gesture Studio canvas and hit 'Save Gesture'.\n"
            "5. Activate your shortcut anywhere on the desktop to draw your gesture and launch the app!"
        )
        self.body_steps.setWordWrap(True)

        self.title_tips.setText("Tips for Reliable Gesture Recording")
        self.title_tips.setObjectName("SectionTitle")
        self.body_tips.setText(
            "• Use continuous smooth strokes (e.g. single-letter shapes like 'C' for Chrome, 'F' for Files, 'T' for Terminal).\n"
            "• Avoid tiny dots or extremely subtle wiggles.\n"
            "• You can clear and redraw gestures anytime in the Gesture Studio."
        )
        self.body_tips.setWordWrap(True)

        self.title_faq.setText("Troubleshooting & FAQ")
        self.title_faq.setObjectName("SectionTitle")
        self.body_faq.setText(
            "Q: Why isn't my application showing up?\n"
            "A: Gesture Launcher automatically scans standard system locations (/usr/share/applications). "
            "Custom apps installed elsewhere may need a valid desktop entry file.\n\n"
            "Q: How do I minimize or keep the service running?\n"
            "A: The background daemon runs silently according to your settings toggle."
        )
        self.body_faq.setWordWrap(True)

    def _create_layouts(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setSpacing(16)

        # Overview
        o_layout = QVBoxLayout(self.card_overview)
        o_layout.addWidget(self.title_overview)
        o_layout.addWidget(self.body_overview)

        # Steps
        s_layout = QVBoxLayout(self.card_steps)
        s_layout.addWidget(self.title_steps)
        s_layout.addWidget(self.body_steps)

        # Tips
        t_layout = QVBoxLayout(self.card_tips)
        t_layout.addWidget(self.title_tips)
        t_layout.addWidget(self.body_tips)

        # FAQ
        f_layout = QVBoxLayout(self.card_faq)
        f_layout.addWidget(self.title_faq)
        f_layout.addWidget(self.body_faq)

        content_layout.addWidget(self.card_overview)
        content_layout.addWidget(self.card_steps)
        content_layout.addWidget(self.card_tips)
        content_layout.addWidget(self.card_faq)
        content_layout.addStretch()

        self.scroll_area.setWidget(self.content_widget)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.scroll_area, 1)

    def _create_connections(self) -> None:
        self.back_button.clicked.connect(self._on_back_clicked)

    def _on_back_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_applications()
