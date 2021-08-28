from manimlib.imports import MovingCameraScene, Dot, VGroup, BLACK, FadeIn, FadeOut
from manimlib.mobject.types.image_mobject import ImageMobject
from numpy import array
from random import randint
from .histogram_text import HistogramText
from .table import CustomersTable
from .graph import ContinuousGraph, CategoricalGraph
from .funnel import Funnel
from .movable_graph import MovableCategoricalGraph


class Scenario:
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

    def play_second_scene(self):
        table = CustomersTable(
            (
                (-2, 2),
                (2, 2)
            ),
            row_count=10,
            visible_row_count=5,
            bins=2
        )

        self.scene.play(
            FadeIn(table)
        )

        self.scene.wait(3)

    def play_third_scene(self):
        cont_graph = ContinuousGraph(
            (
                (-4, -1),
                (0, -1)
            ),
            (
                (-2, 1),
                (-2, -3)
            ),
            bins=4,
            annot=False,
        )

        cat_graph = CategoricalGraph(
            (
                (0, 2),
                (4, 2)
            ),
            None,
            bins=4,
            annot=True,
        )

        self.scene.play(
            FadeIn(cont_graph),
            FadeIn(cat_graph)
        )

        self.scene.wait(3)

    def play_fourth_scene(self):
        funnel = Funnel(
            (
                (-4, 2),
                (4, -2)
            ),
            funnels_count=3,
            point_radius=.2,
            bins=4
        )

        self.scene.play(
            FadeIn(funnel),
        )

        self.scene.wait(3)

    def play_fifth_scene(self):
        start_dot_values = [1,2,1,3,4,2,1]
        table = CustomersTable(
            (
                (-6, 2),
                (-2, 2)
            ),
            row_count=10,
            visible_row_count=8,
            bins=4,
            start_dots_values=start_dot_values
        )

        x_graph = MovableCategoricalGraph(
            (
                (0, 0),
                (4, 0)
            ),
            None,
            bins=4,
            annot=True,
        )

        self.scene.play(
            FadeIn(table),
            FadeIn(x_graph)
        )

        self.scene.wait(2)

        x_graph.drag_in_dots(
            self.scene,
            dots=table.dots,
            animate_slow=3,
            animate_rest=True
        )

        self.scene.wait(3)
