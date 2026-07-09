# Chess (Python)♟️

A player-vs-player chess game software implementing all FIDE rules except for threefold repetition, the 50-move rule, and insufficient material draws.

Built from scratch in Python using the Pygame library, this project focuses on complex board state management and accurate move validation. Originally finished in early 2024 before the age of AI for a high school senior CS project.

## Features
* **Complete Core Mechanics:** Accurate move generation and capture logic for all piece types.
* **Special Moves Implemented:**
  * En Passant (via specialized square tracking)
  * Castling (Kingside & Queenside rights management)
  * Pawn Promotion (interactive UI for selecting Queen, Rook, Bishop, or Knight)
* **Check, Checkmate, & Stalemate Detection:** Algorithm actively filters out pseudo-legal moves that would leave the King vulnerable, and successfully detects Checkmate vs. Stalemate conditions.
* **Custom Pygame GUI:** Includes a built-in game clock, interactive square highlighting (legal moves, checks), and resignation controls.

## Prerequisites
* Python 3.x
* [Pygame](https://www.pygame.org/)

## Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/anrenguo/Chess-Python-.git
```
**2. Navigate to the directory:**
```bash
cd Chess-Python-
```
**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```
## How to Play
Run the main script from your terminal to launch the game interface:
```bash
python main.py
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.
