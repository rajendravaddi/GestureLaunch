import json
from pathlib import Path
from typing import Optional

from app.models.settings import Settings


class SettingsRepository:
    """JSON persistent storage repository for user settings."""

    def __init__(self, data_path: Optional[Path] = None) -> None:
        if data_path is None:
            data_path = Path.home() / ".config" / "gesture-launcher" / "settings.json"
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self._settings = Settings()
        self._load()

    def _load(self) -> None:
        if not self.data_path.exists():
            return
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._settings = Settings(
                    activation_shortcut=data.get("activation_shortcut", "Super+Shift+G"),
                    gesture_service_enabled=data.get("gesture_service_enabled", True),
                    autostart_on_login=data.get("autostart_on_login", False),
                    launch_minimized=data.get("launch_minimized", False),
                    dark_theme=data.get("dark_theme", True),
                )
        except Exception:
            self._settings = Settings()

    def get_settings(self) -> Settings:
        return self._settings

    def save_settings(self, settings: Settings) -> None:
        self._settings = settings
        data = {
            "activation_shortcut": settings.activation_shortcut,
            "gesture_service_enabled": settings.gesture_service_enabled,
            "autostart_on_login": settings.autostart_on_login,
            "launch_minimized": settings.launch_minimized,
            "dark_theme": settings.dark_theme,
        }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
