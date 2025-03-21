import manim as mn
import numpy as np
from collections.abc import Hashable, Sequence


class HuffmanAnimation(mn.Scene):
    def construct(self):
        self.tree = Tree(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            [
                (0, 2),
                (0, 1),
                (1, 4),
                (1, 3),
                (2, 6),
                (2, 5),
                (4, 8),
                (4, 7),
                (6, 10),
                (6, 9),
                (8, 12),
                (8, 11),
                (9, 14),
                (9, 13),
                (10, 16),
                (10, 15),
            ],
            labels={
                # recursive nodes
                0: "0",
                1: "1",
                2: "2",
                4: "4",
                6: "6",
                8: "8",
                9: "9",
                10: "10",
                # leaf nodes
                3: "o",
                5: "l",
                7: "h",
                11: "d",
                12: r"\textbackslash{}n",
                13: "w",
                14: "r",
                15: "e",
                16: "`` ''",
            },
            layout="tree",
            layout_scale=5,
            root_vertex=0,
            vertex_type=Node,
            edge_config={
                "tip_config": {
                    "tip_width": 0.0,
                    "tip_length": 0.0,
                },
            },
        )

        # Node(
        #     char=0,
        #     left=Node(1),
        # )
        self.play(mn.Create(self.tree), run_time=8.0)

        self.traversals = []

        self.char_label = mn.Tex("char:").to_corner(mn.UL)
        self.char = mn.Tex("h").next_to(self.char_label, mn.RIGHT)
        self.play(mn.Succession(mn.Create(self.char_label), mn.Create(self.char)))

        self.animate_h()
        self.animate_e()
        self.animate_l()

        return

    def animate_h(self):
        self.digits = self.create_digits("0")
        dot_destroyer = self.animate_traversal(self.tree.edges[(0, 1)])
        self.play(
            mn.AnimationGroup(dot_destroyer, mn.Create(self.digits, run_time=0.75))
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(1, 4)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("01"), run_time=0.75),
            )
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(4, 7)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("010"), run_time=0.75),
            )
        )
        self.completed_text = mn.Tex("h").to_corner(mn.UR)
        self.play(mn.ReplacementTransform(self.digits, self.completed_text))

        self.clear_traversals()

    def animate_e(self):
        self.play(mn.Transform(self.char, mn.Tex("e").move_to(self.char, mn.DOWN)))
        self.digits = self.create_digits("1")
        dot_destroyer = self.animate_traversal(self.tree.edges[(0, 2)])
        self.play(
            mn.AnimationGroup(dot_destroyer, mn.Create(self.digits, run_time=0.75))
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(2, 6)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("11"), run_time=0.75),
            )
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(6, 10)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("111"), run_time=0.75),
            )
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(10, 15)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("1110"), run_time=0.75),
            )
        )

        old_completed_text = self.completed_text
        self.completed_text = mn.Tex("he").to_corner(mn.UR)
        self.play(
            mn.AnimationGroup(
                mn.ReplacementTransform(self.digits, self.completed_text),
                mn.LaggedStart(mn.FadeOut(old_completed_text), lag_ratio=0.6),
            )
        )

        self.clear_traversals()

    def animate_l(self):
        self.play(mn.Transform(self.char, mn.Tex("l").move_to(self.char, mn.DOWN)))
        self.digits = self.create_digits("1")
        dot_destroyer = self.animate_traversal(self.tree.edges[(0, 2)])
        self.play(
            mn.AnimationGroup(dot_destroyer, mn.Create(self.digits, run_time=0.75))
        )

        dot_destroyer = self.animate_traversal(self.tree.edges[(2, 5)])
        self.play(
            mn.AnimationGroup(
                dot_destroyer,
                mn.Transform(self.digits, self.create_digits("10"), run_time=0.75),
            )
        )

        old_completed_text = self.completed_text
        self.completed_text = mn.Tex("hel").to_corner(mn.UR)
        self.play(
            mn.AnimationGroup(
                mn.ReplacementTransform(self.digits, self.completed_text),
                mn.LaggedStart(mn.FadeOut(old_completed_text), lag_ratio=0.6),
            )
        )

        self.clear_traversals()

    def animate_traversal(self, edge):
        dot = mn.Dot(radius=0.05).set_color(mn.GOLD)
        l2 = mn.VMobject()
        l2.add_updater(
            lambda x: x.become(mn.Line(edge.start, dot.get_center()).set_color(mn.GOLD))
        )
        self.add(dot, l2)
        self.play(mn.MoveAlongPath(dot, edge), run_time=0.5, rate_func=mn.linear)

        self.traversals.append(l2)
        return mn.FadeOut(dot, run_time=0.5)

    def clear_traversals(self):
        self.play(
            mn.AnimationGroup(mn.FadeOut(mobj) for mobj in self.traversals),
        )
        self.remove(mobj for mobj in self.traversals)
        self.traversals = []

    def create_digits(self, digits):
        return mn.Tex(digits).next_to(self.char, mn.RIGHT, aligned_edge=mn.DOWN)


