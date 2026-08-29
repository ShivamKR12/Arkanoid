<div align="center">

# Arkanoid Fire Ball

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/Library-pygame--ce-1D9BF0?logo=pygame&logoColor=white)
![Web](https://img.shields.io/badge/Target-Web%20Game-FF5A5F)
![itch.io](https://img.shields.io/badge/Publish-itch.io-FA5C5C?logo=itch.io&logoColor=white)
[![Build Web Game](https://github.com/ShivamKR12/Arkanoid/actions/workflows/pygbag.yml/badge.svg)](https://github.com/ShivamKR12/Arkanoid/actions/workflows/pygbag.yml)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

A colorful arcade-style Arkanoid clone built in Python with `pygame-ce` and prepared for browser deployment with `pygbag`.

<div align="center">
  <img src="screenshots/0.png" alt="Gameplay Screenshot" width="600">
</div>

## 🚀 Features

*   Classic breakout gameplay with paddle control and bouncing ball physics.
*   Multiple levels and difficulty modes.
*   Power-ups: expand, extra life, multiball, and rapid-fire gun mode.
*   Breakable, multi-hit, and unbreakable brick types.
*   Built-in level editor for creating custom layouts.
*   Browser-ready setup for `pygbag` and itch.io publishing.

## 🎮 Getting Started

You can easily play the game directly in your browser. No download required!

*   **GitHub Pages:** Play the game at [shivamkr12.github.io/Arkanoid](https://shivamkr12.github.io/Arkanoid/).
*   **itch.io:** (Page coming soon!)

## 🕹️ How to Play

*   **Left / Right arrows:** Move your paddle.
*   **Spacebar:** Shoot when the gun power-up is active.
*   **E / H:** Choose easy or hard difficulty on the title screen.

## 🛠️ Building From Source

If you want to build the game yourself, you'll need Python 3 and some dependencies.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ShivamKR12/Arkanoid.git
    cd Arkanoid
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `.\venv\Scripts\Activate.ps1`
    ```

3.  **Install dependencies:**
    ```sh
    pip install pygame-ce pygbag
    ```

4.  **Run the game:**
    ```sh
    python main.py
    ```

5.  **Run the level editor:**
    ```sh
    python Level-Editor.py
    ```

6.  **Build for the web:**
    This project is already structured to build as a web game using `pygbag`.
    ```sh
    pygbag main.py
    ```
    This generates a web build in the `build/` folder.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
