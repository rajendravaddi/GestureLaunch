import ast
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
DAEMON_SCRIPT = PROJECT_ROOT / "daemon.py"

SHORTCUT_ID = "gesture-launcher"
BASE_SCHEMA = "org.gnome.settings-daemon.plugins.media-keys"

SHORTCUT_PATH = (
    "/org/gnome/settings-daemon/plugins/media-keys/"
    f"custom-keybindings/{SHORTCUT_ID}/"
)

CUSTOM_SCHEMA = (
    "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:"
    f"{SHORTCUT_PATH}"
)


def _get_custom_shortcuts() -> list[str]:
    try:
        result = subprocess.run(
            ["gsettings", "get", BASE_SCHEMA, "custom-keybindings"],
            capture_output=True,
            text=True,
            check=True,
        )
        val = result.stdout.strip()
        if val == "@as []" or not val:
            return []
        return ast.literal_eval(val)
    except Exception:
        return []


def is_gnome_shortcut_installed() -> bool:
    """Checks if the GestureLaunch GNOME custom keybinding is registered."""
    shortcuts = _get_custom_shortcuts()
    return SHORTCUT_PATH in shortcuts


def install_gnome_shortcut() -> bool:
    """Registers GNOME custom keybinding for Ctrl+Shift+G to run daemon.py."""
    try:
        shortcuts = _get_custom_shortcuts()
        if SHORTCUT_PATH not in shortcuts:
            shortcuts.append(SHORTCUT_PATH)
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    BASE_SCHEMA,
                    "custom-keybindings",
                    str(shortcuts),
                ],
                check=True,
            )

        # Set shortcut details
        subprocess.run(
            ["gsettings", "set", CUSTOM_SCHEMA, "name", "Gesture Launcher"],
            check=True,
        )

        command = f"{PYTHON} {DAEMON_SCRIPT}"
        subprocess.run(
            ["gsettings", "set", CUSTOM_SCHEMA, "command", command],
            check=True,
        )

        subprocess.run(
            ["gsettings", "set", CUSTOM_SCHEMA, "binding", "<Control><Shift>g"],
            check=True,
        )
        return True
    except Exception as e:
        print(f"[GnomeShortcutManager Error] Failed to install shortcut: {e}")
        return False


def remove_gnome_shortcut() -> bool:
    """Removes the GestureLaunch GNOME custom keybinding."""
    try:
        shortcuts = _get_custom_shortcuts()
        if SHORTCUT_PATH in shortcuts:
            shortcuts.remove(SHORTCUT_PATH)
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    BASE_SCHEMA,
                    "custom-keybindings",
                    str(shortcuts),
                ],
                check=True,
            )
        return True
    except Exception as e:
        print(f"[GnomeShortcutManager Error] Failed to remove shortcut: {e}")
        return False
