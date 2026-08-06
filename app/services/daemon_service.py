import sys
from typing import Optional

from pynput import keyboard
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from app.models.settings import Settings
from app.repository.gesture_repository import GestureRepository
from app.repository.settings_repository import SettingsRepository
from app.services.application_service import ApplicationService
from app.utils.gesture_matcher import DollarOneRecognizer
from app.utils.launcher import launch_application
from app.utils.notifier import notify_gesture_matched, notify_gesture_unmatched
from app.widgets.overlay_window import GestureOverlayWindow


class DaemonService(QObject):
    """Background Daemon Service managing shortcut listener and gesture recognition flow."""

    triggerOverlaySignal = Signal()

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self.gesture_repo = GestureRepository()
        self.settings_repo = SettingsRepository()
        self.app_service = ApplicationService(self.gesture_repo)

        self.overlay_window: Optional[GestureOverlayWindow] = None
        self.hotkey_listener: Optional[keyboard.GlobalHotKeys] = None

    def start(self) -> None:
        """Starts background service, creates overlay window, and binds global hotkey."""
        settings = self.settings_repo.get_settings()
        if not settings.gesture_service_enabled:
            print("[Daemon] Gesture recognition service is disabled in settings.")

        self.overlay_window = GestureOverlayWindow()
        self.overlay_window.gestureCaptured.connect(self._on_gesture_captured)
        self.triggerOverlaySignal.connect(self.overlay_window.activate_overlay)

        self._bind_hotkey(settings.activation_shortcut)
        print(f"[Daemon] Service running. Shortcut active: {settings.activation_shortcut}")

    def _bind_hotkey(self, shortcut_str: str) -> None:
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except Exception:
                pass

        pynput_shortcut = self._convert_shortcut_to_pynput(shortcut_str)

        try:
            hotkeys = {pynput_shortcut: self._on_hotkey_triggered}
            self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()
        except Exception as e:
            print(f"[Daemon Error] Failed to bind global hotkey '{shortcut_str}': {e}")
            # Fallback default shortcut
            fallback = "<cmd>+<shift>+g"
            hotkeys = {fallback: self._on_hotkey_triggered}
            self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()

    def _on_hotkey_triggered(self) -> None:
        """Called in background thread when shortcut is pressed. Emits Qt signal to UI thread."""
        self.triggerOverlaySignal.emit()

    def _on_gesture_captured(self, candidate_strokes: list) -> None:
        """Evaluates captured gesture strokes using $1 Unistroke algorithm."""
        # Refresh current gestures
        self.app_service.refresh_applications()

        # Collect all configured gesture templates
        templates = []
        for app in self.app_service.get_all_applications():
            if app.has_gesture:
                g = self.gesture_repo.get_by_app_id(app.id)
                if g and not g.is_empty():
                    templates.append(g)

        if not templates:
            print("[Daemon] No stored application gestures found.")
            notify_gesture_unmatched()
            return

        # Perform shape match
        matched_gesture, score = DollarOneRecognizer.recognize(candidate_strokes, templates)

        if matched_gesture:
            matched_app = self.app_service.get_application_by_id(matched_gesture.app_id)
            app_name = matched_app.name if matched_app else matched_gesture.name
            exec_cmd = matched_app.exec_command if matched_app else ""

            print(f"[Daemon Match Success] {app_name} (Score: {score:.2f}) -> Command: '{exec_cmd}'")
            notify_gesture_matched(app_name, score)

            if exec_cmd:
                launch_application(exec_cmd)
        else:
            print(f"[Daemon Match Failed] Best score was: {score:.2f}")
            notify_gesture_unmatched()

    def _convert_shortcut_to_pynput(self, shortcut: str) -> str:
        """Converts user-friendly shortcut string (e.g. Super+Shift+G) to pynput format."""
        parts = shortcut.split("+")
        converted = []
        for part in parts:
            p = part.strip().lower()
            if p in ("super", "meta", "win", "cmd"):
                converted.append("<cmd>")
            elif p in ("ctrl", "control"):
                converted.append("<ctrl>")
            elif p == "shift":
                converted.append("<shift>")
            elif p in ("alt", "option"):
                converted.append("<alt>")
            else:
                converted.append(p)
        return "+".join(converted)

    def stop(self) -> None:
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except Exception:
                pass
        if self.overlay_window:
            self.overlay_window.close()
