from typing import List, Optional

from app.models.application import Application
from app.repository.gesture_repository import GestureRepository
from app.utils.desktop_parser import scan_desktop_applications


class ApplicationService:
    """Service providing access to desktop applications, filtering, and gesture status."""

    def __init__(self, gesture_repo: GestureRepository) -> None:
        self.gesture_repo = gesture_repo
        self._applications: List[Application] = []
        self.refresh_applications()

    def refresh_applications(self) -> List[Application]:
        """Scans installed applications and correlates with existing gesture templates."""
        self._applications = scan_desktop_applications()
        for app in self._applications:
            gesture = self.gesture_repo.get_by_app_id(app.id)
            if gesture and not gesture.is_empty():
                app.has_gesture = True
                app.gesture_id = gesture.id
            else:
                app.has_gesture = False
                app.gesture_id = None
        return self._applications

    def get_all_applications(self) -> List[Application]:
        return self._applications

    def get_application_by_id(self, app_id: str) -> Optional[Application]:
        for app in self._applications:
            if app.id == app_id:
                return app
        return None

    def filter_applications(
        self, query: str = "", gesture_filter: str = "All"
    ) -> List[Application]:
        """Filters applications based on search query and gesture status."""
        filtered = self._applications

        # Filter by gesture status
        if gesture_filter == "Gesture Created":
            filtered = [app for app in filtered if app.has_gesture]
        elif gesture_filter == "Gesture Not Created":
            filtered = [app for app in filtered if not app.has_gesture]

        # Filter by search query
        if query.strip():
            q = query.strip().lower()
            filtered = [
                app
                for app in filtered
                if q in app.name.lower() or q in app.description.lower()
            ]

        return filtered
