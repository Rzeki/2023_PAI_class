import pygame as pg
import math

class Player:
    def __init__(self) -> None:
        self.position = pg.Vector2([ z/2 for z in pg.display.get_surface().get_size()])
        self.direction = pg.Vector2(1,0)
        self.velocity = pg.Vector2(0,0)
        self.speed = 10
        self.size = 50
        self.body = pg.image.load("assets\spaceship.png")
        self.body = pg.transform.rotate(self.body, -90)
        
        
        
    def draw(self) -> None:
        pg.display.get_surface().blit(self.body,(self.position.x - self.body.get_size()[0]/2, self.position.y - self.body.get_size()[1]/2))
        pg.draw.circle(pg.display.get_surface(), pg.Color(255,255,0), self.position, 5)
        
    def move(self) -> None:
        # try:
        #     self.velocity = pg.Vector2.normalize(self.direction) * self.speed
        # except ValueError:
        self.velocity = self.direction * self.speed
        self.velocity.x = pg.math.clamp(self.velocity.x, -10, 10)
        self.velocity.y = pg.math.clamp(self.velocity.y, -10, 10)
        self.position += self.velocity * 1/60