import pygame as pg

class GameObject:
    def __init__(self) -> None:
        self.position = pg.Vector2(0,0)
        self.direction = pg.Vector2(0,0)
        self.velocity = pg.Vector2(0,0)
        self.speed = 0.001
        self.radius = 50
        self.body = pg.Rect()
        
    def draw(self, surface) -> None:
        (self.body, self.position)
        
    def move(self, dt) -> None:
        # self.velocity = self.direction * self.speed
        self.position += self.velocity * dt
        