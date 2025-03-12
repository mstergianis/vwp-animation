import manim as mn
import numpy as np

SCALE_FACTOR = 0.5


class VWPAnimation(mn.Scene):
    def construct(self):
        vaultwarden = Box("Vaultwarden")

        gmail = Cipher("gmail login")
        banking = Cipher("banking login")
        github = Cipher("github login")
        gmail.next_to(vaultwarden.heading, mn.DOWN * SCALE_FACTOR)
        banking.next_to(gmail, mn.DOWN * SCALE_FACTOR)
        github.next_to(banking, mn.DOWN * SCALE_FACTOR)

        self.play(mn.Create(vaultwarden))
        self.play(
            mn.Create(gmail),
            mn.Create(banking),
            mn.Create(github),
        )

        vaultwarden.generate_target()
        gmail.generate_target()
        banking.generate_target()
        github.generate_target()

        vaultwarden.target.shift(4 * mn.RIGHT)
        gmail.target.shift(4 * mn.RIGHT)
        banking.target.shift(4 * mn.RIGHT)
        github.target.shift(4 * mn.RIGHT)

        self.play(
            mn.MoveToTarget(vaultwarden),
            mn.MoveToTarget(gmail),
            mn.MoveToTarget(banking),
            mn.MoveToTarget(github),
        )

        # create VWP
        self.vwp = Box("vwp", width=5.0, height=2.0)
        self.unix_pass = Box("pass", width=5.0, height=2.0)
        self.unix_pass.shift(4 * mn.LEFT)
        self.play(mn.Create(self.vwp), mn.Create(self.unix_pass))

        self.move_unlock_relock(gmail, run_time=0.8)
        self.move_unlock_relock(banking, run_time=0.8)
        self.move_unlock_relock(github, run_time=0.8)

        self.play(
            mn.FadeOut(vaultwarden), mn.FadeOut(self.vwp), mn.FadeOut(self.unix_pass)
        )

        self.wait(0.5)

    def move_unlock_relock(self, cipher, run_time=1.0):
        cipher.generate_target()
        cipher.target.next_to(self.vwp.heading, mn.DOWN * SCALE_FACTOR)
        self.play(mn.MoveToTarget(cipher, run_time=run_time))
        self.play(cipher.unlock(run_time=run_time))

        cipher.generate_target()
        cipher.target.next_to(self.unix_pass.heading, mn.DOWN * SCALE_FACTOR)
        self.play(mn.MoveToTarget(cipher, run_time=run_time))
        self.play(cipher.relock(run_time=run_time))
        self.play(mn.FadeOut(cipher, run_time=run_time))
        pass


class Box(mn.VGroup):
    def __init__(self, text_content, width=5.0, height=4.0, **kwargs):
        super().__init__(**kwargs)
        self.box = mn.Rectangle(
            width=width * SCALE_FACTOR, height=height * SCALE_FACTOR
        )
        self.box.set_color(mn.BLUE_D)

        self.heading = mn.Rectangle(
            width=width * SCALE_FACTOR, height=0.75 * SCALE_FACTOR
        )
        self.heading.set_color(mn.BLUE_D)
        self.heading.set_fill(mn.BLUE_D, opacity=1.0)
        self.heading.align_to(self.box, mn.UP)

        self.text = mn.Tex(text_content, font_size=mn.DEFAULT_FONT_SIZE * SCALE_FACTOR)
        self.text.move_to(self.heading, mn.LEFT)
        self.text.shift(np.array((0.1 * SCALE_FACTOR, 0.0, 0.0)))

        self.add(self.box, self.heading, self.text)

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs):
        return mn.Succession(
            mn.AnimationGroup(
                mn.FadeIn(self.box),
                mn.FadeIn(self.heading),
            ),
            mn.Write(self.text),
            **kwargs,
        )

    def push(self, element) -> mn.Animation:
        pass


