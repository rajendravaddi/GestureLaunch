from app.models.settings import Settings


class SettingsRepository:
    """Repository providing global application settings."""

    def __init__(self) -> None:
        self._settings = Settings()

    def get_settings(self) -> Settings:
        return self._settings
