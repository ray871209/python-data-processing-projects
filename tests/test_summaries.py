import csv
import tempfile
import unittest
from pathlib import Path
from movie_review_analysis.summary import summarize_movies
from gps_distance_processing.track_summary import summarize_track

class SummaryTests(unittest.TestCase):
    def test_empty_movie_list(self):
        self.assertEqual(summarize_movies([]), [])

    def test_movie_grouping(self):
        result = summarize_movies([
            {"movie":"A", "rating":8, "comment":"great"},
            {"movie":"A", "rating":6, "comment":"slow"},
            {"movie":"B", "rating":9, "comment":"excellent"},
        ])
        self.assertEqual(result[0]["review_count"], 2)
        self.assertEqual(result[0]["average_rating"], 7)
        self.assertEqual(result[1]["movie"], "B")

    def test_gps_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            with path.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["latitude", "longitude"])
                w.writerow([0, 0])
                w.writerow([0, 1])
            result = summarize_track(path)
            self.assertEqual(result["segment_count"], 1)
            self.assertAlmostEqual(result["total_km"], 111.195, places=2)

    def test_empty_gps(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.csv"
            path.write_text("latitude,longitude\n", encoding="utf-8")
            self.assertEqual(summarize_track(path)["total_km"], 0)

if __name__ == "__main__":
    unittest.main()
