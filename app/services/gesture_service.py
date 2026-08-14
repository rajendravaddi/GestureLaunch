import uuid
from typing import Optional

from app.models.gesture import Gesture, Stroke
from app.repository.gesture_repository import GestureRepository


class GestureService:
    """Service handling gesture CRUD operations and verification skeleton."""

    def __init__(self, repository: GestureRepository) -> None:
        self.repository = repository

    def get_gesture_for_app(self, app_id: str) -> Optional[Gesture]:
        return self.repository.get_by_app_id(app_id)

    def get_all_gestures(self) -> list[Gesture]:
        return self.repository.get_all()

    def save_gesture(self, app_id: str, app_name: str, strokes: list[Stroke]) -> Gesture:
        existing = self.repository.get_by_app_id(app_id)
        if existing:
            existing.strokes = strokes
            existing.updated_at = existing.updated_at
            self.repository.save(existing)
            return existing

        gesture_id = str(uuid.uuid4())
        gesture = Gesture(
            id=gesture_id,
            app_id=app_id,
            name=app_name,
            strokes=strokes,
        )
        self.repository.save(gesture)
        return gesture

    def delete_gesture_for_app(self, app_id: str) -> bool:
        gesture = self.repository.get_by_app_id(app_id)
        if gesture:
            return self.repository.delete(gesture.id)
        return False
