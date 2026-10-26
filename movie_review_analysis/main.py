"""Small illustrative review-processing workflow (standard library only)."""

from __future__ import annotations

import csv
import re
from pathlib import Path

# New, deliberately small sample word list: not a comprehensive sentiment model.
SENTIMENT = {
    "excellent": 3, "wonderful": 3, "enjoyed": 2, "great": 2,
    "fun": 1, "good": 1, "boring": -2, "slow": -1,
    "poor": -2, "awful": -3, "confusing": -1, "disappointing": -2,
}


def tokenize(text: str) -> list[str]:
    """Extract lower-case English words, ignoring punctuation."""
    return re.findall(r"[a-z]+", text.lower())


def sentiment_score(comment: str, lexicon: dict[str, int] | None = None) -> int:
    """Sum scores for matching words (a simple bag-of-words baseline)."""
    weights = SENTIMENT if lexicon is None else lexicon
    return sum(weights.get(token, 0) for token in tokenize(comment))


def clean_reviews(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Discard malformed/duplicate records; keep the first occurrence of an ID."""
    valid: list[dict[str, object]] = []
    seen: set[str] = set()
    for row in rows:
        review_id = row.get("review_id", "").strip()
        reviewer = row.get("reviewer", "").strip()
        movie = row.get("movie", "").strip()
        if not review_id or not reviewer or not movie or review_id in seen:
            continue
        try:
            rating = float(row.get("rating", ""))
        except (ValueError, TypeError):
            continue
        if not 0 <= rating <= 10:
            continue
        seen.add(review_id)
        valid.append({
            "review_id": review_id, "reviewer": reviewer, "movie": movie,
            "rating": rating, "comment": row.get("comment", ""),
        })
    return valid


def average_favorability(
    reviews: list[dict[str, object]], reviewer: str
) -> float | None:
    """Average 80% rating + 20% lexicon score for a given reviewer."""
    values = [
        0.8 * float(r["rating"]) + 0.2 * sentiment_score(str(r["comment"]))
        for r in reviews if r["reviewer"] == reviewer
    ]
    return round(sum(values) / len(values), 2) if values else None


def auto_reply(reviewer: str, movie: str, rating: float) -> str:
    """Build a short response using the supplied 0–10 rating."""
    if not 0 <= rating <= 10:
        raise ValueError("Rating must be between 0 and 10.")
    if rating < 4:
        response = "Thanks for the feedback. We are sorry it was disappointing."
    elif rating < 7:
        response = "Thanks for sharing your thoughts."
    else:
        response = "We are glad you enjoyed it!"
    return f"Hi {reviewer}, thanks for reviewing {movie}. {response}"


def load_reviews(path: str | Path) -> list[dict[str, object]]:
    with open(path, encoding="utf-8", newline="") as stream:
        return clean_reviews(list(csv.DictReader(stream)))


def main() -> None:
    source = Path(__file__).parent / "data" / "sample_reviews.csv"
    reviews = load_reviews(source)
    print(f"Valid unique reviews: {len(reviews)}")
    for reviewer in sorted({str(review["reviewer"]) for review in reviews}):
        print(f"{reviewer}: average favorability = {average_favorability(reviews, reviewer)}")
    sample = reviews[0]
    print(auto_reply(str(sample["reviewer"]), str(sample["movie"]), float(sample["rating"])))


if __name__ == "__main__":
    main()
