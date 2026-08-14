import time
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Point:
    """Represents a 2D normalized coordinate point (x, y)."""

    x: float
    y: float


@dataclass
class Stroke:
    """Represents a continuous stroke of points."""

    points: List[Point] = field(default_factory=list)


@dataclass
class Gesture:
    """Model representing a touchpad/mouse gesture template."""

    id: str
    app_id: str
    name: str
    strokes: List[Stroke] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def is_empty(self) -> bool:
        return not any(len(stroke.points) > 0 for stroke in self.strokes)
