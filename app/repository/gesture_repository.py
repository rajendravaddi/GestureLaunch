import json
from pathlib import Path
from typing import Dict, Optional

from app.models.gesture import Gesture, Point, Stroke


class GestureRepository:
    """JSON persistent storage repository for user gestures."""

    def __init__(self, data_path: Optional[Path] = None) -> None:
        if data_path is None:
            data_path = Path.home() / ".config" / "gesture-launcher" / "gestures.json"
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self._gestures: Dict[str, Gesture] = {}
        self._load()

    def _load(self) -> None:
        if not self.data_path.exists():
            return
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for gesture_id, g_dict in data.items():
                    strokes = []
                    for stroke_data in g_dict.get("strokes", []):
                        points = [
                            Point(
                                x=pt["x"],
                                y=pt["y"],
                                timestamp=pt.get("timestamp", 0.0),
                            )
                            for pt in stroke_data.get("points", [])
                        ]
                        strokes.append(Stroke(points=points))

                    gesture = Gesture(
                        id=g_dict["id"],
                        app_id=g_dict["app_id"],
                        name=g_dict.get("name", ""),
                        strokes=strokes,
                        created_at=g_dict.get("created_at", 0.0),
                        updated_at=g_dict.get("updated_at", 0.0),
                    )
                    self._gestures[gesture_id] = gesture
        except Exception:
            self._gestures = {}

    def _save(self) -> None:
        data = {}
        for g_id, gesture in self._gestures.items():
            data[g_id] = {
                "id": gesture.id,
                "app_id": gesture.app_id,
                "name": gesture.name,
                "created_at": gesture.created_at,
                "updated_at": gesture.updated_at,
                "strokes": [
                    {
                        "points": [
                            {"x": pt.x, "y": pt.y, "timestamp": pt.timestamp}
                            for pt in stroke.points
                        ]
                    }
                    for stroke in gesture.strokes
                ],
            }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_by_app_id(self, app_id: str) -> Optional[Gesture]:
        for gesture in self._gestures.values():
            if gesture.app_id == app_id:
                return gesture
        return None

    def get_by_id(self, gesture_id: str) -> Optional[Gesture]:
        return self._gestures.get(gesture_id)

    def get_all(self) -> list[Gesture]:
        return list(self._gestures.values())

    def save(self, gesture: Gesture) -> None:
        self._gestures[gesture.id] = gesture
        self._save()

    def delete(self, gesture_id: str) -> bool:
        if gesture_id in self._gestures:
            del self._gestures[gesture_id]
            self._save()
            return True
        return False
