import pygame as pg
from GameObject import GameObject
from pygame import Vector2 as Vec2

class Wall(GameObject):
    def __init__(self, window, x, y, radius) -> None:
        super().__init__(window)
        self.position = Vec2(x, y)
        self.radius = radius
        
    def draw(self) -> None:
        pg.draw.circle(self.window, pg.Color(0, 0, 255), self.position, self.radius)   