from abc import ABC
from copy import deepcopy
from typing import Dict, Union

from manimlib.imports import DEFAULT_ANIMATION_RUN_TIME, ApplyMethod, Scene, Transform, VGroup
from numpy import array, ndarray

from .graph import CategoricalGraph, ContinuousGraph
from .histogram_dot import HistogramDot


class Movable(ABC):
    """Abstract class to add 'movable' functionality to the granp"""

    _next_dot_coords: Dict[Union[int, float], Dict[str, Union[int, float]]] = {}
    dot_padding: Union[int, float] = 0

    def __init__(self, *args, **kwargs):
        self._next_dots_coords = self._prepare_next_dot_coords()

        super().__init__(*args, **kwargs)

    def _get_next_dot_coords(self, dot: HistogramDot) -> ndarray:
        """Getting points for dots to move.

        Args:
            dot (HistogramDot): Dot from which we will calculate current coordinates.

        Returns:
            array: Next dot location.
        """
        current_coord = self._next_dots_coords.get(int(dot.value), {})
        bin_center = array([current_coord.get("x", 0), current_coord.get("y", 0), 0])

        self._next_dots_coords[int(dot.value)]["y"] = current_coord.get("y", 0) + dot.radius + self.dot_padding

        return bin_center

    def drag_in_dots(
        self,
        scene: Scene,
        dots: VGroup,
        animate_slow: int,
        animate_rest: bool,
        run_time: Union[int, float] = None,
        delay: Union[int, float] = None,
    ):
        """Перемещение шариков на график.

        Args:
            scene (Scene): Scene where all our objects located.
            dots (VGroup): List od dots to move.
            animate_slow (int): How much dots we need to animate slowly.
            animate_rest (bool): Do we need to move rest of the dots or not.
            run_time (Union[int, float]): How quickly we need to animate dots. Defaults to None.
            delay (Union[int, float], optional): Delay between animations. Defaults to None.
        """
        if not run_time:
            run_time = DEFAULT_ANIMATION_RUN_TIME

        for dot in dots[:animate_slow]:
            scene.play(
                ApplyMethod(dot.move_to, self._get_next_dot_coords(dot)),
                run_time=run_time,
            )

            if delay:
                scene.wait(delay)

        if animate_rest:
            dots_rest = deepcopy(dots[animate_slow:])

            for dot in dots_rest:
                dot.move_to(self._get_next_dot_coords(dot))

            scene.play(Transform(dots[animate_slow:], dots_rest))

            scene.remove(dots[animate_slow:])

        else:
            for dot in dots[animate_slow:]:
                dot.move_to(self._get_next_dot_coords(dot))


class MovableContinuousGraph(ContinuousGraph, Movable):
    """Continious graph that could move dots"""


class MovableCategoricalGraph(CategoricalGraph, Movable):
    """Categorical graph that could move dots"""
