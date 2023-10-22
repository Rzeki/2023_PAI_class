import pygame as pg
from GameObject import GameObject
from pygame import Vector2 as Vec2

class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.position = pg.Vector2([ z / 2 for z in pg.display.get_surface().get_size() ])
        self.direction = self.direction_vec["UP"]
        self.body = pg.image.load("assets\spaceship.png")
              
    def draw(self, surface : pg.Surface) -> None:
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        pg.draw.circle(surface, pg.Color(255, 255, 0, 100), self.position, self.radius)
        pg.draw.line(surface, pg.Color(0, 0, 255), self.position, self.position + self.velocity * 50, 5)
        pg.draw.line(surface, pg.Color(255, 0, 255), self.position, self.position + self.direction * 500, 5)
        
    def rotate(self, manuverability : int) -> None:
        self.direction.rotate_ip(manuverability)
        
    def collide(self, obj : GameObject) -> None:
        distance : Vec2 = self.position - obj.position
        n = distance.normalize()
        
        if distance.length() < self.radius + obj.radius:
            self.velocity.reflect_ip(n) #PYGAME FUNCTION, MAY CHANGE LATER TO THE PURE PHYSICS TM
            self.direction.reflect_ip(n) 
        
    
        
        