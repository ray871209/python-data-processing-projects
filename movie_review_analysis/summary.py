"""Aggregate clean, fictional review data by film; no third-party libraries."""
from collections import defaultdict
from movie_review_analysis.main import sentiment_score

def summarize_movies(reviews):
    groups = defaultdict(list)
    for row in reviews:
        groups[str(row["movie"])].append(row)
    output = []
    for movie, group in sorted(groups.items()):
        ratings = [float(r["rating"]) for r in group]
        output.append({
            "movie": movie, "review_count": len(group),
            "average_rating": round(sum(ratings) / len(ratings), 2),
            "mean_lexicon_sentiment": round(
                sum(sentiment_score(str(r["comment"])) for r in group) / len(group), 2
            ),
        })
    return output
