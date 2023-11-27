import pygame as pg
from GameObject import *
from pygame import Vector2 as Vec2
import util

class Player(MovingObject):
    def __init__(self, window : pg.Surface) -> None:
        super().__init__(window)
        self.position = pg.Vector2([ z / 2 for z in self.window.get_size() ])
        self.direction = Vec2(util.dir["UP"])
        self.body = pg.image.load("assets\spaceship.png")
        self._speed = 0.001 #fix this so its not needed
              
    def draw(self) -> None:
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.window.blit(rotated_surface, blit_position)
        if util.DEBUG:
            pg.draw.circle(self.window, pg.Color(255, 255, 0, 0), self.position, self.radius)
            pg.draw.line(self.window, pg.Color(0, 0, 255), self.position, self.position + self.velocity*100, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.direction * 50, 3)
        
    def rotate(self, manuverability : int) -> None:
        self.direction.rotate_ip(manuverability)
        
    def collide(self, obj : GameObject) -> None:
        distance : Vec2 = self.position - obj.position
        n = distance.normalize()
        
        if distance.length() < self.radius + obj.radius:
            self.velocity.reflect_ip(n)
            self.direction.reflect_ip(n) 
        
    
        
        