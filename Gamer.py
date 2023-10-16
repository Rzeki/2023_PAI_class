import pygame as pg
from GameObj import GameObject

class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.position = pg.Vector2([ z / 2 for z in pg.display.get_surface().get_size() ])
        self.direction = pg.Vector2(0,-1)
        self.body = pg.image.load("assets\spaceship.png")
              
    def draw(self, surface) -> None:
        super().draw(surface)
        pg.draw.circle(pg.display.get_surface(), pg.Color(255,255,0), self.position, 5)
        
    def rotate(self, manuverability):
        self.direction.rotate_ip(manuverability)
        
        