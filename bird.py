from pico2d import load_image


BIRD_FRAME_WIDTH = 183
BIRD_FRAME_HEIGHT = 168
BIRD_SHEET_COLUMNS = 5
BIRD_FRAME_COUNT = 14
BIRD_SHEET_HEIGHT = 506


class Bird:
    image = None

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        column = self.frame % BIRD_SHEET_COLUMNS
        row = self.frame // BIRD_SHEET_COLUMNS
        source_y = BIRD_SHEET_HEIGHT - (row + 1) * BIRD_FRAME_HEIGHT
        self.image.clip_draw(
            column * BIRD_FRAME_WIDTH, source_y,
            BIRD_FRAME_WIDTH, BIRD_FRAME_HEIGHT,
            self.x, self.y
        )
