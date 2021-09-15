from typing import List, Tuple, Union

from manimlib.imports import Scene, VGroup

from . import Funnel, ShapePoint


class Funnels(VGroup):
    funnels: List[Funnel] = []

    def __init__(
        self,
        start_end_points: Tuple[tuple, tuple],
        funnel: Funnel,
        count: int,
        bins: Union[int, float],
        annot: bool = False,
        *args,
        **kwargs,
    ):
        """[summary]"""

        self.left_top_point = ShapePoint(start_end_points[0])
        self.right_top_point = ShapePoint(start_end_points[1])
        self.bins = bins
        self.count = count

        step = abs((self.right_top_point[0] - self.left_top_point[0]) / count)
        x_start_point = self.left_top_point[0]
        x_end_point = x_start_point + step
        y_point = self.left_top_point[1]

        # Создаем массив с текстом для аннотаций
        annot_step = int(self.bins / self.count)
        annot_bins = [i for i in range(0, int(self.bins) + annot_step, annot_step)]
        annots = [f"{x+1}–{y}" for x, y in zip(annot_bins[:-1], annot_bins[1:])]

        for i in range(self.count):
            self.funnels.append(
                funnel(
                    *args,
                    start_end_points=((x_start_point, y_point), (x_end_point, y_point)),
                    annot=annot,
                    annot_text=annots[i],
                    **kwargs,
                )
            )

            x_start_point, x_end_point = x_end_point, x_end_point + step

        super().__init__(*self.funnels)

    def drag_in_dots(self, scene: Scene, dots: VGroup, animate_slow: int, animate_rest: bool):
        #
        _dots = VGroup(*sorted(dots, key=lambda x: x.value))

        for funnel in self.funnels:
            funnel.drag_in_dots(scene=scene, dots=_dots, animate_slow=animate_slow, animate_rest=animate_rest)

            animate_slow = animate_slow - funnel.animated_slowly
