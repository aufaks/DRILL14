import sys
import types
import unittest
from unittest.mock import patch


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_draw(self, *args):
        self.draw_calls.append(args)


image = FakeImage()
pico2d_stub = types.ModuleType('pico2d')
pico2d_stub.get_canvas_width = lambda: 1600
pico2d_stub.load_image = lambda _: image
framework_stub = types.ModuleType('game_framework')
framework_stub.frame_time = 0.0
boy_stub = types.ModuleType('boy')
boy_stub.Boy = object
grass_stub = types.ModuleType('grass')
grass_stub.Grass = object

with patch.dict(sys.modules, {
        'pico2d': pico2d_stub,
        'game_framework': framework_stub,
        'boy': boy_stub,
        'grass': grass_stub,
}):
    import bird
    import play_mode


class BirdTests(unittest.TestCase):
    def setUp(self):
        bird.game_framework.frame_time = 0.0
        image.draw_calls.clear()
        bird.Bird.image = None

    def test_motion_and_animation_use_elapsed_time(self):
        first = bird.Bird(400, 250)
        bird.game_framework.frame_time = 0.5
        first.update()

        second = bird.Bird(400, 250)
        bird.game_framework.frame_time = 0.25
        second.update()
        second.update()

        self.assertAlmostEqual(first.x, second.x)
        self.assertAlmostEqual(first.frame, second.frame)
        self.assertAlmostEqual(first.x, 400 + bird.BIRD_SPEED_PPS * 0.5)

    def test_draw_selects_the_correct_atlas_cell(self):
        flying_bird = bird.Bird(320, 250)
        flying_bird.frame = 6.9
        flying_bird.draw()

        self.assertEqual(
            image.draw_calls[-1],
            (bird.BIRD_FRAME_WIDTH, 170,
             bird.BIRD_FRAME_WIDTH, bird.BIRD_FRAME_HEIGHT, 320, 250),
        )

    def test_bird_turns_before_leaving_the_canvas(self):
        flying_bird = bird.Bird(1600 - bird.BIRD_FRAME_WIDTH / 2, 250, 1)
        bird.game_framework.frame_time = 0.1
        flying_bird.update()

        self.assertAlmostEqual(
            flying_bird.x,
            1600 - bird.BIRD_FRAME_WIDTH / 2
            - bird.BIRD_SPEED_PPS * 0.1,
        )
        self.assertEqual(flying_bird.direction, -1)

    def test_large_frame_time_preserves_distance_after_edge_turn(self):
        right_edge = 1600 - bird.BIRD_FRAME_WIDTH / 2
        flying_bird = bird.Bird(right_edge - 20, 250, 1)
        elapsed_time = 2.0
        bird.game_framework.frame_time = elapsed_time
        flying_bird.update()

        distance_after_turn = (
            bird.BIRD_SPEED_PPS * elapsed_time - 20
        )
        self.assertAlmostEqual(
            flying_bird.x, right_edge - distance_after_turn
        )
        self.assertEqual(flying_bird.direction, -1)

    def test_animation_repeats_after_all_frames(self):
        flying_bird = bird.Bird(400, 250)
        flying_bird.frame = bird.BIRD_FRAME_COUNT - 0.5
        bird.game_framework.frame_time = 1 / bird.BIRD_FRAMES_PER_SECOND
        flying_bird.update()

        self.assertAlmostEqual(flying_bird.frame, 0.5)

    def test_play_mode_creates_ten_birds_in_two_lanes(self):
        flock = play_mode.create_bird_flock()

        self.assertEqual(len(flock), 10)
        self.assertEqual({flying_bird.y for flying_bird in flock}, {250, 440})
        self.assertEqual(
            [flying_bird.direction for flying_bird in flock],
            [1 if index % 2 == 0 else -1 for index in range(10)],
        )


if __name__ == '__main__':
    unittest.main()
