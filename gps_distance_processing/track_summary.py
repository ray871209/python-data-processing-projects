"""Independent GPS track-distance summary built on the existing Haversine function."""
import csv
from pathlib import Path
from gps_distance_processing.main import haversine_km

def summarize_track(path: str | Path) -> dict:
    with open(path, encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"latitude", "longitude"}.issubset(reader.fieldnames):
            raise ValueError("CSV requires latitude and longitude columns")
        points = []
        for line_no, row in enumerate(reader, start=2):
            try:
                lat, lon = float(row["latitude"]), float(row["longitude"])
                haversine_km(lat, lon, lat, lon)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Invalid coordinates at line {line_no}") from exc
            points.append((lat, lon))
    segments = [haversine_km(*a, *b) for a, b in zip(points, points[1:])]
    return {
        "point_count": len(points),
        "segment_count": len(segments),
        "total_km": round(sum(segments), 3),
        "longest_segment_km": round(max(segments, default=0), 3),
    }
