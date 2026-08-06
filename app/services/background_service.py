import os
import signal
import subprocess
from pathlib import Path

from app.repository.settings_repository import SettingsRepository

PID_FILE = Path.home() / ".config" / "gesture-launcher" / "daemon.pid"


class BackgroundService:
    """Daemon controller service for background gesture recognition state."""

    def __init__(self, settings_repo: SettingsRepository) -> None:
        self.settings_repo = settings_repo

    def is_enabled(self) -> bool:
        return self.settings_repo.get_settings().gesture_service_enabled

    def is_running(self) -> bool:
        """Checks if the background daemon process is currently running."""
        if not PID_FILE.exists():
            return False

        try:
            with open(PID_FILE, "r", encoding="utf-8") as f:
                pid = int(f.read().strip())
            # Signal 0 checks process existence without killing it
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            PID_FILE.unlink(missing_ok=True)
            return False

    def set_enabled(self, enabled: bool) -> None:
        settings = self.settings_repo.get_settings()
        settings.gesture_service_enabled = enabled
        self.settings_repo.save_settings(settings)

        if enabled:
            self.start_daemon()
        else:
            self.stop_daemon()

    def start_daemon(self) -> bool:
        """Launches standalone daemon.py background process detached."""
        self.stop_daemon()  # Clean up any existing instances first

        daemon_script = Path(__file__).parent.parent.parent / "daemon.py"
        project_dir = daemon_script.parent

        try:
            cmd = f"PYTHONPATH={project_dir} uv run python {daemon_script}"
            subprocess.Popen(
                cmd,
                shell=True,
                cwd=project_dir,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception as e:
            print(f"[Daemon Control Error] Failed to start daemon: {e}")
            return False

    def stop_daemon(self) -> bool:
        """Stops running daemon.py process instances cleanly."""
        if PID_FILE.exists():
            try:
                with open(PID_FILE, "r", encoding="utf-8") as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
                PID_FILE.unlink(missing_ok=True)
                return True
            except Exception:
                PID_FILE.unlink(missing_ok=True)

        try:
            subprocess.run(
                ["pkill", "-f", "daemon.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False
