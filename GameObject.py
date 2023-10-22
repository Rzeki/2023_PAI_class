import pygame as pg

class GameObject:
    def __init__(self) -> None:
        self.position : pg.Vector2 = pg.Vector2(0,0)
        self.direction : pg.Vector2 = pg.Vector2(0,0)
        self.velocity : pg.Vector2 = pg.Vector2(0,0)
        self.speed : float = 0.001
        self.radius : int = 50
        self.body : pg.Rect = pg.Rect(0,0,0,0)
        
    def draw(self, surface) -> None:
        pass
        
    def move(self, dt) -> None:
        # self.velocity = self.direction * self.speed
        self.position += self.velocity * dt
    
    def check_boundaries(self, window : pg.Surface) -> bool :
        '''Checks screen bounds and bounces object.
        TODO: optimize
        TODO: fix corners'''
        wdth, hgth = window.get_size()
        if self.position.x - self.radius <= 0:
            self.direction.reflect_ip(pg.Vector2(1,0))
            self.velocity.reflect_ip(pg.Vector2(1,0))
            return True
        elif self.position.x + self.radius > wdth:
            self.direction.reflect_ip(pg.Vector2(-1,0))
            self.velocity.reflect_ip(pg.Vector2(-1,0))
            return True
        elif self.position.y - self.radius  < 0:
            self.direction.reflect_ip(pg.Vector2(0,1))
            self.velocity.reflect_ip(pg.Vector2(0,1))
            return True
        elif self.position.y + self.radius > hgth:
            self.direction.reflect_ip(pg.Vector2(0,-1))
            self.velocity.reflect_ip(pg.Vector2(0,-1))
            return True
        else: return False

    
    