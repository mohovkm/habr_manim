# Manimlib animation examples [manimlib](https://github.com/3b1b/manim)
![final scenario](final_scenario.gif)

### How to run it on your local machine:
1. Install [poetry](https://python-poetry.org/)

2. Install dependencies

MacOS: Install **ffmpeg** and **mactex** 
```bash
brew install ffmpeg mactex
```

OPTIONAL: For MacOS [cairo](https://formulae.brew.sh/formula/cairo) library might also be needed, so install it with brew:
```bash
brew install cairo
```

Linux (Ubuntu/Mint) Install **cairo**
```bash
sudo apt-get install libcairo2-dev
```

3. Compile and run your project
```bash
cd habr_manim/
poetry install
poetry run python main.py
```

### Explanation
- main.py - entry point for the animation
- scenario.py - examples of different scenes with custom classes
- classes/\*.py - custom classes of different objects (table, dot, graph, etc).
