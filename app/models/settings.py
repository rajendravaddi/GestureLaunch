from dataclasses import dataclass


@dataclass
class Settings:
    """Model for global application settings."""

    activation_shortcut: str = "Super+Shift+G"
    gesture_service_enabled: bool = False
    autostart_on_login: bool = False
    launch_minimized: bool = False
    dark_theme: bool = True
