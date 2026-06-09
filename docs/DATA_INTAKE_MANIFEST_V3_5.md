# SlowMate v3.5 Data Intake Manifest

Date: 2026-06-07

This manifest tracks external training data copied into SlowMate for engine
improvements. Source datasets are read-only and remain unchanged in their
original location.

## Source Root

- `e:/Programming Stuff/Chess Engines/Chess Engine Playground/engine-metrics/raw_data/pgn_training_data`

## Intake Targets

1. Syzygy 3-4-5 tablebases
- Source:
  - `syzygy_data_piece_endgames/3-4-5`
- Target:
  - `data/endgames/syzygy/3-4-5`
- Purpose:
  - Exact endgame probing for 3-4-5 piece positions in search.

2. Opening PGN corpus
- Source:
  - `pgn_data_openings/*.pgn`
- Target:
  - `data/training/openings/pgn`
- Purpose:
  - Rebuild and score opening choices using principled human/engine lines.

3. Puzzle CSV corpus
- Source:
  - `csv_data_puzzles/lichess_db_puzzle.csv`
- Target:
  - `data/training/puzzles/lichess_db_puzzle.csv`
- Purpose:
  - Tactical regression suites and future motif-driven evaluation tuning.

4. Endgame PGN corpus
- Source:
  - `pgn_data_endgames/*.pgn`
- Target:
  - `data/training/endgames/pgn`
- Purpose:
  - Add endgame test positions and endgame heuristic examples.

## Notes

- Intake is copy-only. No edits or deletes are performed in source folders.
- Initial v3.5 implementation focuses on runtime Syzygy integration and
  opening/tactical quality hardening.
- Large evaluation JSONL datasets are intentionally deferred for a later
  supervised-evaluation branch.

## Opening Book Builder

Use the offline builder to generate a corpus-based book from imported PGNs:

```bash
python -m src.tools.opening_book_builder \
  --input data/training/openings/pgn \
  --output data/openings/opening_book_generated_v3_5.json \
  --max-halfmoves 30 \
  --min-count 3 \
  --top-k 4
```

You can tune `--min-count` upward for a smaller, more conservative book.