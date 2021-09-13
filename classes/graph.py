from abc import ABC, abstractmethod
from typing import Tuple

from manimlib.imports import BLACK, Line, VGroup
from numpy import array

from .histogram_text import HistogramText
from .shape_point import ShapePoint


class GraphException(Exception):
    pass


class GraphLinesEmptyException(GraphException):
    pass


class Graph(ABC):
    """Класс для получения и отрисовки графика (график состоит из линий(Line))"""

    bins: int
    color: str
    annot: bool
    text_scale: float = 0.6
    dot_padding: float = 0.25
    stroke_width: float

    def __init__(
        self,
        horizontal_line: Tuple[tuple, tuple] = None,
        vertical_line: Tuple[tuple, tuple] = None,
        bins: int = 1,
        annot: bool = False,
        color=BLACK,
        stroke_width=1,
    ):
        """

        :param horizontal_line: Координаты горизонтальной линии ((x1, y1), (x2, y2)).
        :param vertical_line: Координаты вертикальной линии ((x1, y1), (x2, y2)).
        :param bins: Количество корзин на графике.
        :param annot: Подписывать корзины или нет.
        :param color: Цвет линий графика.
        :param stroke_width: Ширина линий графика.
        """
        if not horizontal_line and not vertical_line:
            detail = "Can't create graph with empty lines."
            raise GraphLinesEmptyException(detail)

        # Initialise graph lines
        self.horizontal_line = None
        if horizontal_line:
            self.horizontal_line = [
                ShapePoint(horizontal_line[0]),
                ShapePoint(horizontal_line[1]),
            ]
            self.step_x = abs(horizontal_line[0][0] - horizontal_line[1][0]) / bins

        self.vertical_line = None
        if vertical_line:
            self.vertical_line = [
                ShapePoint(vertical_line[0]),
                ShapePoint(vertical_line[1]),
            ]
            self.step_y = abs(vertical_line[0][1] - vertical_line[1][1]) / bins

        self.bins = bins
        self.color = color
        self.annot = annot
        self.stroke_width = stroke_width

        lines, texts = self.create_graph()

        super().__init__(*lines, *texts)

    def _prepare_next_dot_coords(self) -> dict:
        """Подготовка словаря с информацией о серединах корзин на графике.

        :return: dict
        """
        d = {}
        start_x = self.horizontal_line[0][0]
        for i in range(1, int(self.bins) + 1):
            d[i] = {
                "x": start_x + (self.step_x / 2),
                "y": self.horizontal_line[0][1] + 0.25,
            }
            start_x += self.step_x

        return d

    @abstractmethod
    def create_graph(self) -> Tuple[list, list]:
        pass


class CategoricalGraph(Graph, VGroup):
    """Категориальный тип графика (VGroup) (Наследуется от Graph)"""

    def create_graph(self) -> Tuple[list, list]:
        """Создание графика

        :return: lines, texts (список из линий графика и текста аннотации)
        """
        lines = []
        texts = []

        if self.horizontal_line:
            # Добавляем горизонтальную линию
            line = Line(
                self.horizontal_line[0].coords,
                self.horizontal_line[1].coords,
                color=self.color,
                stroke_width=self.stroke_width,
            )

            lines.append(line)

            # Рисуем вертикальные линии
            start_x = self.horizontal_line[0].coords[0]
            y_coord = self.horizontal_line[0].coords[1]
            for i in range(1, self.bins + 2):
                lines.append(
                    Line(
                        array([start_x, y_coord + 0.3, 0]),
                        array([start_x, y_coord - 0.3, 0]),
                        color=self.color,
                        stroke_width=self.stroke_width,
                    )
                )

                # Добавляем надписи для корзин
                if self.annot and (i != self.bins + 1):
                    text = HistogramText(str(i), color=BLACK)
                    text.scale(self.text_scale)
                    text.move_to(array([start_x + (self.step_x / 2), y_coord - 0.3, 0]))
                    texts.append(text)

                start_x += self.step_x

            if self.vertical_line:
                # Добавляем вертикальную линию
                line = Line(
                    self.vertical_line[0].coords,
                    self.vertical_line[1].coords,
                    color=self.color,
                    stroke_width=self.stroke_width,
                )

                lines.append(line)

                # Рисуем горизонтальные линии
                start_y = self.vertical_line[0].coords[1]
                x_coord = self.vertical_line[0].coords[0]

                for i in range(1, self.bins + 2):
                    lines.append(
                        Line(
                            array([x_coord - 0.3, start_y, 0]),
                            array([x_coord + 0.3, start_y, 0]),
                            color=self.color,
                            stroke_width=self.stroke_width,
                        )
                    )

                    if self.annot and (i != self.bins + 1):
                        text = HistogramText(str(i), color=BLACK)
                        text.scale(self.text_scale)
                        text.move_to(array([x_coord - 0.3, start_y - (self.step_y / 2), 0]))
                        texts.append(text)

                    start_y -= self.step_y

        return texts, lines


