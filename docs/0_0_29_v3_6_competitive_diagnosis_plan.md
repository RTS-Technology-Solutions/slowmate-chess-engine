# v3.6 Competitive Diagnosis and Improvement Plan

**Date**: October 31, 2026  
**Status**: ✅ v3.6 implementation and package staged; deployment pending approval  
**Phase**: Competitive diagnosis and release preparation  
**Current target**: SlowMate v3.6

## Evidence from supplied game records

The supplied PGNs were parsed by game headers. These are match outcomes, not
engine-strength estimates, and the two exports overlap in dates; do not add
their totals together.

| PGN export | Games | SlowMate vs C0BR4 | SlowMate vs V7P3R |
|---|---:|---:|---:|
| `20261031_lichess_slowmate_bot.pgn` | 10,524 | 1 win, 63 draws, 201 losses (32.5/265 points; 12.3%) | No games |
| `20260608_lichess_slowmate_bot.pgn` | 8,102 | 2 wins, 60 draws, 216 losses (32/278 points; 11.5%) | 3 wins, 0 draws, 9 losses (3/12 points; 25%) |
| User-supplied V7P3R export dated 2026-05-18 | 6,004 | Not used for SlowMate-C0BR4 totals | 2 wins, 0 draws, 5 losses (2/7 points; 28.6%) |

The newer export's C0BR4 games span June 9 through September 12, 2026; all 265
are recorded with `Normal` termination. The older export also has two C0BR4
games ending on time. The user-supplied V7P3R file contains seven SlowMate
head-to-head games from November 21 through December 6, 2025; two ended on
time. It is the latest V7P3R file available, but not a recent test of the
current engine. These results establish persistent head-to-head problems, but
do not identify their chess causes.

## Repository and live deployment baseline

The root engine currently reports v3.5 and includes Syzygy probing, while
`build/build_config.py` still describes v3.2. The checked-in
`lichess-bot/config.yml` points to `SlowMate_v3.3`; the v3.5 deployment
documents describe a procedure but do not confirm that it was completed. The
PGNs do not identify which package/version played each historical game.

Read-only inspection of GCP on October 31, 2026 established:

- Project `slowmate-lichess-bot`, VM `slowmate-bot-vm` in `us-central1-a` is
  `RUNNING`; `slowmate-bot.service` is `active`/`running`.
- The VM's live bot config points to `./engines/SlowMate_v3.4/` and launches
  `run_uci.py`.
- That package's runner identifies itself as v3.4 and its engine
  `get_version()` returns `3.4`, but the UCI `id name` is **SlowMate v3.3**.
  Search telemetry also labels allocated time as v3.2. These stale identifiers
  make Lichess/client logs misleading and should be reconciled before the next
  release.
- The bot service process started at 2026-10-31 13:21 UTC. This verifies the
  currently configured deployment, not which engine version played games
  earlier in the year.
- The public Lichess profile reported `seenAt` 2026-10-31 14:22 UTC during
  inspection. The public response did not provide an `online` field, so this
  confirms recent activity but is not proof of current online presence.

The current config accepts standard games from 60+0 through 600+180 seconds
within its configured bounds (60-600 seconds base, 0-180 seconds increment);
the V7P3R sample itself mixes 120+1, 300+1/3, and 600+3/5 controls. Compare
results by time control rather than treating those games as one homogeneous
match.

The PGNs provide moves and outcomes, but no per-move evaluations, clock
telemetry, or deployment version. Therefore, do not introduce opponent-specific
opening lines, evaluation weights, or search parameters based only on the win
rate. First classify the losses and find repeatable, testable failure modes.

## v3.6 work and remaining validation

1. **Reconcile provenance**: the v3.6 source and staged package now advertise
   v3.6 consistently. The older live v3.4 package still has mismatched
   identifiers; this is addressed by switching to the v3.6 package only after
   deployment approval. Historical game-to-version mapping remains unknown.
2. **Analyze decisive C0BR4 games**: identify recurring loss mechanisms (for
   example, tactical blunders, opening disadvantage, endgame conversion, or
   time forfeits) from annotated positions and clock data. Keep draws separate
   from losses.
3. **Implement one search correctness fix**: v3.6 now stores transposition
   bounds against the original alpha-beta window; regression tests cover exact,
   upper, and lower bounds in all four search paths.
4. **Gate the release**: focused tests and a packaged UCI smoke test pass.
   A fixed-color-swapped match is still required before claiming a strength
   improvement. Report W/D/L and score with sample sizes.
5. **Refresh control coverage**: obtain a current V7P3R sample before making a
   competitor-specific claim or selecting an anti-V7P3R change.

## Remaining evidence gaps before making strength claims

- Deployment records mapping the historical C0BR4 games to packages/commits;
  the current live VM is configured for v3.4, but that does not establish
  which version played games through September.
- The PGNs have not been analyzed with engine evaluations. Obtain annotated
  decisive C0BR4 games or run a controlled local analysis before attributing
  the match results to a specific chess weakness.
- No newer V7P3R games are available: the bot is under maintenance. Keep the
  May 18, 2026 export as the latest baseline and refresh when it returns.
- Confirm whether the checked-in challenge settings were active for all
  games, since the PGNs include multiple controls.

The v3.6 change, package, release notes, and deployment runbook are prepared.
The code change addresses a search correctness defect but is not yet validated
by an engine match. No GCP VM or live Lichess configuration has been changed.
