# Импортируем необходимые библиотеки. 
# Вместо обычной CameraScene импортируем MovingCamera, чтобы иметь возможность
# перемещать сцену
from manimlib.imports import MovingCameraScene
from pathlib import Path
import os

# Из папки с классами импортируем наш созданный класс
from classes import HistAndFunnel

# Добавляем флаги для запуски сборки анимации
# -l (low quality)
# -s (only screenshot) 
RESOLUTION = ""
FLAGS = f"-pl {RESOLUTION}"
SCENE = "MainScene"


class MainScene(MovingCameraScene):
    # По умолчанию фон видео будет черным. Изменить текущее поведение можно
    # с помощью переменной класса "CONFIG" 
    CONFIG = {
        'camera_config': {
            'background_color': '#fff2df'
        }
    }

    def construct(self):
        """Метод construct - точка входа в создание сцены
        """
        hist = HistAndFunnel(self)
        hist.play_first_scene()


if __name__ == '__main__':
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim {script_name} {SCENE} {FLAGS}")
