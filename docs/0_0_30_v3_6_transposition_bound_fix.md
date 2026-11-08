# v3.6 - Transposition-Table Bound Fix

**Date**: October 31, 2026  
**Status**: ✅ Implemented and locally validated; GCP deployment pending approval  
**Phase**: Search correctness and Lichess deployment preparation  
**Version**: 3.6  
**Engine ID**: `SlowMate v3.6`

## Motivation

The current search had four transposition-table storage paths. Each updated
`alpha` while searching, then compared the final score against that updated
value to determine the stored bound. Since `alpha` is raised to at least
`best_score`, the upper-bound comparison was always true; exact results and
fail-high results were consequently stored as `UPPER`.

This prevented correct `EXACT` and `LOWER` entries from being recorded and
reduced the value of transposition-table cutoffs. The fix preserves the
original alpha-beta window and classifies each result against that window in
all four search paths.

## Changes

- Corrected bound classification in `_search_depth`,
  `_search_depth_with_pv`, `_negamax`, and `_negamax_with_pv`.
- Updated the engine version to 3.6 and synchronized build naming/features.
- Prepared a Lichess package from the current `src/`, retaining the existing
  opening book and runner layout. Syzygy probing remains optional; the local
  tablebase corpus is not bundled.
- Added parameterized regression tests for exact, fail-low, and fail-high
  storage through each search path, plus an engine/UCI version test.

## Validation

- v3.6 regression tests and v3.5 opening/Syzygy tests: **16 passed**.
- Packaged `run_uci.py` smoke test: advertises `id name SlowMate v3.6` and
  completes the UCI handshake.
- Packaged `src/engine.py` SHA-256 matches the repository's `src/engine.py`.
- No match result or rating improvement is claimed; this is a search
  correctness fix, not a measured strength result.

## Deployment status

The package is staged at `lichess-bot/engines/SlowMate_v3.6/`. The deployment
guide is [CLOUD_DEPLOYMENT_V3_6.md](./CLOUD_DEPLOYMENT_V3_6.md). No GCP VM or
Lichess configuration has been changed. Deploy only after explicit approval.
