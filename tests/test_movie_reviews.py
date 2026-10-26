import unittest
from movie_review_analysis.main import (
    auto_reply, average_favorability, clean_reviews, sentiment_score, tokenize, load_reviews
)
from pathlib import Path


class ReviewTests(unittest.TestCase):
    def test_tokenization(self):
        self.assertEqual(tokenize("GREAT, great!"), ["great", "great"])

    def test_sentiment(self):
        self.assertEqual(sentiment_score("Great but slow."), 1)

    def test_clean_deduplicate_and_validate(self):
        rows = [
            {"review_id": "1", "reviewer": "A", "movie": "M", "rating": "6", "comment": "good"},
            {"review_id": "1", "reviewer": "A", "movie": "M", "rating": "6", "comment": "good"},
            {"review_id": "2", "reviewer": "A", "movie": "M", "rating": "99", "comment": "great"},
        ]
        self.assertEqual(len(clean_reviews(rows)), 1)

    def test_favorability(self):
        reviews = [{"reviewer": "A", "rating": 8.0, "comment": "great"}]
        self.assertEqual(average_favorability(reviews, "A"), 6.8)
        self.assertIsNone(average_favorability(reviews, "B"))

    def test_reply(self):
        self.assertIn("glad", auto_reply("A", "M", 8))
        with self.assertRaises(ValueError):
            auto_reply("A", "M", -1)

    def test_fixture(self):
        path = Path(__file__).resolve().parents[1] / "movie_review_analysis/data/sample_reviews.csv"
        self.assertEqual(len(load_reviews(path)), 5)


if __name__ == "__main__":
    unittest.main()
