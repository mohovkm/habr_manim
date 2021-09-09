from colour import Color
from manimlib.imports import BLACK, WHITE, Dot, VGroup
from numpy import array

from .histogram_text import HistogramText
from .shape_point import ShapePoint


class HistogramDot(VGroup):
    """Класс точки (шарика) Vgroup. Отличается от стандартного Dot тем, что содержит: Dot, Text и преднастраивает их."""

    colors = {
        1: "#7FCC81",  # green
        2: "#FFE236",  # yellow
        3: "#FFB742",  # orange
        4: "#FF7555",  # red
    }

    def __init__(
        self,
        value: int,
        point: array,
        radius: float = None,
        color: Color = None,
        *args, # для чего
        **kwargs,
    ):
        """Инициализация класса

        :param value: Значение (текст) шарика.
        :param point: Локация шарика на экране.
        :param radius: Радиус шарика.
        :param color: Цвет шарика.
        :param args:
        :param kwargs:
        """
        self.value = value

        if not radius:
            self.radius = 0.2

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
            text.scale(0.25)
        else:
            text.scale(0.4)

        # Двигаем текст в центр шарика
        text.move_to(dot.get_center())

        super().__init__(dot, text, *args, **kwargs) # тут соотв

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value}, {self.point}, {self.radius}, {self.color})"
