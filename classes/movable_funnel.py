from copy import deepcopy
from typing import Dict, Tuple, Union

from manimlib.imports import ApplyMethod, Scene, Transform, VGroup
from numpy import array, interp

from .funnel import Funnel
from .histogram_dot import HistogramDot


class MovableFunnelException(Exception):
    pass


class LineNotFoundException(MovableFunnelException):
    pass


class MovableFunnel(Funnel):
    """Overriden Funnel class to add 'movable' functionality"""

    _next_dot_coords: Dict[str, Union[int, float]] = {}
    dot_padding: Union[int, float] = 0.22
    animated_slowly: int = None

    def __init__(
        self,
        start_end_points: Tuple[tuple, tuple],
        run_time: Union[int, float],
        *args,
        **kwargs,
    ):
        """Class initialisation. It recieves all parameters that Funnel class needs.

        Args:
            start_end_points (Tuple[tuple, tuple]): Left top and right top points. ((x1,y1), (x2,y2)).
            run_time (Union[int, float]): How quickly we need to animate dots.
        """
        self.run_time = run_time

        super().__init__(start_end_points, *args, **kwargs)

        self._next_dots_coords = {
            "x": self.x_funnel_center,
            "y": self.y_point_bottom + (self.y_bottom_shift * 2),
        }

    def _get_next_dots_coords(
        self, dot: HistogramDot
    ) -> Union[Tuple[array, array, array], Tuple[None, None, array], Tuple[None, None, None]]:
        """Getting points for dots to move.

        Args:
            dot (HistogramDot): Dot from which we will calculate current coordinates.

        Returns:
            Union[
                Tuple[array, array, array],
                Tuple[None, None, array],
                Tuple[None, None, None,]
            ]: Tuple with the points for the next dot move (fall).
        """
        # Получаем необходимые координаты точек воронки
        current_coord = self._next_dots_coords.get("y")
        x_left_to_bottom_right = self.left_to_bottom_right.get_all_points()[-1][0]
        x_right_to_bottom_left = self.right_to_bottom_left.get_all_points()[-1][0]
        funnel_center_y = self.left_to_bottom_right.get_all_points()[-1][1] + 0.1

        point_x = dot.get_x()
        first_point = None
        second_point = None

        # Ищем линию воронки, на которую будет падать шарик
        if self.x_point_left <= point_x <= x_left_to_bottom_right:
            line = self.left_to_bottom_right

        elif x_right_to_bottom_left <= point_x <= self.x_point_right:
            line = self.right_to_bottom_left

        elif x_left_to_bottom_right < point_x < x_right_to_bottom_left:
            line = None

        else:
            return None, None, None

        if line is not None:
            # Получаем все X и Y линии
            line_x = [x[0] for x in line.get_all_points()]
            line_y = [x[1] for x in line.get_all_points()]

            # Основная магия. Интерполируем значение Y исходя из массива точек X и Y.
            point_y = interp(point_x, line_x, line_y, period=10)
            point_y += 0.25

            first_point = array([point_x, point_y, 0])

            second_point = array([self.x_funnel_center, funnel_center_y, 0])

        third_point = array([self.x_funnel_center, current_coord, 0])

        # Запоминаем текущее положение
        self._next_dots_coords["y"] = current_coord + dot.radius + self.dot_padding

        return first_point, second_point, third_point

    def drag_in_dots(self, scene: Scene, dots: VGroup, animate_slow: int, animate_rest: bool):
        """Moving dots from anywhere to the funnel.

        Args:
            scene (Scene): Scene where all our objects located.
            dots (VGroup): List od dots to move.
            animate_slow (int): How much dots we need to animate slowly.
            animate_rest (bool): Do we need to move rest of the dots or not.
        """
        if animate_slow > len(dots):
            animate_slow = len(dots)

        animated_slowly = 0
        for dot in dots[:animate_slow]:

            first_point, second_point, third_point = self._get_next_dots_coords(dot)

            if all(x is None for x in (first_point, second_point, third_point)):
                continue

            if first_point is not None:
                scene.play(ApplyMethod(dot.move_to, first_point), run_time=self.run_time)

                scene.play(ApplyMethod(dot.move_to, second_point), run_time=self.run_time)

            scene.play(ApplyMethod(dot.move_to, third_point), run_time=self.run_time)

            animated_slowly += 1

        dots_rest = deepcopy(dots[animate_slow:])

        for dot in dots_rest:
            *_, third_point = self._get_next_dots_coords(dot)
            if third_point is None:
                continue

            dot.move_to(third_point)

        if dots_rest:
            if animate_rest:
                scene.play(Transform(dots[animate_slow:], dots_rest))

            else:
                scene.add(dots_rest)

            scene.remove(dots_rest)

        self.animated_slowly = animated_slowly
