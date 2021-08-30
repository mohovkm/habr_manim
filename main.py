# Импортируем необходимые библиотеки.
# Вместо обычной CameraScene импортируем MovingCamera, чтобы иметь возможность
# перемещать сцену
import os
from pathlib import Path

from manimlib.imports import MovingCameraScene

# Из папки с классами импортируем наш созданный класс
from classes import Scenario

# Добавляем флаги для запуски сборки анимации
# -l (low quality)
# -s (only screenshot)
RESOLUTION = ""
FLAGS = f"-pl {RESOLUTION}"
SCENE = "MainScene"


class MainScene(MovingCameraScene):
    # По умолчанию фон видео будет черным. Изменить текущее поведение можно
    # с помощью переменной класса "CONFIG"
    CONFIG = {"camera_config": {"background_color": "#fff2df"}}

    def construct(self):
        """Метод construct - точка входа в создание сцены"""
        hist = Scenario(self)
        # hist.play_first_scene()
        # hist.play_second_scene()
        # hist.play_third_scene()
        # hist.play_fourth_scene()
        # hist.play_fifth_scene()
        hist.play_whole_scenario()


if __name__ == "__main__":
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim {script_name} {SCENE} {FLAGS}")
