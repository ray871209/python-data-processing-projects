"""Transform an example GPS CSV and compute segment distances in kilometres."""

from __future__ import annotations

import argparse
import csv
from math import asin, cos, radians, sin, sqrt
from pathlib import Path

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two geographic positions in kilometres."""
    if not all((-90 <= lat <= 90 for lat in (lat1, lat2))):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not all((-180 <= lon <= 180 for lon in (lon1, lon2))):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    a_lat, b_lat = radians(lat1), radians(lat2)
    delta_lat = b_lat - a_lat
    delta_lon = radians(lon2 - lon1)
    a = sin(delta_lat / 2) ** 2 + cos(a_lat) * cos(b_lat) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(min(1, sqrt(a)))


def process_track(input_path: str | Path, output_path: str | Path) -> int:
    """Output original columns plus segment_km, calculated from previous point."""
    with open(input_path, newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        for field in ("timestamp", "latitude", "longitude"):
            if field not in fields:
                raise ValueError(f"Missing required column: {field}")
        rows = list(reader)

    transformed = []
    previous: tuple[float, float] | None = None
    for line_number, row in enumerate(rows, start=2):
        try:
            lat, lon = float(row["latitude"]), float(row["longitude"])
            # Validate even the first coordinate.
            haversine_km(lat, lon, lat, lon)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid coordinate at CSV line {line_number}") from exc
        distance = 0.0 if previous is None else haversine_km(*previous, lat, lon)
        transformed.append({**row, "segment_km": f"{distance:.3f}"})
        previous = (lat, lon)

    with open(output_path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=[*fields, "segment_km"])
        writer.writeheader()
        writer.writerows(transformed)
    return len(transformed)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate distance between consecutive GPS points.")
    parser.add_argument("input", nargs="?", default=str(Path(__file__).parent / "data" / "sample_track.csv"))
    parser.add_argument("output", nargs="?", default=str(Path(__file__).parent / "data" / "output_track.csv"))
    args = parser.parse_args()
    count = process_track(args.input, args.output)
    print(f"Processed {count} GPS points -> {args.output}")


if __name__ == "__main__":
    main()
