import manim as mn
import numpy as np


class HuffmanAnimation(mn.Scene):
    def construct(self):
        tree = mn.DiGraph(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            [
                (0, 1),
                (0, 2),
                (1, 3),
                (1, 4),
                (2, 5),
                (2, 6),
                (4, 7),
                (4, 8),
                (6, 9),
                (6, 10),
                (8, 11),
                (8, 12),
                (9, 13),
                (9, 14),
                (1, 15),
                (1, 16),
            ],
            labels={
                3: "o",
                5: "l",
                7: "h",
                11: "d",
                12: "newline",
                13: "w",
                14: "r",
                15: "e",
                16: '" "',
            },
            layout="tree",
            root_vertex=0,
            vertex_type=Node,
        )

        # Node(
        #     char=0,
        #     left=Node(1),
        # )
        self.play(mn.Create(tree), run_time=7.0)
        pass


type Node = Node


class Node(mn.VGroup):
    def __init__(
        self,
        label: str | None = None,
        left: Node | None = None,
        right: Node | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        scale = 0.1
        self.border = mn.Circle(radius=2.0 * scale)
        if label is not None:
            self.label = mn.Tex(label, font_size=mn.DEFAULT_FONT_SIZE * 2 * scale)
            self.add(self.label)

        self.add(self.border)
