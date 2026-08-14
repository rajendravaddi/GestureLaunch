from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.navigation import NavigationController
from app.pages.application_page import ApplicationPage
from app.pages.applications_page import ApplicationsPage
from app.pages.help_page import HelpPage
from app.pages.settings_page import SettingsPage
from app.repository.gesture_repository import GestureRepository
from app.repository.settings_repository import SettingsRepository
from app.services.application_service import ApplicationService
from app.services.gesture_service import GestureService


class MainWindow(QMainWindow):
    """Main application window hosting QStackedWidget pages and central services."""

    def __init__(self) -> None:
        super().__init__()

        self._initialize_services()
        self._initialize_window()
        self._load_stylesheet()
        self._create_widgets()
        self._create_pages()
        self._setup_navigation()

    def _initialize_services(self) -> None:
        self.gesture_repo = GestureRepository()
        self.settings_repo = SettingsRepository()

        self.application_service = ApplicationService(self.gesture_repo)
        self.gesture_service = GestureService(self.gesture_repo)

    def _initialize_window(self) -> None:
        self.setWindowTitle("Gesture Launcher")
        self.resize(1100, 750)
        self.setMinimumSize(900, 600)

    def _load_stylesheet(self) -> None:
        style_path = Path(__file__).parent / "resources" / "styles" / "main.qss"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def _create_widgets(self) -> None:
        self.page_stack = QStackedWidget()
        self.setCentralWidget(self.page_stack)

    def _create_pages(self) -> None:
        self.nav_controller = NavigationController(self)

        self.settings_page = SettingsPage(
            nav_controller=self.nav_controller,
        )

        self.applications_page = ApplicationsPage(
            application_service=self.application_service,
            nav_controller=self.nav_controller,
        )

        self.application_page = ApplicationPage(
            application_service=self.application_service,
            gesture_service=self.gesture_service,
            nav_controller=self.nav_controller,
        )

        self.help_page = HelpPage(
            nav_controller=self.nav_controller,
        )

        # Add to stack in index order (0=Applications, 1=ApplicationDetails, 2=Settings, 3=Help)
        self.page_stack.addWidget(self.applications_page)
        self.page_stack.addWidget(self.application_page)
        self.page_stack.addWidget(self.settings_page)
        self.page_stack.addWidget(self.help_page)

    def _setup_navigation(self) -> None:
        # Default start page is Applications page
        self.nav_controller.go_to_applications()