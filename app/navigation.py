from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.main_window import MainWindow


class PageIndex(IntEnum):
    SETTINGS = 0
    APPLICATIONS = 1
    APPLICATION_DETAILS = 2
    HELP = 3


class NavigationController:
    """Manages page navigation across the QStackedWidget."""

    def __init__(self, main_window: "MainWindow") -> None:
        self.main_window = main_window

    def go_to_settings(self) -> None:
        self.main_window.page_stack.setCurrentIndex(PageIndex.SETTINGS)

    def go_to_applications(self) -> None:
        self.main_window.applications_page.refresh_data()
        self.main_window.page_stack.setCurrentIndex(PageIndex.APPLICATIONS)

    def go_to_application_details(self, app_id: str) -> None:
        self.main_window.application_page.load_application(app_id)
        self.main_window.page_stack.setCurrentIndex(PageIndex.APPLICATION_DETAILS)

    def go_to_help(self) -> None:
        self.main_window.page_stack.setCurrentIndex(PageIndex.HELP)
