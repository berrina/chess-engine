# Chess Engine

A chess engine built from scratch in Python, implementing legal move generation,
minimax search with alpha-beta pruning, and a material-based evaluation function.
Playable via terminal or a simple web interface.

## Features
- Full board representation and move generation for all 6 piece types
  (pawns, knights, bishops, rooks, queens, king)
- Legal move filtering (rejects moves that leave your own king in check)
- Minimax search with alpha-beta pruning
- Material-based position evaluation
- Verified correct via perft testing against known reference values
  (depth 1: 20, depth 2: 400, depth 3: 8,902 — all confirmed)
- Playable via terminal CLI or browser-based UI (Flask backend)

## How it works
Move generation is handled per piece type, with rook/bishop/queen sharing a
common "sliding" implementation (step in a direction until blocked by the edge
of the board or another piece). Legal moves are filtered by simulating each
candidate move and checking whether it leaves the mover's own king in check.

The engine picks moves via minimax search: it looks ahead a fixed number of
moves, assuming both sides play their best available option at each step, and
scores resulting positions using material count (standard piece values, pawn=1
through queen=9). Alpha-beta pruning skips branches that are mathematically
proven not to affect the final decision, without changing the result.

## Known limitations
This was built with a tight timeline, so some rules are intentionally out of
scope for now:
- No castling
- No en passant
- No pawn promotion (pawns currently stop at the back rank)
- No checkmate/stalemate detection (games don't auto-end)

These are natural next additions — castling and promotion in particular are on
the roadmap.


## Verifying correctness

## Running it

### Terminal

Enter moves as `from_row,from_col to_row,to_col` (e.g. `1,4 3,4`). Rows/columns
are 0-7.

### Web
Then open http://127.0.0.1:5000 in your browser. Click a piece, then click its
destination square.

## verifying correctness 

Runs a perft test against the starting position and prints legal move-sequence
counts at depths 1-3, which should match known reference values (20, 400, 8902).

## Project structure

chess-engine/
├── engine/
│ ├── board.py # board state, piece movement, legal move generation
│ ├── search.py # minimax + alpha-beta search
│ └── perft.py # correctness verification
├── templates/
│ └── index.html # web UI
├── cli.py # terminal play loop
├── app.py # Flask web server
└── README.md

## Tech
Python, Flask, vanilla JS/HTML/CSS (no frontend framework or build step).