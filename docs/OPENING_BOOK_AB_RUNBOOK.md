# Opening Book A/B Runbook

This runbook compares baseline opening book (A) vs generated opening book (B) on Lichess rapid games.

## 1) Runtime Requirement

The lichess-bot engine now supports environment override:
- `SLOWMATE_OPENING_BOOK_PATH`

This is wired in:
- `lichess-bot/engines/SlowMate_v3.3/src/core/opening_book.py`

## 2) Run Variant A (Baseline)

From repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/ab/run_book_a.ps1
```

## 3) Run Variant B (Generated Book)

From repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/ab/run_book_b.ps1
```

Optional custom generated book:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/ab/run_book_b.ps1 -BookPath "E:\\...\\your_book.json"
```

## 4) Separate PGN Buckets (Recommended)

To make comparison cleaner, set `pgn_directory` in `lichess-bot/config.yml` to different folders before each run:
- Variant A run: `game_records_ab/a`
- Variant B run: `game_records_ab/b`

## 5) Compare Results After 1-2 Days

Use the A/B comparator:

```powershell
C:/Users/Pat/AppData/Local/Python/pythoncore-3.14-64/python.exe -m src.tools.pgn_ab_compare --a lichess-bot/game_records_ab/a --b lichess-bot/game_records_ab/b --only-rapid
```

## 6) Profile and Trim the Generated Book

Generate profile report and trimmed book candidate:

```powershell
C:/Users/Pat/AppData/Local/Python/pythoncore-3.14-64/python.exe -m src.tools.opening_book_profiler --input data/openings/opening_book_generated_v3_5.json --report docs/reports/opening_book_profile_generated_v3_5.md --trim-output data/openings/opening_book_generated_v3_5_trimmed.json --min-weight 5 --top-k 4 --max-ply 24 --remove-risky-early
```

Then run Variant B with the trimmed book:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/ab/run_book_b.ps1 -BookPath "e:\Programming Stuff\Chess Engines\SlowMate Chess Engine\slowmate-chess-engine\data\openings\opening_book_generated_v3_5_trimmed.json"
```
