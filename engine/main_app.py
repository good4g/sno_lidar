import math


import pygame as pg
from obj_3d import Object3D
from camera import *
from projection import *

from rangefinder.get_data import get_clean_data


class SoftWareRender:

    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1920, 1080

        # зададим поверхность отрисовки
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self. HEIGHT // 2

        self.FPS = 60

        self.screen = pg.display.set_mode(self.RES)

        self.clock = pg.time.Clock()

        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        v, f = get_clean_data()
        print(len(v), len(f))
        self.object = Object3D(self, v, f)
        self.object.translate([0.2, 0.4, 0.2])
        #self.object.rotate_y(math.pi / 3)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftWareRender()
    app.run()