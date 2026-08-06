import math
from typing import List, Optional, Tuple

from app.models.gesture import Gesture, Point, Stroke


class DollarOneRecognizer:
    """$1 Unistroke Gesture Recognition Engine.

    Recognizes gestures based strictly on shape and stroke direction,
    independent of speed, timing, or absolute scale.
    """

    NUM_POINTS = 64
    SQUARE_SIZE = 100.0
    MATCH_THRESHOLD = 0.68  # Minimum similarity score (0.0 to 1.0) to declare a match

    @classmethod
    def recognize(cls, candidate_strokes: List[Stroke], templates: List[Gesture]) -> Tuple[Optional[Gesture], float]:
        """Matches candidate strokes against list of stored gesture templates.

        Returns (best_matching_gesture, confidence_score) or (None, 0.0).
        """
        candidate_points = cls._flatten_strokes(candidate_strokes)
        if len(candidate_points) < 5:
            return None, 0.0

        normalized_candidate = cls._normalize_path(candidate_points)

        best_match: Optional[Gesture] = None
        best_score = -1.0

        for template in templates:
            if template.is_empty():
                continue

            template_points = cls._flatten_strokes(template.strokes)
            if len(template_points) < 5:
                continue

            normalized_template = cls._normalize_path(template_points)
            dist = cls._path_distance(normalized_candidate, normalized_template)

            # Score ranges from 0.0 to 1.0 (1.0 = exact match)
            half_diag = math.sqrt(2.0) * cls.SQUARE_SIZE / 2.0
            score = max(0.0, 1.0 - (dist / half_diag))

            if score > best_score:
                best_score = score
                best_match = template

        if best_score >= cls.MATCH_THRESHOLD:
            return best_match, best_score

        return None, best_score

    @classmethod
    def _flatten_strokes(cls, strokes: List[Stroke]) -> List[Tuple[float, float]]:
        pts = []
        for stroke in strokes:
            for p in stroke.points:
                pts.append((p.x, p.y))
        return pts

    @classmethod
    def _normalize_path(cls, points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Applies $1 Unistroke geometric transformations: Resample -> Scale -> Translate."""
        pts = cls._resample(points, cls.NUM_POINTS)
        pts = cls._scale_to_square(pts, cls.SQUARE_SIZE)
        pts = cls._translate_to_origin(pts)
        return pts

    @classmethod
    def _resample(cls, points: List[Tuple[float, float]], n: int) -> List[Tuple[float, float]]:
        """Resamples points so that they are spaced equidistant along total path length."""
        path_len = cls._path_length(points)
        if path_len == 0.0:
            return [points[0]] * n

        interval = path_len / (n - 1)
        resampled = [points[0]]
        accumulated_dist = 0.0

        i = 1
        curr_pts = list(points)
        while i < len(curr_pts):
            prev_pt = curr_pts[i - 1]
            curr_pt = curr_pts[i]
            d = cls._euclidean_distance(prev_pt, curr_pt)

            if accumulated_dist + d >= interval:
                # Interpolate point
                t = (interval - accumulated_dist) / d if d > 0 else 0.0
                nx = prev_pt[0] + t * (curr_pt[0] - prev_pt[0])
                ny = prev_pt[1] + t * (curr_pt[1] - prev_pt[1])
                new_pt = (nx, ny)
                resampled.append(new_pt)

                # Insert interpolated point into list to continue
                curr_pts.insert(i, new_pt)
                accumulated_dist = 0.0
            else:
                accumulated_dist += d
            i += 1

        # Fallback to pad if rounding error left fewer than n points
        while len(resampled) < n:
            resampled.append(points[-1])

        return resampled[:n]

    @classmethod
    def _scale_to_square(cls, points: List[Tuple[float, float]], size: float) -> List[Tuple[float, float]]:
        """Scales bounding box to size x size preserving stroke shape."""
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)

        width = max_x - min_x
        height = max_y - min_y

        if width == 0:
            width = 0.001
        if height == 0:
            height = 0.001

        scaled = []
        for x, y in points:
            scaled_x = ((x - min_x) / width) * size
            scaled_y = ((y - min_y) / height) * size
            scaled.append((scaled_x, scaled_y))
        return scaled

    @classmethod
    def _translate_to_origin(cls, points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Translates centroid of points to (0, 0)."""
        centroid_x = sum(p[0] for p in points) / len(points)
        centroid_y = sum(p[1] for p in points) / len(points)

        return [(x - centroid_x, y - centroid_y) for x, y in points]

    @classmethod
    def _path_distance(cls, pts1: List[Tuple[float, float]], pts2: List[Tuple[float, float]]) -> float:
        """Calculates mean point-to-point Euclidean distance."""
        total_dist = 0.0
        n = min(len(pts1), len(pts2))
        if n == 0:
            return 99999.0

        for i in range(n):
            total_dist += cls._euclidean_distance(pts1[i], pts2[i])

        return total_dist / n

    @classmethod
    def _path_length(cls, points: List[Tuple[float, float]]) -> float:
        d = 0.0
        for i in range(1, len(points)):
            d += cls._euclidean_distance(points[i - 1], points[i])
        return d

    @classmethod
    def _euclidean_distance(cls, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
