# 2048 - Python Pygame Edition 🎮

This is a Python-based version of the classic puzzle game **2048**, built using the **Pygame** library. The goal is simple: combine matching tiles to reach the number **2048**!

---

## 🧩 How to Play

- Use arrow keys to move all tiles in one direction.
- When two tiles with the same number collide, they merge into one.
  - (Example: 2 + 2 = 4, 4 + 4 = 8, and so on.)
- A new tile (2 or 4) appears randomly after every move.
- **You win when you create a tile with the number 2048!**
- The game ends when no more moves are possible.

---

## 🎮 Controls

| Action      | Key           |
|-------------|---------------|
| Move Left   | ← Arrow Key   |
| Move Right  | → Arrow Key   |
| Move Up     | ↑ Arrow Key   |
| Move Down   | ↓ Arrow Key   |
| Start Game  | Click the "PLAY" button on the start screen |
| Restart Game | Click "Play Again" on the Game Over screen |

---

## 💾 Requirements

You need to have Python installed (version **3.7 or higher**) and install the Pygame library:

```bash
pip install pygame

How to Run

git clone https://github.com/your-username/2048-python.git

Navigate into the project folder:

cd 2048-python/src

Run the game:

python ui_pygame.py


Game Stats
Your progress is saved automatically to a file named stats.json, including:

Your high score

Total number of wins