from typing import List, Tuple, Union

from manimlib.imports import Scene, VGroup

from classes.movable_funnel import MovableFunnel

from .funnel import Funnel
from .shape_point import ShapePoint


class FunnelsExeption(Exception):
    """Основная ошибка для класса Funnels"""


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
        """Объект - констурктор воронок. Вместе с основными аргументами для текущего класса
        передаются так же все необходимые аргументы для инициализации класса "funnel".

        Args:
            start_end_points (Tuple[tuple, tuple]): Левая верхняя точки и правая верхняя,
                соответственно. ((x1,y1), (x2,y2))
            funnel (Funnel): Класс для построения воронок. Должен наследовать Funnel.
            count (int): Количество воронок.
            bins (Union[int, float]): Количество корзин для воронок
            annot (bool, optional): Подписывать воронки или нет. Defaults to False.

        Example:
            funnels = Funnels(
                start_end_points=((-6.5, -4), (6.5, -4)),
                funnel=MovableFunnel,
                count=5,
                bins=bins,
                annot=True,
                point_radius=0.2,
                run_time=0.8,
                height=4,
            )
        """

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

        # Создаем воронки в цикле и сохраянем их во внутреннюю переменную
        for i in range(self.count):
            self.funnels.append(
                funnel(
                    *args,
                    start_end_points=(
                        (x_start_point, y_point),
                        (x_end_point, y_point),
                    ),
                    annot=annot,
                    annot_text=annots[i],
                    **kwargs,
                )
            )

            x_start_point, x_end_point = x_end_point, x_end_point + step

        super().__init__(*self.funnels)

    def drag_in_dots(self, scene: Scene, dots: VGroup, animate_slow: int, animate_rest: bool):
        """Метод для перемещения точек в воронку. Вызывает такой же метод drag_in_dots
        на каждой из воронок класса.

        Args:
            scene (Scene): Класс сцены.
            dots (VGroup): Точки, которые необходимо переместить.
            animate_slow (int): Сколько точек анимировать по очереди (падение).
            animate_rest (bool): Перемещать остальные точки или нет.

        Raises:
            FunnelsExeption: Исключение выбрасывается, если воронки были созданы не
                через MovableFunnel
        """
        if any(not isinstance(x, MovableFunnel) for x in self.funnels):
            raise FunnelsExeption('метод "drag_in_dots" доступен только для "MovableFunnel"')
        # Сортируем шарики по возрастанию значений, чтобы анимация проигрывалась от
        # меньшего к большему
        _dots = VGroup(*sorted(dots, key=lambda x: x.value))

        for funnel in self.funnels:
            funnel.drag_in_dots(
                scene=scene,
                dots=_dots,
                animate_slow=animate_slow,
                animate_rest=animate_rest,
            )

            animate_slow = animate_slow - funnel.animated_slowly
