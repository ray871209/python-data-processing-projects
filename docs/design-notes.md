# Python implementation notes

The demonstrations are newer portfolio adaptations, not original graded submissions.

## Reviews
- Validation checks ratings in 0–10 and missing record identifiers.
- Deduplication keeps the first valid review per ID: this is a deliberate example policy.
- Sentiment uses a tiny hand-built lexicon and can mishandle negation, irony, and context.
- Weighted favorability is illustrative, not a validated rating scale.

## GPS
- Haversine uses a spherical Earth model; road travel and elevation are not included.
- Points are processed in CSV order. Real trajectories should validate timestamps and units.
- First segment distance is zero by convention; output rounds to three decimal places.
- Invalid coordinates raise exceptions.

## Extensions
Test empty data, antimeridian crossings, out-of-range coordinates, duplicate records, and reversed timestamps. Add structured logging and reproducible input manifests for production workloads.
