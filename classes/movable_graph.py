from abc import ABC
from copy import deepcopy
from typing import Union

from manimlib.imports import DEFAULT_ANIMATION_RUN_TIME, ApplyMethod, Scene, Transform, VGroup
from numpy import array

from .graph import CategoricalGraph, ContinuousGraph
from .histogram_dot import HistogramDot


class Movable(ABC):
    """Абстрактный класс для придатия объекту возможности перемещения шариков к нему"""

    _next_dot_coords = {}
    dot_padding = 0

    def __init__(self, *args, **kwargs):
        """Инициализация класса"""
        self._next_dots_coords = self._prepare_next_dot_coords()

        super().__init__(*args, **kwargs)

    def _get_next_dot_coords(self, dot: HistogramDot) -> array:
        """Получение координат для локации следующего шарика.
            Применяется при перемещении шариков на объект.

        Args:
            dot (HistogramDot): Объект с шариком.

        Returns:
            array: Cледующая локация шарика.
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
            scene (Scene): Сцена, на которой необходимо показывать перемещение объектов.
            dots (VGroup): Список из шариков.
            animate_slow (int): Количество шариков, которые нужно медленно и красиво переместить.
            animate_rest (bool): Анимировать перемещение остальных шариков или нет.
            run_time (Union[int, float], optional): Время проигрывания перемещения. Defaults to None.
            delay (Union[int, float], optional): Задержка между перемещением шариков. Defaults to None.
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
    """Непрерывный график, который может перемещать к себе шарики."""


class MovableCategoricalGraph(CategoricalGraph, Movable):
    """Категориальный график, который может перемещать к себе шарики."""
