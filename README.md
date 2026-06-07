# Space Invaders 🚀

A modern, highly polished clone of the classic arcade game **Space Invaders**, built entirely in Python using the Pygame library. This project features a robust entity-component-system architecture, state management, particle effects, and dynamic difficulty scaling.

## ✨ Features

- **Dynamic Difficulty Scaling:** As you clear waves, the aliens become faster, drop closer to your ship, and fire more bullets simultaneously. If they get desperate, their fire rate increases dramatically!
- **State Management:** Fully functional game loop with a Main Menu, active Play State, Wave Clear transitions, and a Game Over screen.
- **High Score Persistence:** Your highest score is automatically saved locally and loaded the next time you boot up the game.
- **Particle Engine:** Custom physics-based particle system for satisfying, colorful explosions when entities are destroyed.
- **The Mystery UFO:** A rare red UFO occasionally flies across the top of the screen. Snipe it for a massive random score bonus!
- **Strategic Combat:** Holding down the fire button reduces your ship's movement speed by 25%, forcing you to choose between offensive firepower and evasive maneuvers.
- **Pause System:** Pause the action at any time to take a breather.

## 🎮 Controls

| Action | Keybinding |
| :--- | :--- |
| **Move Left** | `Left Arrow` or `A` |
| **Move Right** | `Right Arrow` or `D` |
| **Shoot** | `Spacebar` (Hold for rapid fire) |
| **Pause/Unpause** | `P` or `Escape` |
| **Menu Navigation** | `Spacebar` |

## 🛠️ Installation & Setup

1. **Ensure you have Python installed** (Python 3.8+ recommended).
2. **Install Pygame** via pip:
   ```bash
   pip install pygame
   ```
3. **Clone the repository** and navigate to the project directory:
   ```bash
   git clone https://github.com/yourusername/space-invaders.git
   cd space-invaders
   ```
4. **Run the game:**
   ```bash
   python main.py
   ```

## 📂 Architecture & Code Structure

The codebase is organized into cleanly separated modules to ensure scalability and readability:

- `main.py` / `game.py`: The core engine, state machine, and main game loop.
- `/states/`: Contains `menu_state.py`, `play_state.py`, and `game_over_state.py` to handle different phases of the application.
- `/entities/`: Contains the actual game objects (`player.py`, `enemy_grid.py`, `bullet.py`, `ufo.py`).
- `/systems/`: Contains the logic managers that govern the entities (`collision_system.py`, `bullet_manager.py`, `particle_system.py`, `input_manager.py`, etc.).
- `/assets/`: The directory where all `.png` sprites and `.wav` sound effects are stored.

## 🎨 Customizing Assets

The game looks for specific files inside the `assets/` folder to render graphics and play sounds. If it can't find them, it safely falls back to drawing colored rectangles and muting audio.
- **Images:** `player.png`, `enemy_1.png`, `enemy_2.png`, `ufo.png`
- **Audio:** `shoot.wav`, `explosion.wav`, `ufo.wav`

## 📜 License
This project is open-source and available for educational purposes. Feel free to fork, modify, and improve upon the codebase!
