import csv
import tempfile
import unittest
from pathlib import Path
from gps_distance_processing.main import haversine_km, process_track


class GpsTests(unittest.TestCase):
    def test_same_location(self):
        self.assertAlmostEqual(haversine_km(-37.81, 144.96, -37.81, 144.96), 0)

    def test_one_degree_equator(self):
        self.assertAlmostEqual(haversine_km(0, 0, 0, 1), 111.195, places=2)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            haversine_km(91, 0, 0, 0)

    def test_csv_transformation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / "input.csv", Path(tmp) / "output.csv"
            source.write_text("timestamp,latitude,longitude\na,0,0\nb,0,1\n", encoding="utf-8")
            self.assertEqual(process_track(source, dest), 2)
            with open(dest, encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]["segment_km"], "0.000")
            self.assertEqual(rows[1]["segment_km"], "111.195")

    def test_empty_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / "input.csv", Path(tmp) / "output.csv"
            source.write_text("timestamp,latitude,longitude\n", encoding="utf-8")
            self.assertEqual(process_track(source, dest), 0)
            self.assertEqual(dest.read_text().strip(), "timestamp,latitude,longitude,segment_km")


if __name__ == "__main__":
    unittest.main()
