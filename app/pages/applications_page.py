from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.services.application_service import ApplicationService
from app.widgets.application_grid import ApplicationGrid
from app.widgets.application_toolbar import ApplicationToolbar


class ApplicationsPage(QWidget):
    """Page 2: Applications Page displaying grid of desktop applications with search and filters."""

    def __init__(
        self,
        application_service: ApplicationService = None,
        nav_controller=None,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.application_service = application_service
        self.nav_controller = nav_controller

        self._current_query = ""
        self._current_filter = "All"

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.title_label = QLabel()
        self.settings_nav_btn = QPushButton()
        self.help_nav_btn = QPushButton()

        self.toolbar = ApplicationToolbar()
        self.grid = ApplicationGrid()

    def _configure_widgets(self) -> None:
        self.title_label.setText("Applications")
        self.title_label.setObjectName("HeaderTitle")

        self.settings_nav_btn.setText("⚙ Settings")
        self.settings_nav_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.help_nav_btn.setText("❓ Help")
        self.help_nav_btn.setCursor(Qt.CursorShape.PointingHandCursor)

    def _create_layouts(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)

        # Header Bar
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_nav_btn)
        header_layout.addWidget(self.help_nav_btn)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.grid, 1)

    def _create_connections(self) -> None:
        self.toolbar.searchChanged.connect(self._on_search_changed)
        self.toolbar.filterChanged.connect(self._on_filter_changed)
        self.grid.appClicked.connect(self._on_app_clicked)

        self.settings_nav_btn.clicked.connect(self._on_settings_clicked)
        self.help_nav_btn.clicked.connect(self._on_help_clicked)

    def _load_data(self) -> None:
        self.refresh_data()

    def refresh_data(self) -> None:
        if self.application_service:
            self.application_service.refresh_applications()
            self._apply_filter()

    def _on_search_changed(self, query: str) -> None:
        self._current_query = query
        self._apply_filter()

    def _on_filter_changed(self, filter_name: str) -> None:
        self._current_filter = filter_name
        self._apply_filter()

    def _apply_filter(self) -> None:
        if self.application_service:
            filtered_apps = self.application_service.filter_applications(
                query=self._current_query, gesture_filter=self._current_filter
            )
            self.grid.populate(filtered_apps)

    def _on_app_clicked(self, app_id: str) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_application_details(app_id)

    def _on_settings_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_settings()

    def _on_help_clicked(self) -> None:
        if self.nav_controller:
            self.nav_controller.go_to_help()
