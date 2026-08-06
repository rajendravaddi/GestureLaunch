from app.models.settings import Settings
from app.repository.settings_repository import SettingsRepository


class ShortcutService:
    """Service managing global activation keyboard shortcut configuration."""

    def __init__(self, settings_repo: SettingsRepository) -> None:
        self.settings_repo = settings_repo

    def get_current_shortcut(self) -> str:
        return self.settings_repo.get_settings().activation_shortcut

    def update_shortcut(self, new_shortcut: str) -> bool:
        settings = self.settings_repo.get_settings()
        settings.activation_shortcut = new_shortcut
        self.settings_repo.save_settings(settings)
        return True
