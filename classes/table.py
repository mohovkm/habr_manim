import random
from typing import List, Tuple, Union

from colour import Color
from manimlib.imports import BLACK, LEFT_SIDE, Line, VGroup
from numpy import array

from .histogram_dot import HistogramDot
from .histogram_text import HistogramText
from .shape_point import ShapePoint


class TableException(Exception):
    pass


class TableLineEmptyException(TableException):
    pass


class Table(VGroup):
    """Класс таблицы (VGroup). Таблица состоит из линий (Line)"""

    def __init__(
        self,
        start_end_points: Tuple[tuple, tuple],
        row_count: int = 0,
        row_height: Union[int, float] = 0.2,
        column_count: int = 0,
        visible_row_count: int = 0,
        columns_width: tuple = None,
        lines_color: Color = BLACK,
        stroke_width: Union[int, float] = 1,
        *args,
        **kwargs,
    ):
        """Инициализация класса таблицы

        :param start_end_points: Левая верхняя и правая верхняя точка таблицы. ((x1, y1), (x2, y2))
        :param row_count: Количество строк таблицы.
        :param row_height: Высота строк таблицы.
        :param column_count: Количество колонок таблицы.
        :param visible_row_count: Количество видимых на экране строк.
        :param columns_width: Ширина колонок. Для 3-х колонок выглядит, как (.4, .4, .2)
        :param lines_color: Цвет линий таблицы.
        :param stroke_width: Ширина линий таблицы.
        :param args:
        :param kwargs:
        """
        if not start_end_points:
            detail = "Can't create graph with empty start line."
            raise TableLineEmptyException(detail)

        if columns_width:
            assert (
                len(columns_width) == column_count
            ), "Columns count and list with they widths must be the same length."

        self.horizontal_line = [
            ShapePoint(start_end_points[0]),
            ShapePoint(start_end_points[1]),
        ]

        self.row_count = row_count
        self.row_height = row_height
        self.column_count = column_count
        self.visible_row_count = visible_row_count
        self.columns_width = columns_width
        self.lines_color = lines_color
        self.stroke_width = stroke_width

        self.lines = self._create_table()

        super().__init__(*self.lines, *args, **kwargs)

    def _create_table(self) -> VGroup:
        """Функция построения таблицы

        :return: VGroup - список из линий
        """
        lines = []
        y_point = self.horizontal_line[0][1]
        y_step = self.row_height
        x_left_point = self.horizontal_line[0][0]
        x_right_point = self.horizontal_line[1][0]
        distance = abs(x_right_point - x_left_point)

        # Рисуем таблицу
        for i in range(self.row_count + 1):
            # Добавляем горизонтальную линию
            lines.append(
                Line(
                    array([x_left_point, y_point, 0]),
                    array([x_right_point, y_point, 0]),
                    color=self.lines_color,
                    stroke_width=self.stroke_width,
                )
            )

            if i == self.row_count:
                break

            # Добавляем вертикальные линии
            x_point = x_left_point
            for j in range(self.column_count + 1):
                lines.append(
                    Line(
                        array([x_point, y_point, 0]),
                        array([x_point, y_point - y_step, 0]),
                        color=self.lines_color,
                        stroke_width=self.stroke_width,
                    )
                )

                if j == self.column_count:
                    break

                if self.columns_width:
                    temp_step = self.columns_width[j]

                    assert isinstance(temp_step, float), "Column width must be a float value"
                    assert 0 < temp_step <= 1, "Column with must be in range [0 < column_width <= 1]"

                    x_point = x_point + (distance * temp_step)
                else:
                    x_point = x_point + (distance / self.column_count)

            y_point -= y_step

        lines = VGroup(*lines)

        return lines


class CustomersTable(Table):
    """Перегрузка стандартной таблицы. Добавление текста (customers) и шариков (dots)"""

    def __init__(
        self,
        start_end_points: Tuple[tuple, tuple],
        row_count: int = 0,
        row_height: Union[int, float] = 0.5,
        visible_row_count: int = 0,
        colors: list = None,
        bins: Union[int, float] = 0,
        text: str = "",
        start_dots_values: list = None,
        *args,
        **kwargs,
    ):
        """Инициализация класса.

        :param start_end_points: Левая верхняя и правая верхняя точка таблицы. ((x1, y1), (x2, y2))
        :param row_count: Количество строк таблицы.
        :param row_height: Высота строк таблицы.
        :param column_count: Количество колонок таблицы.
        :param visible_row_count: Количество видимых на экране строк.
        :param colors: Список с цветами шариков.
        :param bins: Количество корзин (возможных значений шариков).
        :param text: ,
        :param start_dots_values: Список с начальными значениями шариков,
        :param args:
        :param kwargs:
        """

        horizontal_line = [
            ShapePoint(start_end_points[0]),
            ShapePoint(start_end_points[1]),
        ]

        self.colors = colors or list()
        self.bins = bins
        column_count = 2
        columns_width = (0.8, 0.2)
        self.text = text
        self.text_scale = 0.6
        self.start_dots_values = start_dots_values
        self.default_color = "red"

        self.customers, self.dots = self._add_dots_and_customers_to_table(
            horizontal_line=horizontal_line,
            row_count=row_count,
            row_height=row_height,
            columns_width=columns_width,
        )

        super().__init__(
            start_end_points,
            row_count,
            row_height,
            column_count,
            visible_row_count,
            columns_width,
            BLACK,
            1,
            *self.customers,
            *self.dots,
            *args,
            **kwargs,
        )

    def _add_dots_and_customers_to_table(
        self,
        horizontal_line: List[ShapePoint],
        row_height: Union[int, float],
        row_count: int,
        columns_width: Tuple,
    ) -> Tuple[VGroup, VGroup]:
        """Добавление точек в таблицу с покупателями.

        :return:
        """
        customers = []
        dots = []
        y_point = horizontal_line[0][1]
        y_step = row_height
        x_left_point = horizontal_line[0][0]
        x_right_point = horizontal_line[1][0]
        distance = abs(x_right_point - x_left_point)
        step_x = distance * columns_width[0]

        # Рисуем тексты и шарики
        for i in range(row_count):

            # Добавляем надпись "Покупатель"
            customer = HistogramText(
                f"{self.text} {i+1}",
                color=BLACK,
            )

            # Меняем размер текста
            customer.scale(self.text_scale)

            # Передвигаем текст в ячейку
            customer.move_to(
                array([x_left_point + 0.2, y_point - (y_step / 2), 0]),
                aligned_edge=LEFT_SIDE,  # Выравниваем относительно левой части объекта
            )
            customers.append(customer)

            # Настраиваем генерацию рандома
            random.seed(i + 1)

            # Добавляем значение точки (шарика)
            if self.start_dots_values and i < len(self.start_dots_values):
                dot_value = self.start_dots_values[i]
            else:
                if isinstance(self.bins, int):
                    dot_value = random.randrange(1, self.bins + 1)
                else:
                    dot_value = round(random.uniform(1.0, self.bins + 1.0), 1)

            if len(self.colors) < dot_value:
                dot_color = self.default_color
            else:
                dot_color = self.colors[int(dot_value) - 1]
            # Создаем шарик
            dot = HistogramDot(
                value=dot_value,
                point=array([x_left_point + step_x + 0.3, y_point - (y_step / 2), 0]),
                color=dot_color,
            )

            dots.append(dot)

            y_point -= y_step

        customers = VGroup(*customers)
        dots = VGroup(*dots)

        return customers, dots
