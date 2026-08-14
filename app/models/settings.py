from dataclasses import dataclass


@dataclass
class Settings:
    """Model for global application settings."""

    activation_shortcut: str = "Ctrl+Shift+G"
