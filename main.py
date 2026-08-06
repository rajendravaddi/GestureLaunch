import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.repository.settings_repository import SettingsRepository
from app.services.background_service import BackgroundService


def main() -> None:
    application = QApplication(sys.argv)

    # Ensure background daemon is running if enabled
    settings_repo = SettingsRepository()
    bg_service = BackgroundService(settings_repo)
    if bg_service.is_enabled():
        bg_service.start_daemon()

    main_window = MainWindow()
    main_window.show()

    application.exec()


if __name__ == "__main__":
    main()