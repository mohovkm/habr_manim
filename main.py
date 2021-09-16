import os
from pathlib import Path

# We are importing MovingCamera, instead of CameraScene to be albe to
# move camera around.
from manimlib.imports import MovingCameraScene

from config import SCENE_BACKGROUND_COLOR
from scenario import Scenario

# Adding flags to build animation.
# -l (low quality)
# -s (only screenshot)
RESOLUTION = ""
FLAGS = f"-pl {RESOLUTION}"
SCENE = "MainScene"


class MainScene(MovingCameraScene):
    # Scene background is black by default, to change it we need to
    # override CONFIG dictionary.
    CONFIG = {
        "camera_config": {
            "background_color": SCENE_BACKGROUND_COLOR,
        },
    }

    def construct(self):
        """Метод construct - точка входа в создание сцены"""
        hist = Scenario(self)
        # hist.play_first_scene()
        # hist.play_second_scene()
        # hist.play_third_scene()
        # hist.play_fourth_scene()
        # hist.play_fifth_scene()
        # hist.play_sixth_scene()
        hist.play_whole_scenario()


if __name__ == "__main__":
    script_name = Path(__file__).resolve()
    os.system(f"manim {script_name} {SCENE} {FLAGS}")
