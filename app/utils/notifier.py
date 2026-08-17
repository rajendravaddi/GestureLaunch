import shutil
import subprocess


def send_desktop_notification(title: str, message: str, icon_name: str = "gesture-launch") -> bool:
    """Sends a desktop notification using Linux notify-send."""
    notify_send_path = shutil.which("notify-send")
    if not notify_send_path:
        return False

    try:
        cmd = [
            notify_send_path,
            "--app-name=Gesture Launch",
            f"--icon={icon_name}",
            title,
            message,
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def notify_gesture_matched(app_name: str, confidence: float) -> None:
    """Sends success notification when a gesture matches an application."""
    title = f"Launching {app_name}"
    message = f"Matched gesture template (Confidence: {int(confidence * 100)}%)"
    send_desktop_notification(title, message, icon_name="emblem-ok")


def notify_gesture_unmatched() -> None:
    """Sends failure notification when no gesture match is found."""
    title = "No Match Found"
    message = "No application gesture template matched your drawn input."
    send_desktop_notification(title, message, icon_name="dialog-warning")
