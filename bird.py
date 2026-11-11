from pico2d import get_canvas_width, load_image

import game_framework


BIRD_FRAME_WIDTH = 183
BIRD_FRAME_HEIGHT = 168
BIRD_DISPLAY_WIDTH = 100
BIRD_DISPLAY_HEIGHT = 92
BIRD_SHEET_COLUMNS = 5
BIRD_FRAME_COUNT = 14
BIRD_SHEET_HEIGHT = 506
BIRD_COUNT = 10
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
        """Advance flight and animation using elapsed time and reflected bounds."""
        frame_time = game_framework.frame_time
        half_width = BIRD_DISPLAY_WIDTH / 2
        left_edge = half_width
        right_edge = get_canvas_width() - half_width
        travel_distance = BIRD_SPEED_PPS * frame_time
        flight_span = right_edge - left_edge
        phase = (
            self.x - left_edge
            if self.direction > 0
            else 2 * flight_span - (self.x - left_edge)
        )
        phase = (phase + travel_distance) % (2 * flight_span)
        if phase < flight_span:
            self.x = left_edge + phase
            self.direction = 1
        else:
            self.x = right_edge - (phase - flight_span)
            self.direction = -1

        self.frame = (
            self.frame + BIRD_FRAMES_PER_SECOND * frame_time
        ) % BIRD_FRAME_COUNT

    def draw(self):
        frame_index = int(self.frame)
        column = frame_index % BIRD_SHEET_COLUMNS
        row = frame_index // BIRD_SHEET_COLUMNS
        source_y = BIRD_SHEET_HEIGHT - (row + 1) * BIRD_FRAME_HEIGHT
        flip = '' if self.direction > 0 else 'h'
        self.image.clip_composite_draw(
            column * BIRD_FRAME_WIDTH, source_y,
            BIRD_FRAME_WIDTH, BIRD_FRAME_HEIGHT,
            0, flip, self.x, self.y,
            BIRD_DISPLAY_WIDTH, BIRD_DISPLAY_HEIGHT,
        )