class ContinuousGraph(Graph, VGroup):
    """Непрерывный тип графика (VGroup) (Наследуется от Graph)"""

    def create_graph(self) -> Tuple[list, list]:
        """Создание графика

        :return: lines, texts (список из линий графика и текста аннотации)
        """
        lines = []
        texts = []

        if self.horizontal_line:
            # Добавляем горизонтальную линию
            lines.append(
                Line(
                    self.horizontal_line[0].coords,
                    self.horizontal_line[1].coords,
                    color=self.color,
                    stroke_width=self.stroke_width,
                )
            )

            y_coord = self.horizontal_line[0].coords[1]
            # Добавляем 2 вертикальные линии
            lines.extend(
                [
                    Line(
                        array([self.horizontal_line[0].coords[0], y_coord + 0.3, 0]),
                        array([self.horizontal_line[0].coords[0], y_coord - 0.3, 0]),
                        color=self.color,
                        stroke_width=self.stroke_width,
                    ),
                    Line(
                        array([self.horizontal_line[1].coords[0], y_coord + 0.3, 0]),
                        array([self.horizontal_line[1].coords[0], y_coord - 0.3, 0]),
                        color=self.color,
                        stroke_width=self.stroke_width,
                    ),
                ]
            )

            if self.annot:
                text0 = HistogramText(str(0), color=BLACK)
                text0.scale(self.text_scale)
                text0.move_to(array([self.horizontal_line[0].coords[0], y_coord - 0.55, 0]))

                text1 = HistogramText(str(self.bins), color=BLACK)
                text1.scale(self.text_scale)
                text1.move_to(array([self.horizontal_line[1].coords[0], y_coord - 0.55, 0]))
                texts.extend([text0, text1])

        if self.vertical_line:
            # Добавляем вертикальную линию
            lines.append(
                Line(
                    self.vertical_line[0].coords,
                    self.vertical_line[1].coords,
                    color=self.color,
                    stroke_width=self.stroke_width,
                )
            )

            x_coord = self.vertical_line[0].coords[0]
            # Добавляем 2 горизонтальные линии
            lines.extend(
                [
                    Line(
                        array([x_coord - 0.3, self.vertical_line[0].coords[1], 0]),
                        array([x_coord + 0.3, self.vertical_line[0].coords[1], 0]),
                        color=self.color,
                        stroke_width=self.stroke_width,
                    ),
                    Line(
                        array([x_coord - 0.3, self.vertical_line[1].coords[1], 0]),
                        array([x_coord + 0.3, self.vertical_line[1].coords[1], 0]),
                        color=self.color,
                        stroke_width=self.stroke_width,
                    ),
                ]
            )

            if self.annot:
                text0 = HistogramText(str(0), color=BLACK)
                text0.scale(self.text_scale)
                text0.move_to(array([x_coord - 0.55, self.vertical_line[0].coords[1], 0]))

                text1 = HistogramText(str(self.bins), color=BLACK)
                text1.scale(self.text_scale)
                text1.move_to(array([x_coord - 0.55, self.vertical_line[1].coords[1], 0]))
                texts.extend([text0, text1])

        return lines, texts
