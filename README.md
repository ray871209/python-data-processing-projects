# Python Data Processing Projects

Two small, self-contained projects illustrating foundational Python programming and data-processing skills.

These examples were **newly implemented and tested for portfolio use**, inspired by programming concepts I practised in a 2023 University of Melbourne *Introduction to Programming* course. They are **not original submitted assignments**, nor copies of assignment prompts or university-supplied datasets. The portfolio adaptation and tests were prepared with AI assistance.

## Projects

### 1. Movie review analysis
- Clean review text and validate ratings
- Deduplicate records using review IDs
- Score sentiment with a **small, custom demonstration lexicon**
- Compute a transparent, weighted favorability score
- Produce a personalized reply based on a film rating

### 2. GPS distance processing
- Read and write CSV files with Python's standard library
- Validate coordinate pairs
- Calculate distances between successive GPS points using the Haversine formula
- Save a transformed CSV with a segment-distance column

## Quick start

Requires **Python 3.10+**. No external packages or API keys.

```bash
python movie_review_analysis/main.py
python gps_distance_processing/main.py gps_distance_processing/data/sample_track.csv gps_distance_processing/data/output_track.csv
python -m unittest discover -s tests -v
```

The GPS output is written to `gps_distance_processing/data/output_track.csv` (ignored by Git).

## Structure

```text
movie_review_analysis/
  main.py                 Review analysis logic and demonstration
  data/sample_reviews.csv Fictional reviews
gps_distance_processing/
  main.py                 CSV transformation and distance logic
  data/sample_track.csv   Fictional GPS points
tests/
  test_movie_reviews.py
  test_gps_distance.py
PROJECT_NOTES.md
```

## Limitations

- Sentiment analysis is rule-based and uses a deliberately tiny demonstration lexicon. It is **not machine learning**, and negations or nuanced language may be misclassified.
- Favorability is an illustrative blend of ratings and lexicon scores, not a validated metric.
- GPS distances are between successive points, not road-routing distances; distances are in **kilometres**.
- Sample records were generated specifically for this portfolio and do not represent actual customers or GPS traces.

## Academic integrity and provenance

The project is a post-course educational adaptation; it does not redistribute examination materials, university assignment questions, supplied data or lecture slides. Course-related public sharing rules should be confirmed before switching the repository from Private to Public.
