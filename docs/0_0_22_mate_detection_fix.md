# Mate Detection Fix - v3.3

## Issue Description
**Critical Bug:** SlowMate v3.2 missed a mate-in-1 at move 40 in game vs v7p3r (2025-12-05)

### Position Analysis
```
After 40.Kd4, Black played 40...Qd8?? allowing 41.Qxd8#
Evaluation before blunder: -10.09 (Black winning)
Correct move: 40...Qe5+ (forces king movement, continues attack)
```

### Root Causes
1. **Quiescence Search Blindness**: No mate/stalemate detection when no captures available
2. **Horizon Effect**: Engine can't see 1-ply checkmates if they're past quiescence depth
3. **Move Generation**: No special priority for checking moves in quiescence
4. **King Safety**: Failed to detect king walking into mate threats

## Fixes Implemented

### 1. Mate Detection in Quiescence Search
Added comprehensive terminal node detection:
- Check for checkmate when no legal moves
- Check for stalemate when no legal moves
- Check if IN CHECK even when stand-pat looks good
- Return proper mate scores with distance-to-mate

### 2. Check Extension in Quiescence
- Extended quiescence search when in check (checks are forcing)
- Added checking moves to quiescence consideration
- Prioritize checking moves that might be mate

### 3. Mate Distance Scoring
- Changed from `-20000` to `-30000 + ply` for proper mate distance
- Engine now prefers shorter mates and longer defensive sequences
- PV correctly shows forced mate sequences

### 4. Move Ordering Enhancement
- Checking moves get +10000 bonus in move ordering
- Captures of high-value pieces prioritized
- Mate threats detected earlier in search tree

## Testing Strategy
1. **Perft Tests**: Verify no regression in move generation
2. **Mate Puzzles**: Test suite of mate-in-1, mate-in-2, mate-in-3
3. **Regression Game**: Replay the v7p3r game, verify 40...Qe5+ is chosen
4. **Tournament Testing**: Monitor for similar blunders in live play

## Expected Impact
- **Zero Mate-in-1 Blunders**: Engine will never miss 1-ply checkmates
- **Improved Tactical Awareness**: Better detection of checking sequences
- **Rating Gain**: Estimated +50-100 ELO from eliminating catastrophic blunders
- **Confidence**: Can defend winning positions without self-destructing

## Version Update
- **v3.2 → v3.3**: Mate detection enhancement
- **Priority**: CRITICAL (game-losing bug)
- **Deployment**: Immediate to cloud after validation

## References
- Game PGN: `analysis/critical_games/mate_in_1_blunder_20251205.pgn`
- Lichess Link: https://lichess.org/QJTFBLrr
- Issue: Horizon effect + quiescence blindness
