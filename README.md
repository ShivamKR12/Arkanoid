# Arkanoid Fire Ball

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/Library-pygame--ce-1D9BF0?logo=pygame&logoColor=white)
![Web](https://img.shields.io/badge/Target-Web%20Game-FF5A5F)
![itch.io](https://img.shields.io/badge/Publish-itch.io-FA5C5C?logo=itch.io&logoColor=white)

</div>

A colorful arcade-style Arkanoid clone built in Python with `pygame-ce` and prepared for browser deployment with `pygbag`.

## 🎮 Features

- Classic breakout gameplay with paddle control and bouncing ball physics
- Multiple levels and difficulty modes
- Power-ups: expand, extra life, multiball, and rapid-fire gun mode
- Breakable, multi-hit, and unbreakable brick types
- Built-in level editor for creating custom layouts
- Browser-ready setup for `pygbag` and itch.io publishing

## 🧪 Local Setup

1. Clone the repo
   ```bash
   git clone https://github.com/your-user/Arkanoid.git
   cd Arkanoid
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```

   Windows:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies
   ```bash
   pip install pygame-ce pygbag
   ```

4. Run the game
   ```bash
   python main.py
   ```

5. Run the level editor
   ```bash
   python Level-Editor.py
   ```

## 🌐 Browser / itch.io Setup

This project is already structured to build as a web game using `pygbag`.

### 1) Build for the web

From the project root:

```bash
pygbag main.py
```

This generates a web build in the `build/` or exported web target folder depending on your `pygbag` version.

### 2) Test locally

Open the generated HTML or serve the build using a simple local web server.

## 🕹️ Controls

- Left / Right arrows: move paddle
- Space: shoot when gun power-up is active
- E / H: choose easy or hard difficulty on the title screen

## 🏗️ Project Structure

```text
Arkanoid/
├── main.py                  # game entry point
├── game_manager.py          # main loop and game state
├── game_objects.py          # Paddle, Ball, Brick, PowerUp classes
├── levels.py                # level loader
├── ui.py                    # in-game UI and menus
├── Level-Editor.py          # class-based editor app
├── levels/                  # level JSON files
├── assets/                  # optional sounds/images
├── pygbag.ini              # pygbag config
├── README.md                # project docs
├── LICENSE                  # licensing
└── build/                   # generated web output
```

## ✅ License

This project is released under the [MIT License](LICENSE).
