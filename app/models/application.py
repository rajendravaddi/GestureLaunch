from dataclasses import dataclass
from typing import Optional


@dataclass
class Application:
    """Model representing an installed desktop application."""

    id: str
    name: str
    exec_command: str
    icon_name: str = "application-x-executable"
    description: str = ""
    desktop_file_path: str = ""
    has_gesture: bool = False
    gesture_id: Optional[str] = None
