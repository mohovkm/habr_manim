from manimlib.imports import MovingCameraScene, Dot, VGroup, BLACK, FadeIn, FadeOut, Transform
from numpy import array
from random import randint
from .histogram_text import HistogramText


class HistAndFunnel:
    def __init__(self, scene: MovingCameraScene):
        self.scene = scene
    
    def play_first_scene(self):
        # Для начала создадим шарики и сохраним в переменной 
        dots = []

        # Столбики с шариками будут располагаться один за другим, поэтому позиция X
        # будет высчитываться динамически 
        start_x = -4


        # Задаем размер шарика
        point_radius = .3

        for _ in range(5):        
            # шарики будут располагаться один над другим, поэтому позиция Y
            # будет высчитываться динамически 
            start_y = -2

            for _ in range(randint(2, 6)):
                dots.append(
                    Dot(
                        point=array([start_x, start_y, 0]), # Координаты расположения, задаются в x,y,z плоскости
                        radius=point_radius, # Размер шарика
                        stroke_width=1,      # Ширина обводки
                        stroke_color=BLACK,  # Цвет обводки
                        color="#7fcc81"      # Цвет шарика
                    )
                )
                start_y += .7
            start_x += 2

        # Группируем шарики, преобразовывая в элемент сцены VGroup
        dots = VGroup(*dots)

        # Добавляем шарики на экран
        self.scene.add(dots)

        # Создаем надпись. Для текста используем свой перегруженный класс,
        # чтобы применился необходимый нам шрифт 
        heading = HistogramText(
            "Гистограммы",
            color=BLACK
        )

        # Меняем размер текста методом scale
        heading.scale(2)

        # Перемещаем текст на позицию заголовка (чуть выше середины)
        heading.move_to(array([0, 2.5, 0]))

        # Проигрываем появление текста
        self.scene.play(FadeIn(heading))

        # Ждем 2 секунды
        self.scene.wait(2)

        # Проигрываем исчезновение точек и текста
        self.scene.play(
            FadeOut(dots),
            FadeOut(heading)
        )

        # Ждем 1 секунду
        self.scene.wait(1)
