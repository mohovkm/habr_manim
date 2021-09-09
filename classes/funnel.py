import logging
from typing import Tuple, Union

from colour import Color
from manimlib.imports import BLACK, Line, VGroup
from numpy import arange, array

from .histogram_text import HistogramText
from .shape_point import ShapePoint

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class FunnelException(Exception):
    pass

### класс воронки или воронок? Абстракция
class Funnel(VGroup):
    """Класс VGroup для получения воронки (Воронка состоит из линий(Line))"""

    def __init__(
        self,
        left_top_and_right_bottom_points: Tuple[tuple],
        funnels_count: int,
        point_radius: Union[float, int],
        bins: int,
        annot: bool = True,
        lines_color: Color = BLACK,
        stroke_width: Union[int, float] = 1,
        *args,
        **kwargs,
    ):
        """Инициализация воронки.

        :param left_top_and_right_bottom_points: Левая верхняя точки и правая нижняя, соответственно. ((x1,y1), (x2,y2))
        :param funnels_count: Количество воронок, которые нужно нарисовать
        :param point_radius: Радиус шарика. Нужен для того, чтобы понять, какой шириниы должно быть горлышко воронки.
        :param bins: Количество корзин на все воронки. Нужно для расчитывания диапазона значения каждой воронки.
        :param annot: Подписывать воронки или нет.
        :param lines_color: Цвет линий воронок.
        :param stroke_width: Толщина линий воронок.
        :param args:
        :param kwargs:
        """

        self.left_top_point = ShapePoint(left_top_and_right_bottom_points[0])
        self.right_bottom_point = ShapePoint(left_top_and_right_bottom_points[1])
        self.funnels_count = funnels_count
        self._point_in_funnels = []
        self.point_radius = point_radius
        self.y_bottom_shift = 0.2
        self.bins = bins
        self.annot = annot
        self.text_scale = 0.6
        self.lines_color = lines_color
        self.stroke_width = stroke_width
        self.step = abs(self.left_top_point[0] - self.right_bottom_point[0]) / self.funnels_count

        self.funnels, self.texts = self.create_funnels()

        super().__init__(*self.funnels, *self.texts, *args, **kwargs)

    def create_funnels(self) -> Tuple[list, list]:
        """Метод строит список из воронок, где каждая из воронок является списком(VGroup) из линий.
        [[line1,line2...]...]

        :return:
        """

        for _ in range(self.funnels_count):
            self._point_in_funnels.append([])

        radius = self.point_radius * 3
        funnels = []
        texts = []
        y_point_top = self.left_top_point[1]
        y_point_bottom = self.right_bottom_point[1]
        x_point_left = self.left_top_point[0]
        x_point_right = self.right_bottom_point[0]
        annot_step = int(self.bins / self.funnels_count)
        annot_bins = [i for i in range(0, int(self.bins) + annot_step, annot_step)]
        annots = [f"{x+1}–{y}" for x, y in zip(annot_bins[:-1], annot_bins[1:])]

        # Рисуем воронки
        for step, i in enumerate(arange(x_point_left, x_point_right, self.step)):
            roof_length = (self.step - radius) / 2

            left_to_top = Line(
                array([i, y_point_bottom, 0]),
                array([i, y_point_top, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            left_to_bottom_right = Line(
                array([i, y_point_top, 0]),
                array([i + roof_length, y_point_top - 0.5, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            right_to_top = Line(
                array([i + self.step, y_point_bottom, 0]),
                array([i + self.step, y_point_top, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            right_to_bottom_left = Line(
                array([i + self.step, y_point_top, 0]),
                array([i + self.step - roof_length, y_point_top - 0.5, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            left_funnel_appendix = Line(
                array([i + roof_length, y_point_top - 0.5, 0]),
                array([i + roof_length, y_point_top - 0.7, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            right_funnel_appendix = Line(
                array([i + self.step - roof_length, y_point_top - 0.5, 0]),
                array([i + self.step - roof_length, y_point_top - 0.7, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )

            funnel = VGroup(
                *[
                    left_to_top,
                    right_to_top,
                    left_to_bottom_right,
                    right_to_bottom_left,
                    left_funnel_appendix,
                    right_funnel_appendix,
                ]
            )

            text = HistogramText(annots[step], color=self.lines_color)
            text.move_to(array([i + (self.step / 2), y_point_bottom - 0.3, 0]))
            text.scale(self.text_scale)

            texts.append(text)
            funnels.append(funnel)

        # Добавляем горизонтальную линию
        funnels.append(
            Line(
                array([x_point_left - 0.2, y_point_bottom + self.y_bottom_shift, 0]),
                array([x_point_right + 0.2, y_point_bottom + self.y_bottom_shift, 0]),
                color=self.lines_color,
                stroke_width=self.stroke_width,
            )
        )

        return funnels, texts
