import pygame as pg
from GameObject import GameObject
from pygame import Vector2 as Vec2

class Wall(GameObject):
    def __init__(self, x, y, radius) -> None:
        super().__init__()
        self.position = Vec2(x, y)
        self.radius = radius
        
    def draw(self, surface) -> None:
        pg.draw.circle(surface, pg.Color(255, 0, 0), self.position, self.radius)   