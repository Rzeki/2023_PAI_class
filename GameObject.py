import pygame as pg
from pygame import Vector2 as Vec2
import util

class GameObject:
    def __init__(self, window : pg.Surface) -> None:
        
        self.window : pg.Surface = window
        # dir_vect : dict[str, Vec2] = {
        #     "UP": Vec2(0,-1),
        #     "DOWN": Vec2(0,1),
        #     "LEFT": Vec2(-1,0),
        #     "RIGHT": Vec2(1,0),
        #     "ZERO": Vec2(0,0)
        # }
        self.position : Vec2 = Vec2(util.dir["ZERO"])
        self.velocity : Vec2 = Vec2(util.dir["ZERO"])
        self.direction : Vec2 = Vec2(util.dir["ZERO"])
        self.side : Vec2 = Vec2(util.dir["ZERO"])       #perpendicular to direction
        
        self.mass : float = 0.0
        
        #see if it sticks
        self.max_speed : float = 2
        self.max_force : float = 5
        self.max_turn : float = 10
        self.tag : bool  = False
        
        self.speed : float = 0.001
        self.radius : int = 50
        self.body : pg.Rect = pg.Rect(0,0,0,0)
        
    def draw(self) -> None:
        pass
        
    def move(self, dt : float) -> None:
        # self.velocity = direction * self.speed
        self.position += self.velocity * dt
    
    def update(self, dt : float):
        pass
    
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
        


    
    