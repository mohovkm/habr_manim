from copy import deepcopy
from typing import Union

from manimlib.imports import ApplyMethod, Scene, Transform, VGroup
from numpy import arange, array, interp

from .funnel import Funnel
from .histogram_dot import HistogramDot


class MovableFunnelException(Exception):
    pass


class LineNotFoundException(MovableFunnelException):
    pass


class MovableFunnel(Funnel):
    """Класс для взаимодействия воронки с шариками"""

    def __init__(self, run_time: Union[int, float], *args, **kwargs):
        """Инициализация класса. Список всех необходимых параметров смотри в методе __init__ класса Funnel.

        :param run_time: Время - насколько быстро анимировать падение шариков.
        :param args:
        :param kwargs:
        """

        self.run_time = run_time

        super().__init__(*args, **kwargs)

    def _get_next_dots_coords(self, point: HistogramDot) -> tuple:
        """Получение точек для падения шарика.

        :param point: Точка, из которой высчитываем координаты
        :return:
        """
        point_x = point.get_x()
        x_point_left = self.left_top_point[0]
        x_point_right = self.right_bottom_point[0]

        index = None
        for i, val in enumerate(arange(x_point_left, x_point_right, self.step)):
            if val <= point_x <= (val + self.step):
                index = i
                break

        if index is None:
            raise LineNotFoundException("Line index was not found")

        funnel = self.funnels[index]
        line_left_x_start = funnel[2].get_points()[0][0]
        line_left_x_end = funnel[2].get_points()[-1][0]
        line_right_x_start = funnel[3].get_points()[-1][0]
        line_right_x_end = funnel[3].get_points()[0][0]
        funnel_center_x = line_left_x_end + point.radius + (point.radius / 2)
        funnel_center_y = funnel[2].get_all_points()[-1][1] + 0.1
        funnel_last_point = self._point_in_funnels[index]

        if len(funnel_last_point) > 0:
            funnel_bottom_y = funnel_last_point[-1][1]
            funnel_bottom_y += (point.radius * 2) + 0.05
        else:
            funnel_bottom_y = funnel[0].get_all_points()[0][1]
            funnel_bottom_y += self.y_bottom_shift + point.radius + 0.05

        if line_left_x_start <= point_x <= line_left_x_end:
            line = funnel[2]
        elif line_right_x_start <= point_x <= line_right_x_end:
            line = funnel[3]
        else:
            line = None

        first_point = None
        second_point = None

        if line is not None:
            line_x = [x[0] for x in line.get_all_points()]
            line_y = [x[1] for x in line.get_all_points()]

            # Основная магия. Интерполируем значение Y исходя из массива точек X и Y.
            point_y = interp(point_x, line_x, line_y, period=10)
            point_y += 0.25

            first_point = array([point_x, point_y, 0])

            second_point = array([funnel_center_x, funnel_center_y, 0])

        third_point = array([funnel_center_x, funnel_bottom_y, 0])

        self._point_in_funnels[index].append(third_point)

        return first_point, second_point, third_point

    def drag_in_dots(self, scene: Scene, dots: VGroup, animate_slow: int, animate_rest: bool):
        """Перемещение (падение) точек в воронку.

        :param scene: Сцена, на которой необходимо показывать перемещение объектов.
        :param dots: Список из точек (шариков).
        :param animate_slow: Количество точек (шариков), которые нужно медленно и красиво переместить.
        :param animate_rest: Анимировать перемещение остальных точек (шариков) или нет.
        :return: None
        """
        if animate_slow > len(dots):
            animate_slow = len(dots)

        for dot in dots[:animate_slow]:
            first_point, second_point, third_point = self._get_next_dots_coords(dot)

            if first_point is not None:
                scene.play(ApplyMethod(dot.move_to, first_point), run_time=self.run_time)

                scene.play(ApplyMethod(dot.move_to, second_point), run_time=self.run_time)

            scene.play(ApplyMethod(dot.move_to, third_point), run_time=self.run_time)

        dots_rest = deepcopy(dots[animate_slow:])

        for dot in dots_rest:
            *_, third_point = self._get_next_dots_coords(dot)
            dot.move_to(third_point)

        if animate_rest:
            scene.play(Transform(dots[animate_slow:], dots_rest))

        else:
            scene.add(dots_rest)

        scene.remove(dots_rest)
