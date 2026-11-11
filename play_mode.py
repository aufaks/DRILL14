from pico2d import *
import game_world
import game_framework
from boy import Boy
from bird import BIRD_COUNT, BIRD_DISPLAY_WIDTH, Bird
from grass import Grass

boy = None
birds = []


def create_bird_flock():
    left_edge = BIRD_DISPLAY_WIDTH / 2
    right_edge = get_canvas_width() - left_edge
    flight_lanes = (250, 440)

    return [
        Bird(
            left_edge + (right_edge - left_edge) * index / (BIRD_COUNT - 1),
            flight_lanes[index % len(flight_lanes)],
            1 if index % 2 == 0 else -1,
        )
        for index in range(BIRD_COUNT)
    ]


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy, birds

    boy = Boy()
    game_world.add_oject(boy)

    birds = create_bird_flock()
    for bird in birds:
        game_world.add_oject(bird)

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy, birds
    game_world.clear()
    boy = None
    birds = []


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()






