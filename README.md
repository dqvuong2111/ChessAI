# Chess AI Game

## Overview
This is a chess game with an AI opponent implemented using Pygame and Python-Chess libraries. The AI uses the Minimax algorithm with alpha-beta pruning and piece-square tables for evaluation.

## Prerequisites
- Python 3.8+
- Pygame
- Python-Chess library

## Installation

Install dependencies:
```
pip install pygame python-chess
```

## Running the Game

Run the game directly:

```
python src/main.py
```

This will start the game with default settings:
- AI Mode: Enabled (play against AI)
- AI Depth: 3
- Algorithm: Minimax with Alpha-Beta pruning

### Customizing Game Parameters

You can easily customize the game parameters by editing the values in `src/main.py`:

```python
# Configure parameters here
app = Main(
    ai_mode=True,     # True: Play against AI, False: Two human players
    ai_depth=3,       # AI search depth (1-5)
    use_alpha_beta=True   # True: Use Alpha-Beta pruning, False: Standard Minimax
)
app.mainloop()
```

## Game Features

- Complete chess game with all standard rules
- AI opponent using Minimax algorithm with Alpha-Beta pruning
- Visual highlighting of legal moves and captures
- Sound effects for moves and captures
- End game detection (checkmate, stalemate)
- AI calculation time display
- Ability to adjust AI difficulty during gameplay

## Game Controls
- Click to select and move chess pieces
- 'r': Restart the game
- '+': Increase AI search depth (makes AI stronger but slower)
- '-': Decrease AI search depth (makes AI faster but weaker)
- 'a': Toggle between Alpha-Beta pruning and standard Minimax algorithms
- Close window to exit

## Project Structure and Classes

### Main Class (`main.py`)
- Main entry point for the application
- Main class controlling the game flow
- Handles the main game loop and player events
- Renders game interface and end game screens
- Manages AI game mode and parameters

### Game Class (`game.py`) 
- Manages game state
- Handles move sound effects
- Renders chessboard and pieces
- Displays legal moves and capture possibilities

### Board Class (`board.py`)
- Manages chess board using python-chess library
- Handles moves and validates their legality
- Checks for conditions like checkmate and stalemate
- Manages piece states and positions

### ChessAI Class (`ai.py`)
- Implements AI opponent using minimax algorithm with alpha-beta pruning
- Evaluates piece positions using position value tables
- Calculates best moves for AI
- Tracks number of calculations performed

### Config Class (`config.py`)
- Manages game configuration and interface
- Provides different color themes for the board
- Manages fonts and display settings

### Theme Class (`theme.py`)
- Defines color themes for the chess board
- Manages colors for light/dark squares
- Defines highlight colors for legal moves

## Customizing the AI

The AI's behavior can be customized in two ways:

### 1. Through the Main File
The easiest way to customize the AI is by modifying the parameters in `main.py`:
- `ai_depth`: Sets the AI search depth (1-5)
- `use_alpha_beta`: Toggles between Alpha-Beta pruning and standard Minimax

### 2. During Gameplay
You can also adjust the AI during gameplay:
- Press '+' to increase AI search depth (makes AI stronger but slower)
- Press '-' to decrease AI search depth (makes AI faster but weaker)
- Press 'a' to toggle between Alpha-Beta pruning and standard Minimax

### Algorithm Details

#### Search Depth
- Higher depth values make the AI look further ahead but will make it think longer
- Recommended values: 3-4 for casual play, 5-7 for stronger AI (but slower)
- The depth is fixed and will not automatically change during gameplay

#### Algorithm Selection
- Alpha-Beta pruning is much faster than standard Minimax, especially at higher depths
- Standard Minimax is useful for educational purposes to see the difference in performance
- You can compare the number of calculations between the two algorithms

### Piece Values
You can modify the base values of pieces by changing the values in the `_get_piece_value` method:
```python
values = {
    chess.PAWN: 10.0,
    chess.KNIGHT: 30.0,
    chess.BISHOP: 30.0,
    chess.ROOK: 50.0,
    chess.QUEEN: 90.0,
    chess.KING: 900.0
}
```

### Position Evaluation
The AI uses piece-square tables to evaluate piece positions. These can be modified in the `ChessAI` class initialization:
- `pawn_eval_white`: Pawn position values
- `knight_eval_white`: Knight position values
- `bishop_eval_white`: Bishop position values
- `rook_eval_white`: Rook position values
- `queen_eval_white`: Queen position values
- `king_eval_white`: King position values

Higher values (positive) encourage pieces to move to those squares, while lower values (negative) discourage piece placement.

## Troubleshooting
- Ensure all dependencies are installed
- Check Python and Pygame versions are compatible
- Verify you're running from the project root directory
- On Windows, use Command Prompt or PowerShell to run commands

## Contributing
Feel free to open issues or submit pull requests.