class Cipher(mn.VGroup):
    def __init__(self, text_content, **kwargs):
        super().__init__(**kwargs)
        self.border_width = 4.0 * SCALE_FACTOR
        self.border_height = 0.75 * SCALE_FACTOR
        self.border_stroke_width = mn.DEFAULT_STROKE_WIDTH * 0.75
        self.border = mn.Rectangle(
            width=self.border_width,
            height=self.border_height,
            stroke_width=self.border_stroke_width,
        )
        self.border_vw_color = mn.GOLD_E
        self.border_unix_pass_color = mn.GREEN
        self.border.set_color(self.border_vw_color)

        self.text = mn.Tex(text_content, font_size=mn.DEFAULT_FONT_SIZE * SCALE_FACTOR)
        self.text.align_to(self.border, mn.LEFT)
        self.text_shift = np.array((0.1, 0, 0))
        self.text.shift(self.text_shift)

        self.lock = Lock(0.25)
        self.lock.align_to(
            self.border,
            mn.RIGHT,
        )
        self.lock.shift(np.array((-self.lock.width * 0.25, 0, 0)))

        self.add(self.border, self.text, self.lock)

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs):
        return mn.Succession(
            mn.AnimationGroup(
                mn.FadeIn(self.border),
                mn.Create(self.lock),
            ),
            mn.Write(self.text),
            **kwargs,
        )

    def unlock(self, run_time=1.0) -> mn.Animation:
        return mn.Succession(
            mn.AnimationGroup(
                self.lock.unlock(),
                self.border.animate.set_stroke(opacity=0.0),
                run_time=run_time,
            ),
        )

    def relock(self, run_time=1.0) -> mn.Animation:
        self.border.set_stroke(color=self.border_unix_pass_color)
        return mn.AnimationGroup(
            self.border.animate.set_stroke(opacity=1.0),
            self.lock.relock(),
            run_time=run_time,
        )


class Lock(mn.VGroup):
    def __init__(self, scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.scale = scale
        self.svg = self._construct_lock()
        self.add(self.svg)

    def _construct_gen(self, f):
        return mn.SVGMobject(
            f,
            width=1.0 * self.scale,
            height=1.0 * self.scale,
            stroke_color=mn.WHITE,
        )

    def _construct_lock(self):
        return self._construct_gen("./svg/lock.svg")

    def _construct_unlock(self):
        return self._construct_gen("./svg/unlock.svg")

    def unlock(self, run_time=1.0) -> mn.Animation:
        unlock = self._construct_unlock()
        unlock.move_to(self.svg)

        # https://www.reddit.com/r/manim/comments/bq5bk2/manim_tutorial_difference_between_transform_and/
        return mn.Transform(self.svg, unlock, run_time=run_time)

    def relock(self, run_time=1.0) -> mn.Animation:
        lock = self._construct_lock()
        lock.move_to(self.svg)
        return mn.Transform(self.svg, lock, run_time=run_time)


class ManualLock(mn.VGroup):
    def __init__(self, scale=1.0, **kwargs):
        self.scale = scale
        super().__init__(**kwargs)
        self.rect = mn.RoundedRectangle(
            corner_radius=0.15 * scale,
            width=0.8 * scale,
            height=0.8 * scale,
            stroke_width=mn.DEFAULT_STROKE_WIDTH * scale,
        )
        anchors = [x for x in self.rect.get_anchors()]

        left_start = anchors[3]
        left_end = anchors[3] + np.array((0, 0.1 * scale, 0))
        self.left_line = mn.Line(
            left_start, left_end, stroke_width=mn.DEFAULT_STROKE_WIDTH * scale
        )

        right_start = anchors[2] + np.array((0, 0.1 * scale, 0))
        right_end = anchors[2]
        # self.right_line = mn.Line(right_start, right_end)

        # self.lock_curve = mn.CubicBezier(
        #     left_end,
        #     left_end + np.array((0.1, 0.5, 0)),
        #     right_start + np.array((-0.1, 0.5, 0)),
        #     right_start,
        # )

        self.left_line.add_cubic_bezier_curve_to(
            left_end + np.array((0.05 * scale, 0.25 * scale, 0)),
            right_start + np.array((-0.05 * scale, 0.25 * scale, 0)),
            right_start,
        )
        self.left_line.add_line_to(
            right_end,
        )

        self.add(self.rect, self.left_line)

    def unlock(self) -> mn.Animation:
        translation = np.array((0, 0.15 * self.scale, 0))
        self.left_line.generate_target()
        start, end = self.left_line.target.get_start(), self.left_line.target.get_end()
        self.left_line.target.put_start_and_end_on(start, end + translation)
        return mn.MoveToTarget(self.left_line)

    def relock(self) -> mn.Animation:
        translation = np.array((0, -0.15 * self.scale, 0))
        self.left_line.generate_target()
        start, end = self.left_line.target.get_start(), self.left_line.target.get_end()
        self.left_line.target.put_start_and_end_on(start, end + translation)
        return mn.MoveToTarget(self.left_line)

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs):
        return mn.AnimationGroup(
            mn.Create(self.rect),
            mn.Create(self.left_line, run_time=1.5),
        )


class LockScene(mn.Scene):
    def construct(self):
        lock = mn.SVGMobject(
            "./svg/lock.svg",
            width=1.0,
            height=1.0,
            stroke_color=mn.WHITE,
        )
        unlock = mn.SVGMobject(
            "./svg/unlock.svg",
            width=1.0,
            height=1.0,
            stroke_color=mn.WHITE,
        )
        self.play(mn.Create(lock))
        self.play(mn.ReplacementTransform(lock, unlock))
        self.play(mn.Wait(0.5))
