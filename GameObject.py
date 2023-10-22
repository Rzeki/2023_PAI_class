import pygame as pg
from pygame import Vector2 as Vec2

class GameObject:
    def __init__(self) -> None:
        
        self.direction_vec : dict[str, Vec2] = {
            "UP": Vec2(0,-1),
            "DOWN": Vec2(0,1),
            "LEFT": Vec2(-1,0),
            "RIGHT": Vec2(1,0),
            "ZERO": Vec2(0,0)
        }
        self.position : Vec2 = self.direction_vec["ZERO"]
        self.direction : Vec2 = self.direction_vec["ZERO"]
        self.velocity : Vec2 = self.direction_vec["ZERO"]
        self.speed : float = 0.001
        self.radius : int = 50
        self.body : pg.Rect = pg.Rect(0,0,0,0)
        
    def draw(self, surface : pg.Surface) -> None:
        pass
        
    def move(self, dt : int) -> None:
        # self.velocity = direction * self.speed
        self.position += self.velocity * dt
    
    def check_boundaries(self, window : pg.Surface) -> bool :
        '''Checks screen bounds and bounces object.'''
        wdth, hgth = window.get_size()

        if self.position.x - self.radius <= 0:
            self.direction.reflect_ip(self.direction_vec["RIGHT"])
            self.velocity.reflect_ip(self.direction_vec["RIGHT"])
            return True
        elif self.position.x + self.radius >= wdth:
            self.direction.reflect_ip(self.direction_vec["LEFT"])
            self.velocity.reflect_ip(self.direction_vec["LEFT"])
            return True
        elif self.position.y - self.radius <= 0:
            self.direction.reflect_ip(self.direction_vec["DOWN"])
            self.velocity.reflect_ip(self.direction_vec["DOWN"])
            return True
        elif self.position.y + self.radius >= hgth:
            self.direction.reflect_ip(Vec2(0,-1))
            self.velocity.reflect_ip(Vec2(0,-1))
            return True
        else: return False
        


    
    