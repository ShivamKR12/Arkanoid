# Arkanoid Fire Ball

A modern take on the classic Arkanoid breakout game, built with Python and `pygame-ce`. This project features classic gameplay enhanced with power-ups, multiple levels, two difficulty modes, and a built-in level editor. It's also configured to be playable in a web browser using `pygbag`.

## Features

- **Classic Arkanoid Gameplay**: Break bricks, control the paddle, and keep the ball in play.
- **Multiple Levels**: Progress through increasingly challenging levels.
- **Two Difficulty Modes**: Choose between 'Easy' and 'Hard' to match your skill level. Hard mode features a smaller paddle and a faster ball.
- **Power-ups**: Catch falling power-ups to gain advantages:
    - 🟢 **Expand (E)**: Increases the paddle size temporarily.
    - ❤️ **Life (L)**: Grants an extra life (up to a maximum of 5).
    - 🌐 **Multiball (M)**: Adds one or two extra balls to the screen.
    - 🔫 **Gun (G)**: Allows the paddle to shoot bullets and destroy bricks for a limited time.
- **Multiple Brick Types**:
    - **Breakable**: Standard bricks that are destroyed in one hit.
    - **Multi-hit**: Bricks that require two hits to be destroyed.
    - **Unbreakable**: Indestructible bricks that serve as obstacles.
- **Level Editor**: A simple, built-in tool (`Level-Editor.py`) to create, edit, and save your own custom levels.
- **Web-Ready**: The included GitHub Actions workflow (`.github/workflows/pygbag.yml`) automatically builds the game for the web and deploys it to GitHub Pages.

## How to Play

### Prerequisites

Make sure you have Python installed. This project uses `pygame-ce`, which will be installed via `pip`.

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ShivamKR12/Arkanoid.git
    cd Arkanoid
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install pygame-ce
    ```

4.  **Run the game:**
    ```bash
    python main.py
    ```

### Web Version

The project is configured to be built and deployed to GitHub Pages automatically. You can play the latest version directly in your browser.

## Controls

### In-Game

-   **Left/Right Arrow Keys**: Move the paddle left and right.
-   **Spacebar**: Shoot bullets when the 'Gun' power-up is active.

## Level Editor Usage

To create or modify levels, run the level editor from your terminal:

```bash
python Level-Editor.py
```

The editor provides on-screen instructions for placing different types of bricks, saving/loading levels, and switching between levels.

### Editor Controls

-   **Left Click**: Place a brick of the selected type and color.
-   **Right Click**: Remove a brick.
-   **Keys 1-6**: Select brick color.
-   **B**: Set brick type to **B**reakable.
-   **M**: Set brick type to **M**ulti-hit.
-   **U**: Set brick type to **U**nbreakable.
-   **S**: **S**ave the current level layout to a JSON file.
-   **L**: **L**oad the layout for the current level number.
-   **C**: **C**lear the entire grid.
-   **Left/Right Arrow Keys**: Switch between level numbers to load/save.
-   **H**: Toggle the help/controls display.

## Project Structure

```
Arkanoid/
├── .github/workflows/pygbag.yml  # GitHub Actions workflow for web build
├── assets/sounds/                # Game sound effects
├── levels/                       # JSON files for level layouts
│   ├── level1.json
│   └── ...
├── main.py                       # Main game entry point
├── player.py                     # Paddle class
├── bricks.py                     # Brick class
├── levels.py                     # Level loading logic
├── Powerups.py                   # PowerUp class
├── ui.py                         # UI functions (menus, HUD)
├── Level-Editor.py               # Standalone level editor script
├── pygbag.ini                    # Configuration for the pygbag web build
├── README.md                     # This file
└── LICENSE.md                    # MIT License
```

## License

The project is under the [MIT License](LICENSE)
