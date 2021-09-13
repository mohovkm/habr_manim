from copy import deepcopy
from random import randint

from colour import Color
from manimlib.imports import BLACK, Dot, FadeIn, FadeOut, MovingCameraScene, Transform, VGroup
from numpy import array

from classes import (
    CategoricalGraph,
    ContinuousGraph,
    CustomersTable,
    Funnel,
    HistogramText,
    MovableCategoricalGraph,
    MovableContinuousGraph,
    MovableFunnel,
)


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
        point_radius = 0.3

        for _ in range(5):
            # шарики будут располагаться один над другим, поэтому позиция Y
            # будет высчитываться динамически
            start_y = -2

            for _ in range(randint(2, 6)):
                dots.append(
                    Dot(
                        point=array([start_x, start_y, 0]),  # Координаты расположения, задаются в x,y,z плоскости
                        radius=point_radius,  # Размер шарика
                        stroke_width=1,  # Ширина обводки
                        stroke_color=BLACK,  # Цвет обводки
                        color="#7fcc81",  # Цвет шарика
                    )
                )
                start_y += 0.7
            start_x += 2

        # Группируем шарики, преобразовывая в элемент сцены VGroup
        dots = VGroup(*dots)

        # Добавляем шарики на экран
        self.scene.add(dots)

        # Создаем надпись. Для текста используем свой перегруженный класс,
        # чтобы применился необходимый нам шрифт
        heading = HistogramText("Гистограммы", color=BLACK)

        # Меняем размер текста методом scale
        heading.scale(2)

        # Перемещаем текст на позицию заголовка (чуть выше середины)
        heading.move_to(array([0, 2.5, 0]))

        # Проигрываем появление текста
        self.scene.play(FadeIn(heading))

        # Ждем 2 секунды
        self.scene.wait(2)

        # Проигрываем исчезновение точек и текста
        self.scene.play(FadeOut(dots), FadeOut(heading))

        # Ждем 1 секунду
        self.scene.wait(1)

    def play_second_scene(self):
        table = CustomersTable(((-2, 2), (2, 2)), row_count=10, visible_row_count=5, bins=2)

        self.scene.play(FadeIn(table))

        self.scene.wait(3)

    def play_third_scene(self):
        cont_graph = ContinuousGraph(
            ((-4, -1), (0, -1)),
            ((-2, 1), (-2, -3)),
            bins=4,
            annot=False,
        )

        cat_graph = CategoricalGraph(
            ((0, 2), (4, 2)),
            None,
            bins=4,
            annot=True,
        )

        self.scene.play(FadeIn(cont_graph), FadeIn(cat_graph))

        self.scene.wait(3)

    def play_fourth_scene(self):
        funnel = Funnel(((-4, 2), (4, -2)), funnels_count=3, point_radius=0.2, bins=4)

        self.scene.play(
            FadeIn(funnel),
        )

        self.scene.wait(3)

    def play_fifth_scene(self):
        # Начальные значения для точек таблицы, чтобы не было рандома
        start_dot_values = [1, 2, 1, 3, 4, 2, 1]

        # Инициализируем таблицу
        table = CustomersTable(
            ((-6, 2), (-2, 2)),
            row_count=10,
            visible_row_count=8,
            bins=4,
            start_dots_values=start_dot_values,
        )

        # Инициализируем график
        x_graph = MovableCategoricalGraph(
            ((0, 0), (4, 0)),
            None,
            bins=4,
            annot=True,
        )

        # Добавляем на экран таблицу и график
        self.scene.play(FadeIn(table), FadeIn(x_graph))

        self.scene.wait(2)

        # Перемещаем точки из таблицы на график
        x_graph.drag_in_dots(self.scene, dots=table.dots, animate_slow=3, animate_rest=True)

        self.scene.wait(3)

    def play_whole_scenario(self):
        # Выставляем значения шариков
        bins = 100

        # Добавляем цвета для значений шариков
        dot_colors = list(Color("#7fcc81").range_to("#ff7555", int(bins)))

        # Определяем, с каких значений начинать таблицу
        start_dots_values = [76, 12, 10, 25, 49, 99, 16, 33, 37]

        # Текст в таблице (Заказчик/Покупатель...)
        table_text = "Заказчик"

        # Инициализируем таблицу
        table = CustomersTable(
            ((-6.5, 3), (-2.5, 3)),
            row_count=40,
            visible_row_count=11,
            bins=bins,
            colors=dot_colors,
            start_dots_values=start_dots_values,
            text=table_text,
        )

        # Инициализируем график
        x_graph = MovableContinuousGraph(
            ((-2, -3), (6.5, -3)),
            None,
            bins=bins,
            annot=True,
        )

        # Добавляем второй график (на всю ширину экрана)
        x_graph_second_position = MovableContinuousGraph(
            ((-6.5, -3), (6.5, -3)),
            None,
            bins=bins,
            annot=True,
        )

        # Копируем все шарики (необходимо для дальнейших преобразований)
        dots_second_position = deepcopy(table.dots)

        # Добавляем на экран таблицу и первый график
        self.scene.play(FadeIn(table), FadeIn(x_graph))

        self.scene.wait(2)

        # Перемещаем точки из таблицы на график
        x_graph.drag_in_dots(
            self.scene,
            dots=table.dots,
            animate_slow=3,
            animate_rest=True,
        )

        self.scene.wait(3)

        # Убираем с экрана таблицу с покупателями
        self.scene.play(FadeOut(table.lines), FadeOut(table.customers))

        # Перемещаем шарики из 1-го графика во 2-й график
        x_graph_second_position.drag_in_dots(
            scene=self.scene,
            dots=dots_second_position,
            animate_slow=0,
            animate_rest=False,
        )

        # Перемещаем на экране график1 в график2 и шарики1 в шарики2
        self.scene.play(
            Transform(x_graph, x_graph_second_position),
            Transform(table.dots, dots_second_position),
        )

        self.scene.wait(3)

        # Создаем объект с воронками
        funnels = MovableFunnel(
            run_time=0.8,
            left_top_and_right_bottom_points=((-6.5, -4), (6.5, -8.5)),
            funnels_count=5,
            point_radius=0.2,
            bins=bins,
        )

        # Показываем воронки на экране
        self.scene.add(funnels)

        # Перемещаем камеру вниз (график уходит вверх)
        self.scene.play(self.scene.camera_frame.move_to, array([0, -5.5, 0]))

        self.scene.wait(1)

        # Перемещаем шарики с графика в воронки
        funnels.drag_in_dots(scene=self.scene, dots=table.dots, animate_slow=9, animate_rest=True)

        self.scene.wait(3)

        # Удаляем со сцены объекты
        self.scene.play(
            FadeOut(funnels),
            FadeOut(table.dots),
            FadeOut(x_graph),
            FadeOut(x_graph_second_position),
        )

        # Возвращаем сцену на предыдущее место
        self.scene.play(self.scene.camera_frame.move_to, array([0, 0, 0]))

        self.scene.wait(1)
