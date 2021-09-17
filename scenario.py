from copy import deepcopy
from random import randint

from colour import Color
from manimlib.imports import BLACK, Dot, FadeIn, FadeOut, Scene, Transform, VGroup
from numpy import array

from classes import (
    CategoricalGraph,
    ContinuousGraph,
    CustomersTable,
    Funnel,
    Funnels,
    HistogramText,
    MovableCategoricalGraph,
    MovableContinuousGraph,
    MovableFunnel,
)


class Scenario:
    def __init__(self, scene: Scene):
        """Main scenario class initialization.

        Args:
            scene (Scene): Instance of the Scene class.
        """
        self.scene = scene

    def play_first_scene(self):
        # We are creating list for storing dots
        dots = []

        # Columns with dots will be placed one after another, so X position
        # will be calculated automatically
        start_x = -4

        # Dot size
        point_radius = 0.3

        for _ in range(5):
            # Dots inside columns will be placed one above the other, so Y position
            # will be calculated automatically
            start_y = -2

            for _ in range(randint(2, 6)):
                dots.append(
                    Dot(
                        point=array([start_x, start_y, 0]),  # Coordinates on the screen, assigned with x,y,z
                        radius=point_radius,  # Dot size
                        stroke_width=1,  # Border width
                        stroke_color=BLACK,  # Border color
                        color="#7fcc81",  # Dot color
                    )
                )
                start_y += 0.7
            start_x += 2

        # Grouping dots into VGroup that is the Scene's element
        dots = VGroup(*dots)

        # Adding dots to the scene
        self.scene.add(dots)

        # Creating text. We are using our own Overridden class.
        heading = HistogramText("Гистограммы", color=BLACK)

        # Changin text size with scale
        heading.scale(2)

        # Changing text location
        heading.move_to(array([0, 2.5, 0]))

        # Playing animation for the text appearing
        self.scene.play(FadeIn(heading))

        # Waiting
        self.scene.wait(2)

        # Playing animation for the text disappearing
        self.scene.play(FadeOut(dots), FadeOut(heading))

        # Waiting
        self.scene.wait(1)

    def play_second_scene(self):
        table = CustomersTable(
            ((-2, 2), (2, 2)),
            row_count=10,
            visible_row_count=5,
            bins=2,
        )

        self.scene.play(FadeIn(table))

        self.scene.wait(3)

    def play_third_scene(self):
        cont_graph = ContinuousGraph(
            ((-4, -1), (0, -1)),
            ((-2, 1), (-2, -3)),
            bins=4,
            annot=False,
        )

        cat_graph = CategoricalGraph(
            ((0, 2), (4, 2)),
            None,
            bins=4,
            annot=True,
        )

        self.scene.play(FadeIn(cont_graph), FadeIn(cat_graph))

        self.scene.wait(3)

    def play_fourth_scene(self):
        funnel = Funnel(
            ((-2, 2), (1, -2)),
            height=4,
            point_radius=0.2,
        )

        self.scene.play(
            FadeIn(funnel),
        )

        self.scene.wait(3)

    def play_fifth_scene(self):
        # Initial dot values, to keep them the same over several animation builds
        start_dot_values = [1, 2, 1, 3, 4, 2, 1]

        # Table initialization
        table = CustomersTable(
            ((-6, 2), (-2, 2)),
            row_count=10,
            visible_row_count=8,
            bins=4,
            start_dots_values=start_dot_values,
        )

        # Graph initialization
        x_graph = MovableCategoricalGraph(
            ((0, 0), (4, 0)),
            None,
            bins=4,
            annot=True,
        )

        # Playing animation for the table and graph appearing
        self.scene.play(FadeIn(table), FadeIn(x_graph))

        self.scene.wait(2)

        # Moving dots from the table to the graph
        x_graph.drag_in_dots(self.scene, dots=table.dots, animate_slow=3, animate_rest=True)

        self.scene.wait(3)

    def play_sixth_scene(self):
        bins = 100
        funnels = Funnels(
            start_end_points=((-6.5, 0), (6.5, 0)),
            funnel=MovableFunnel,
            count=5,
            bins=bins,
            annot=True,
            point_radius=0.2,
            run_time=0.8,
            height=3,
        )

        start_dot_values = [1, 2, 1, 3, 4, 2, 1]

        table = CustomersTable(
            ((-5, 2), (-1, 2)),
            row_count=3,
            visible_row_count=3,
            bins=4,
            start_dots_values=start_dot_values,
        )

        self.scene.add(funnels, table)

        funnels.drag_in_dots(scene=self.scene, dots=table.dots, animate_slow=3, animate_rest=False)

    def play_whole_scenario(self):
        # Dot bins maximum value
        bins = 100

        # Adding dot colors (from green to red)
        dot_colors = list(Color("#7fcc81").range_to("#ff7555", int(bins)))

        # Initial dot values, to keep them the same over several animation builds
        start_dots_values = [31, 25, 63, 47, 82, 25, 49, 99, 21, 33, 37]

        # Custom text for the table (Customer/buyer)
        table_text = "Заказчик"

        # Table initialization
        table = CustomersTable(
            ((-6.5, 3), (-2.5, 3)),
            row_count=30,
            visible_row_count=11,
            bins=bins,
            colors=dot_colors,
            start_dots_values=start_dots_values,
            text=table_text,
        )

        # Graph initialization
        x_graph = MovableContinuousGraph(
            ((-2, -3), (6.5, -3)),
            None,
            bins=bins,
            annot=True,
        )

        # New graph that will be on the whole screen width
        x_graph_second_position = MovableContinuousGraph(
            ((-6.5, -3), (6.5, -3)),
            None,
            bins=bins,
            annot=True,
        )

        # Copying dots. This for the future needs.
        dots_second_position = deepcopy(table.dots)

        # Playing animations
        self.scene.play(FadeIn(table), FadeIn(x_graph))

        self.scene.wait(2)

        # Moving dots from the table to the graph
        x_graph.drag_in_dots(
            self.scene,
            dots=table.dots,
            animate_slow=3,
            animate_rest=True,
        )

        self.scene.wait(3)

        # Removing graph
        self.scene.play(FadeOut(table.lines), FadeOut(table.customers))

        # Moving dots from the first graph to the second
        x_graph_second_position.drag_in_dots(
            scene=self.scene,
            dots=dots_second_position,
            animate_slow=0,
            animate_rest=False,
        )

        # Playing animation with moving graph from position 1 to position 2, and same for the dots.
        self.scene.play(
            Transform(x_graph, x_graph_second_position),
            Transform(table.dots, dots_second_position),
        )

        self.scene.wait(3)

        # Adding funnels
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

        # Adding funnels to the screen
        self.scene.add(funnels)

        # Moving camer to the bottom
        self.scene.play(self.scene.camera_frame.move_to, array([0, -5.5, 0]))

        self.scene.wait(1)

        # Moving dots from the graph to the funnels
        funnels.drag_in_dots(
            scene=self.scene,
            dots=table.dots,
            animate_slow=9,
            animate_rest=True,
        )

        self.scene.wait(3)

        # Removing all objects from scene
        self.scene.play(
            FadeOut(funnels),
            FadeOut(table.dots),
            FadeOut(x_graph),
            FadeOut(x_graph_second_position),
        )

        # Moving scene back to center
        self.scene.play(self.scene.camera_frame.move_to, array([0, 0, 0]))

        self.scene.wait(1)
