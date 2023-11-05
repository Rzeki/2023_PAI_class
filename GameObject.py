import pygame as pg
from pygame import Vector2 as Vec2
import util

class GameObject:
    def __init__(self, window : pg.Surface) -> None:
        
        self.window : pg.Surface = window
        
        self.position : Vec2 = Vec2(util.dir["ZERO"])
        self.radius : int = 50
        self.body : pg.Rect = pg.Rect(0,0,0,0)
        
    def draw(self) -> None:
        pg.draw.circle(self.window, pg.Color(255, 255, 255), self.position, self.radius)

        
class MovingObject(GameObject):
    def __init__(self, window: pg.Surface) -> None:
        super().__init__(window)
        
        self.velocity : Vec2 = Vec2(util.dir["ZERO"])
        self.direction : Vec2 = Vec2(util.dir["ZERO"])
        self.side : Vec2 = Vec2(util.dir["ZERO"])       #perpendicular to direction, must always update while updating direction vec
        
        self.mass : float = 0.0
        
        self.max_speed : float = 2
        self.max_force : float = 5
        self.max_turn : float = 10
        self.tag : bool  = False
        
        self.speed : float = 0.001
    
    def update(self, dt : float):
        self.position += self.velocity * dt
    
    def check_boundaries(self) -> bool :
        '''Checks screen bounds and bounces object.'''
        wdth, hgth = self.window.get_size()

        if self.position.x - self.radius <= 0:
            self.direction.reflect_ip(Vec2(util.dir["RIGHT"]))
            self.velocity.reflect_ip(Vec2(util.dir["RIGHT"]))
            self.side = util.vec_perp(self.direction)   
            return True
        elif self.position.x + self.radius >= wdth:
            self.direction.reflect_ip(Vec2(util.dir["LEFT"]))
            self.velocity.reflect_ip(Vec2(util.dir["LEFT"]))
            self.side = util.vec_perp(self.direction)
            return True
        elif self.position.y - self.radius <= 0:
            self.direction.reflect_ip(Vec2(util.dir["DOWN"]))
            self.velocity.reflect_ip(Vec2(util.dir["DOWN"]))
            self.side = util.vec_perp(self.direction)
            return True
        elif self.position.y + self.radius >= hgth:
            self.direction.reflect_ip(Vec2(util.dir["UP"]))
            self.velocity.reflect_ip(Vec2(util.dir["UP"]))
            self.side = util.vec_perp(self.direction)
            return True
        else: return False
