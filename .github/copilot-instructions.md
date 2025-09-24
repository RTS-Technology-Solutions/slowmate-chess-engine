# SlowMate Chess Engine - AI Development Guide

## Architecture Overview

SlowMate is an educational UCI-compliant chess engine built in Python. The architecture follows a modular design centered around competitive tournament play and iterative development.

### Core Components

**Entry Point**: `src/uci_main.py` - Main UCI interface for chess GUIs (Arena, Nibbler, etc.)
**Engine Core**: `src/engine.py` - Production engine with v3.x architecture (current v3.1)  
**Search**: `src/search/enhanced.py` - Advanced search with transposition tables, move ordering
**Evaluation**: `src/core/enhanced_evaluate.py` - Position evaluation with piece-square tables, game phase detection
**UCI Protocol**: `src/uci/protocol_v2_2.py` - Robust UCI implementation for chess software integration

### Key Data Flow
```
UCI GUI → uci_main.py → engine.py → search/evaluation → UCI responses
```

## Development Patterns

### Version Management
- **Sub-versions**: e.g., v3.1 → v3.2 → v3.3 (incremental improvements)
- **Major versions**: Complete rewrites/architecture changes
- **Build configs**: `build/build_config.py` manages version strings and executable names
- **Documentation**: Each version documented in `docs/` with implementation details

### Build System
```bash
# Build executable for tournament use
cd build/
python build_executable.py
```
- Uses PyInstaller for single-file executables
- Dynamic naming based on `build_config.py`
- Hidden imports for all slowmate modules required

### Testing Philosophy
- **Production validation**: `testing/test_v3_0_production_validation.py` style comprehensive suites
- **Feature-specific tests**: Each major feature has dedicated test files
- **Tournament testing**: Real Arena GUI integration tests
- **A/B testing**: Compare versions directly with blunder detection

## Chess Engine Specifics

### UCI Protocol Implementation
- Engine identifies as "SlowMate v{version}" 
- Must handle: `uci`, `isready`, `position`, `go`, `stop`, `quit`
- Threaded search to prevent UCI blocking
- Time management with tournament controls (wtime/btime/winc/binc)

### Search Architecture
- **Iterative deepening** with aspiration windows
- **Transposition tables** for position caching
- **Move ordering**: TT moves → captures → killers → history
- **Pruning**: Late move reduction, null move pruning, quiescence search

### Evaluation Features
- Game phase detection (opening/middlegame/endgame)
- Piece-square tables with phase interpolation
- Pawn structure analysis (passed, isolated, doubled pawns)
- King safety evaluation
- **Critical**: Evaluation must be from current player's perspective

### Common Pitfalls
- **Perspective bug**: Ensure evaluation returns positive for side-to-move
- **UCI threading**: Search must be interruptible via `stop_requested` flag  
- **Time management**: Don't exceed allocated time in tournaments
- **Move validation**: Always validate moves are legal before making them

## Development Commands

### Testing
```bash
# Comprehensive validation
python testing/test_v3_0_production_validation.py

# UCI protocol testing  
python testing/integration_tests/test_uci.py

# Feature-specific testing
python testing/test_{feature_name}.py
```

### Analysis Tools
```bash
# Game analysis for improvement
python analysis/game_analysis_utility.py --games-dir games/

# Engine feature audit
python testing/audit_engine_features.py
```

## File Naming Conventions

- **Engine files**: `engine.py`, `engine_v2_1.py` (version-specific engines)
- **Documentation**: `docs/0_0_XX_feature_name.md` (chronological numbering)
- **Tests**: `test_v{version}_validation.py` or `test_{feature}.py`
- **Executables**: `SlowMate_v{version}.exe` (tournament-ready builds)

## Integration Points

### External Dependencies
- `python-chess`: Board representation, move generation, UCI parsing
- `PyInstaller`: Executable packaging for tournament deployment
- **No other external engines** - pure Python implementation

### Tournament Integration
- Arena GUI: Load executable directly
- Engine battles: Automated tournaments via Arena's tournament manager
- Time controls: 2+1, 5+5 (testing), 10min, 30min (tournaments)

## Performance Considerations

- **Node count tracking**: `self.nodes` for search statistics
- **Time deadline management**: `self.search_deadline` for time control
- **Memory usage**: Transposition table size configurable (default 64MB)
- **UCI info output**: Real-time depth/score/pv information during search

This engine competes against V7P3R (main competitor), C0BR4 (control), and Stockfish 1% in tournament settings.