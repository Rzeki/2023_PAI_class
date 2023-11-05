import pygame as pg
from pygame import Vector2 as Vec2
from GameObject import GameObject
import util

class Obstacle(GameObject):
    def __init__(self, window : pg.Surface, x, y, radius) -> None:
        super().__init__(window)
        self.position = Vec2(x, y)
        self.radius = radius
        
    def draw(self) -> None:
        pg.draw.circle(self.window, pg.Color(0, 0, 255), self.position, self.radius)   


 
class Wall(GameObject):
    def __init__(self, window: pg.Surface, start : Vec2, end : Vec2) -> None:
        super().__init__(window)
        self.position = start
        self.radius = 0
        
        self.start : Vec2 = start
        self.end : Vec2 =  end
        self.normal : Vec2 = self.calc_normal()
    
    def draw(self) -> None:
        pg.draw.line(self.window, pg.Color(0, 0, 255), self.start, self.end, 5)
    
    def calc_normal(self) -> Vec2:
        temp : Vec2 = Vec2.normalize(self.end-self.start)
        temp.x, temp.y = -temp.y, temp.x
        return temp