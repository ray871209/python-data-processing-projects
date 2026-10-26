"""Additional unit tests for independently reimplemented coursework-inspired examples."""
import unittest
from gps_distance_processing.main import haversine_km
from movie_review_analysis.main import sentiment_score, clean_reviews, auto_reply

class EdgeCaseTests(unittest.TestCase):
    def test_antimeridian(self):
        self.assertAlmostEqual(haversine_km(0, 179.5, 0, -179.5), 111.195, places=2)

    def test_out_of_range_longitude(self):
        with self.assertRaises(ValueError):
            haversine_km(0, -181, 0, 0)

    def test_empty_input(self):
        self.assertEqual(clean_reviews([]), [])

    def test_review_score_boundaries(self):
        self.assertIn("Thanks", auto_reply("A", "Film", 0))
        self.assertIn("glad", auto_reply("A", "Film", 10))

    def test_lexicon_limit_documentation(self):
        # This intentionally demonstrates a limitation of bag-of-words sentiment.
        self.assertEqual(sentiment_score("not good"), 1)

if __name__ == "__main__":
    unittest.main()
