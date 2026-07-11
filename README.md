# Arkanoid Fire Ball

A modern take on the classic Arkanoid breakout game, built with Python and Pygame. This project features classic gameplay enhanced with power-ups, multiple levels, two difficulty modes, and a built-in level editor. It's also configured to be playable in a web browser using `pygbag`.

## Features

- **Classic Arkanoid Gameplay**: Break bricks, control the paddle, and keep the ball in play.
- **Multiple Levels**: Progress through increasingly challenging levels.
- **Power-ups**: Catch falling power-ups to gain advantages:
    - **Expand**: Increases the paddle size.
    - **Life**: Grants an extra life.
    - **Multiball**: Adds more balls to the screen.
    - **Gun**: Allows the paddle to shoot and destroy bricks.
- **Two Game Modes**: Choose between 'Easy' and 'Hard' to match your skill level.
- **Level Editor**: Run `Level-Editor.py` to create, edit, and save your own custom levels.
- **Web-Ready**: The included GitHub Actions workflow (`.github/workflows/pygbag.yml`) automatically builds the game for the web and deploys it to GitHub Pages.

## How to Play

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Install dependencies:**
    This project uses `pygame-ce`.
    ```bash
    pip install pygame-ce
    ```

3.  **Run the game:**
    ```bash
    python main.py
    ```

### Web Version

You can play the latest version directly in your browser on the GitHub Pages site for this repository.

## Controls

-   **Left/Right Arrow Keys**: Move the paddle.
-   **Spacebar**: Shoot bullets when the 'Gun' power-up is active.

## Level Editor Usage

Run the level editor from your terminal:
```bash
python Level-Editor.py
```

The editor provides on-screen instructions for placing different types of bricks, saving/loading levels, and switching between levels.
