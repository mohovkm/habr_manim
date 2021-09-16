from typing import Tuple, Union

from colour import Color
from manimlib.imports import BLACK, Line, VGroup
from numpy import array, mean

from .histogram_text import HistogramText
from .shape_point import ShapePoint


class Funnel(VGroup):
    text_scale: Union[int, float] = 0.6

    def __init__(
        self,
        start_end_points: Tuple[tuple, tuple],
        height: Union[int, float],
        point_radius: Union[int, float],
        annot: bool = False,
        annot_text: str = "",
        lines_color: Color = BLACK,
        stroke_width: Union[int, float] = 1,
    ):
        """Funnel initialisation.

        Args:
            start_end_points (Tuple[tuple, tuple]): Left top and right top points. ((x1,y1), (x2,y2)).
            height (Union[int, float]): Funnel height.
            point_radius (Union[int, float]): Point radius. With that value we could calculate the opening
                of the funnel.
            annot (bool, optional): Do we need to annotate funnel or not. Defaults to False.
            annot_text (str, optional): Text to annotate funnel. Defaults to "".
            lines_color (Color, optional): Lines color for the funnel. Defaults to BLACK.
            stroke_width (Union[int, float], optional): Line width for the funnel. Defaults to 1.
        """
        self.left_top_point = ShapePoint(start_end_points[0])
        self.right_top_point = ShapePoint(start_end_points[1])

        self.height = height
        self.point_radius = point_radius
        self.point_diameter = point_radius * 1.5
        self.lines_color = lines_color
        self.stroke_width = stroke_width
        self.annot = annot
        self.annot_text = annot_text

        self.y_point_top = self.left_top_point[1]
        self.y_point_bottom = self.y_point_top - self.height
        self.x_point_left = self.left_top_point[0]
        self.x_point_right = self.right_top_point[0]
        self.y_bottom_shift = 0.2

        self.x_funnel_center = mean(array([self.right_top_point[0], self.left_top_point[0]]))

        self.left_to_bottom = Line(
            array([self.x_point_left, self.y_point_top, 0]),
            array([self.x_point_left, self.y_point_bottom, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.left_to_bottom_right = Line(
            array([self.x_point_left, self.y_point_top, 0]),
            array([self.x_funnel_center - self.point_diameter, self.y_point_top - 0.5, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.right_to_bottom = Line(
            array([self.x_point_right, self.y_point_top, 0]),
            array([self.x_point_right, self.y_point_bottom, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.right_to_bottom_left = Line(
            array([self.x_point_right, self.y_point_top, 0]),
            array([self.x_funnel_center + self.point_diameter, self.y_point_top - 0.5, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.left_funnel_appendix = Line(
            array([self.x_funnel_center + self.point_diameter, self.y_point_top - 0.5, 0]),
            array([self.x_funnel_center + self.point_diameter, self.y_point_top - 0.7, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.right_funnel_appendix = Line(
            array([self.x_funnel_center - self.point_diameter, self.y_point_top - 0.5, 0]),
            array([self.x_funnel_center - self.point_diameter, self.y_point_top - 0.7, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        self.bottom_line = Line(
            array([self.x_point_left - 0.2, self.y_point_bottom + self.y_bottom_shift, 0]),
            array([self.x_point_right + 0.2, self.y_point_bottom + self.y_bottom_shift, 0]),
            color=self.lines_color,
            stroke_width=self.stroke_width,
        )

        texts = []
        if annot:
            text = HistogramText(annot_text, color=self.lines_color)
            text.move_to(array([self.x_funnel_center, self.y_point_bottom, 0]))
            text.scale(self.text_scale)
            texts.append(text)

        super().__init__(
            self.left_to_bottom,
            self.right_to_bottom,
            self.left_to_bottom_right,
            self.right_to_bottom_left,
            self.left_funnel_appendix,
            self.right_funnel_appendix,
            self.bottom_line,
            *texts,
        )
