import configparser
import os
from pathlib import Path
from typing import List

from app.models.application import Application


def scan_desktop_applications() -> List[Application]:
    """Scans system and user desktop entries to find installed GUI applications."""
    directories = [
        Path("/usr/share/applications"),
        Path(os.path.expanduser("~/.local/share/applications")),
        Path("/var/lib/snapd/desktop/applications")
    ]

    apps: List[Application] = []
    seen_ids = set()

    for directory in directories:
        if not directory.exists():
            continue

        for filepath in directory.glob("*.desktop"):
            try:
                config = configparser.ConfigParser(interpolation=None)
                # Parse .desktop file
                config.read(filepath, encoding="utf-8")

                if "Desktop Entry" not in config:
                    continue

                entry = config["Desktop Entry"]

                # Skip non-application entries or hidden entries
                if entry.get("Type") != "Application":
                    continue
                if entry.getboolean("NoDisplay", fallback=False):
                    continue
                if entry.getboolean("Hidden", fallback=False):
                    continue

                app_id = filepath.stem
                if app_id in seen_ids:
                    continue

                name = entry.get("Name", app_id)
                exec_cmd = entry.get("Exec", "")
                icon = entry.get("Icon", "application-x-executable")
                comment = entry.get("Comment", "")

                # Clean up Exec command field codes like %f, %u
                clean_exec = " ".join(
                    [arg for arg in exec_cmd.split() if not arg.startswith("%")]
                )

                app = Application(
                    id=app_id,
                    name=name,
                    exec_command=clean_exec,
                    icon_name=icon,
                    description=comment,
                    desktop_file_path=str(filepath),
                )
                apps.append(app)
                seen_ids.add(app_id)

            except Exception:
                continue

    # Sort applications alphabetically by name
    apps.sort(key=lambda a: a.name.lower())
    return apps
