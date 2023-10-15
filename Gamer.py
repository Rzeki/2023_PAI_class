import pygame as pg
import math

class Player:
    def __init__(self) -> None:
        self.position = pg.Vector2([ z / 2 for z in pg.display.get_surface().get_size() ])
        self.direction = pg.Vector2(0,-1)
        self.velocity = pg.Vector2(0,0)
        self.speed = 0.1
        self.radius = 50
        self.body = pg.image.load("assets\spaceship.png")
        
        
        
    def draw(self, surface) -> None:
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        pg.draw.circle(pg.display.get_surface(), pg.Color(255,255,0), self.position, 5)
        
    def move(self) -> None:
        # self.velocity = self.direction * self.speed
        self.position += self.velocity * 1/60
        