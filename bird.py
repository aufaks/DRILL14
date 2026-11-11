from pico2d import load_image

import game_framework


BIRD_FRAME_WIDTH = 183
BIRD_FRAME_HEIGHT = 168
BIRD_SHEET_COLUMNS = 5
BIRD_FRAME_COUNT = 14
BIRD_SHEET_HEIGHT = 506
BIRD_FRAMES_PER_SECOND = 12.0
PIXEL_PER_METER = 10.0 / 0.3
BIRD_SPEED_KMPH = 15.0
BIRD_SPEED_MPS = BIRD_SPEED_KMPH * 1000.0 / 3600.0
BIRD_SPEED_PPS = BIRD_SPEED_MPS * PIXEL_PER_METER


class Bird:
    image = None

    def __init__(self, x, y, direction=1):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x, self.y = x, y
        self.direction = direction
        self.frame = 0.0

    def update(self):
        frame_time = game_framework.frame_time
        self.x += self.direction * BIRD_SPEED_PPS * frame_time
        self.frame = (
            self.frame + BIRD_FRAMES_PER_SECOND * frame_time
        ) % BIRD_FRAME_COUNT

    def draw(self):
        frame_index = int(self.frame)
        column = frame_index % BIRD_SHEET_COLUMNS
        row = frame_index // BIRD_SHEET_COLUMNS
        source_y = BIRD_SHEET_HEIGHT - (row + 1) * BIRD_FRAME_HEIGHT
        self.image.clip_draw(
            column * BIRD_FRAME_WIDTH, source_y,
            BIRD_FRAME_WIDTH, BIRD_FRAME_HEIGHT,
            self.x, self.y
        )
