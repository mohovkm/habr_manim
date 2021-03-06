import random
from typing import Tuple, Union

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
    """Table class. Built from Lines"""

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
        """Class initialization.

        Args:
            start_end_points (Tuple[tuple, tuple]): Left top and right top points. ((x1,y1), (x2,y2)).
            row_count (int, optional): Table row count. Defaults to 0.
            row_height (Union[int, float], optional): Table row height. Defaults to 0.2.
            column_count (int, optional): Table column count. Defaults to 0.
            visible_row_count (int, optional): Table visible row count. Defaults to 0.
            columns_width (tuple, optional): Table column width. For 3 columns it looks like
                (.4, .4, .2). Defaults to None.
            lines_color (Color, optional): Table lines color. Defaults to BLACK.
            stroke_width (Union[int, float], optional): Table lines width. Defaults to 1.

        Raises:
            TableLineEmptyException: Raises when no start_end_points were passed.
        """
        if not start_end_points:
            detail = "Can't create a graph with the empty start line."
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
        """Method for creating table.

        Returns:
            VGroup: Object made from the list of lines (Line).
        """
        lines = []
        y_point = self.horizontal_line[0][1]
        y_step = self.row_height
        x_left_point = self.horizontal_line[0][0]
        x_right_point = self.horizontal_line[1][0]
        distance = abs(x_right_point - x_left_point)

        # Drawing table
        for i in range(self.row_count + 1):
            # Adding horizontal line
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

            # Adding verical lines
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
    """Overridden Table class. Custom text and dots were added."""

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
    ):
        """Class initialization.

        Args:
            start_end_points (Tuple[tuple, tuple]): Left top and right top points. ((x1,y1), (x2,y2)).
            row_count (int, optional): Table row count. Defaults to 0.
            row_height (Union[int, float], optional): Table row height. Defaults to 0.2.
            visible_row_count (int, optional): Table visible row count. Defaults to 0.
            colors (list, optional): List with dot colors. Defaults to None.
            bins (Union[int, float], optional): Count of posiible dots values.
                Defaults to 0.
            text (str, optional): Text for adding to the table. Ex "Customer"
                Defaults to "".
            start_dots_values (list, optional): List with initial values for the dots.
                Defaults to None.
        """
        self.horizontal_line = [
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
        )

    def _add_dots_and_customers_to_table(
        self,
        row_height: Union[int, float],
        row_count: int,
        columns_width: Tuple,
    ) -> Tuple[VGroup, VGroup]:
        """Method for creating dots and texts.

        Args:
            row_height (Union[int, float]): Table rows height.
            row_count (int): Table rows count.
            columns_width (Tuple): Table rows width.

        Returns:
            Tuple[VGroup, VGroup]: Tuple with all dots and texts.
        """
        customers = []
        dots = []
        y_point = self.horizontal_line[0][1]
        y_step = row_height
        x_left_point = self.horizontal_line[0][0]
        x_right_point = self.horizontal_line[1][0]
        distance = abs(x_right_point - x_left_point)
        step_x = distance * columns_width[0]

        # Adding texts and dots
        for i in range(row_count):

            # Adding text to the table
            customer = HistogramText(
                f"{self.text} {i+1}",
                color=BLACK,
            )

            # Changind text size
            customer.scale(self.text_scale)

            # Moving text to the table cell
            customer.move_to(
                array([x_left_point + 0.2, y_point - (y_step / 2), 0]),
                aligned_edge=LEFT_SIDE,  # Aligning it at the left side of the cell
            )
            customers.append(customer)

            # Forcing to generate always the same numbers
            random.seed(i + 1)

            # Adding dot value
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

            # Adding dot
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
