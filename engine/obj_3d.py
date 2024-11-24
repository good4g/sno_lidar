import numpy as np


from matrix_functions import *
import pygame as pg




class Object3D:
    def __init__(self, render, vertices, faces):
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes = self.vertices @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 1) | (vertexes < -1)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for face in self.faces:
            polygon = vertexes[face]

            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), polygon, 3)

        #for vertex in vertexes:
            #if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                #pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 6)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)