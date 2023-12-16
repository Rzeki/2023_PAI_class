import pygame as pg
from pygame import Vector2 as Vec2
import util

from GameObject import MovingObject

class Bullet(MovingObject):
    def __init__(self, window: pg.Surface, position : Vec2, direction : Vec2) -> None:
        super().__init__(window)
        
        self.radius : int = 5
        self.mass : float = 50
        self.position = Vec2(position)
        self.direction = Vec2(direction)   
        
        self.body = pg.image.load("assets\Bomb_02_1.png") 
    
    def update(self, dt: float) -> None:
        self.velocity += pg.Vector2.normalize(self.direction) * dt
        self.position += self.velocity * 0.01 * dt
    
    def draw(self) -> None:
        if util.DEBUG:
            return super().draw()
        self.window.blit(self.body, self.position - Vec2(self.radius, self.radius))
    
    def check_boundaries(self, bullet_poll : list) -> bool :
        '''Checks screen bounds and disappears bullet'''
        wdth, hgth = self.window.get_size()

        if self.position.x <= 30 or self.position.x >= wdth-30 or self.position.y <= 30 or self.position.y >= hgth-30:
            bullet_poll.remove(self)
            return True
        else: return False
    
    def collide(self, obj, bullet_poll : list) -> bool:
        '''Checks collision w obstacles and disappears bullet'''
        distance : Vec2 = self.position - obj.position
        
        if distance.length() < self.radius + obj.radius:
            bullet_poll.remove(self)
            return True
        return False
