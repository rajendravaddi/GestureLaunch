import argparse
import os
import signal
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from app.services.daemon_service import DaemonService

PID_FILE = Path.home() / ".config" / "gesture-launcher" / "daemon.pid"


def write_pid() -> None:
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))


def remove_pid() -> None:
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
        except Exception:
            pass


def stop_running_daemon() -> bool:
    if not PID_FILE.exists():
        return False

    try:
        with open(PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        remove_pid()
        print(f"[Daemon] Terminated daemon process (PID: {pid})")
        return True
    except Exception as e:
        print(f"[Daemon] No active daemon running (or couldn't kill PID): {e}")
        remove_pid()
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Gesture Launcher Background Daemon")
    parser.add_argument("--stop", "-k", action="store_true", help="Stop running background daemon")
    args = parser.parse_args()

    if args.stop:
        stop_running_daemon()
        sys.exit(0)

    # Stop any existing daemon instance before starting a new one
    stop_running_daemon()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    write_pid()
    daemon = DaemonService()
    daemon.start()

    # Enable SIGINT (Ctrl+C) handling inside Qt Event Loop
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)  # Allows Python interpreter to process signals

    def handle_sigint(signum, frame):
        print("\n[Daemon] Shutdown signal received. Stopping daemon...")
        daemon.stop()
        remove_pid()
        app.quit()

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    try:
        sys.exit(app.exec())
    finally:
        remove_pid()


if __name__ == "__main__":
    main()