type Node = Node


class Tree(mn.Graph):
    def __init__(
        self,
        vertices: Sequence[Hashable],
        edges: Sequence[tuple[Hashable, Hashable]],
        labels: bool | dict = False,
        label_fill_color: str = mn.BLACK,
        layout="spring",
        layout_scale: float | tuple[float, float, float] = 2,
        layout_config: dict | None = None,
        vertex_type: type[mn.Mobject] = mn.Dot,
        vertex_config: dict | None = None,
        vertex_mobjects: dict | None = None,
        edge_type: type[mn.Mobject] = mn.Line,
        partitions: Sequence[Sequence[Hashable]] | None = None,
        root_vertex: Hashable | None = None,
        edge_config: dict | None = None,
    ):
        super().__init__(
            vertices,
            edges,
            labels,
            label_fill_color,
            layout,
            layout_scale,
            layout_config,
            vertex_type,
            vertex_config,
            vertex_mobjects,
            edge_type,
            partitions,
            root_vertex,
            edge_config,
        )
        self._populate_edge_dict(edges, edge_type)

    def _populate_edge_dict(
        self, edges: list[tuple[Hashable, Hashable]], edge_type: type[mn.Mobject]
    ):
        self.edges = {
            (u, v): edge_type(
                self[u].get_bottom(),
                self[v].get_top(),
                z_index=-1,
                **self._edge_config[(u, v)],
            )
            for (u, v) in edges
        }

    def update_edges(self, graph):
        """Updates the edges to stick at their corresponding vertices.

        Arrow tips need to be repositioned since otherwise they can be
        deformed.
        """
        for (u, v), edge in graph.edges.items():
            # Passing the Mobject instead of the vertex makes the tip
            # stop on the bounding box of the vertex.
            edge.set_points_by_ends(
                graph[u].get_bottom(),
                graph[v].get_top(),
                buff=self._edge_config.get("buff", 0),
                path_arc=self._edge_config.get("path_arc", 0),
            )


class Node(mn.VGroup):
    def __init__(
        self,
        label: str | None = None,
        left: Node | None = None,
        right: Node | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.border = mn.Circle(radius=0.3, color=mn.BLUE_D)
        if label is not None:
            self.label = mn.Tex(label, font_size=mn.DEFAULT_FONT_SIZE * 0.5)
            self.add(self.label)

        self.add(self.border)

    # def get_center(self) -> mn.Vector:
    #     """Get center Point3Ds"""
    #     return self.get_critical_point(mn.UP)

    def get_top(self) -> mn.Vector:
        """Get center Point3Ds"""
        return self.border.point_at_angle(mn.PI / 2)

    def get_bottom(self) -> mn.Vector:
        """Get center Point3Ds"""
        return self.border.point_at_angle(3 * mn.PI / 2)
