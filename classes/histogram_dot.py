from typing import Dict, Union

from colour import Color
from manimlib.imports import BLACK, WHITE, Dot, VGroup
from numpy import ndarray

from .histogram_text import HistogramText
from .shape_point import ShapePoint


class HistogramDot(VGroup):
    """This class contains Dot, Text and all needed info that we want, such as 'value'"""

    colors: Dict[int, str] = {
        1: "#7FCC81",  # green
        2: "#FFE236",  # yellow
        3: "#FFB742",  # orange
        4: "#FF7555",  # red
    }

    dot_scale_float: Union[int, float] = 0.25
    dot_scale_int: Union[int, float] = 0.4
    radius: Union[int, float] = 0.2

    def __init__(
        self,
        value: int,
        point: ndarray,
        radius: float = None,
        color: Color = None,
    ):
        """Class initialisation.

        Args:
            value (int): Text of the dot.
            point (array): Location on the screen.
            radius (float, optional): Dot radius. Defaults to None.
            color (Color, optional): Dot color. Defaults to None.
        """
        self.value = value

        self.radius = radius or self.radius

        if not color:
            color = self.colors.get(value, WHITE)

        dot = Dot(
            point=point,  # Координаты на плоскости
            radius=self.radius,  # Радиус шарика
            color=color,  # Цвет шарика
            stroke_color=BLACK,  # Цвет границы
            stroke_width=1,  # Ширина границы
        )
        text = HistogramText(str(self.value), color=BLACK)

        self.point = ShapePoint(point)

        # Меняем размер текста, чтобы влез в шарик
        if isinstance(self.value, float):
            text.scale(self.dot_scale_float)
        else:
            text.scale(self.dot_scale_int)

        # Двигаем текст в центр шарика
        text.move_to(dot.get_center())

        super().__init__(dot, text)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value}, {self.point}, {self.radius}, {self.color})"
