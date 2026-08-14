import sys

from PySide6.QtWidgets import QApplication

from app.repository.gesture_repository import GestureRepository
from app.services.application_service import ApplicationService
from app.utils.gesture_matcher import DollarOneRecognizer
from app.utils.launcher import launch_application
from app.utils.notifier import notify_gesture_matched, notify_gesture_unmatched
from app.widgets.overlay_window import GestureOverlayWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    gesture_repo = GestureRepository()
    app_service = ApplicationService(gesture_repo)

    overlay = GestureOverlayWindow()

    def on_gesture_captured(candidate_strokes: list) -> None:
        app_service.refresh_applications()
        templates = []
        for a in app_service.get_all_applications():
            if a.has_gesture:
                g = gesture_repo.get_by_app_id(a.id)
                if g and not g.is_empty():
                    templates.append(g)

        if not templates:
            print("[GestureLaunch] No saved application gestures found.")
            notify_gesture_unmatched()
            app.quit()
            return

        matched_gesture, score = DollarOneRecognizer.recognize(candidate_strokes, templates)

        if matched_gesture:
            matched_app = app_service.get_application_by_id(matched_gesture.app_id)
            app_name = matched_app.name if matched_app else matched_gesture.name
            exec_cmd = matched_app.exec_command if matched_app else ""

            print(f"[GestureLaunch Match] {app_name} (Score: {score:.2f}) -> Command: '{exec_cmd}'")
            notify_gesture_matched(app_name, score)

            if exec_cmd:
                launch_application(exec_cmd)
        else:
            print(f"[GestureLaunch Match Failed] Best score was: {score:.2f}")
            notify_gesture_unmatched()

        app.quit()

    overlay.gestureCaptured.connect(on_gesture_captured)
    overlay.activate_overlay()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

