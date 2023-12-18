import pygame as pg
from pygame import Vector2 as Vec2
import util

from GameObject import *
from Bullet import Bullet

class Player(MovingObject):
    def __init__(self, window : pg.Surface) -> None:
        super().__init__(window)
        self.position = pg.Vector2([ z / 2 for z in self.window.get_size() ])
        self.direction = Vec2(util.dir["UP"])
        self.body = pg.image.load("assets\spaceship.png")
        self.crosshair = pg.image.load("assets\crosshair.png")
        self.cursor_img_rect = self.crosshair.get_rect()
        self._speed = 0.0001 #fix this so its not needed
        self.shoot_cooldown = pg.time.get_ticks() + 500
        self.mouse_distance = pg.mouse.get_pos() - self.position
              
    def draw(self) -> None:
        if util.DEBUG:
            pg.draw.circle(self.window, pg.Color(255, 255, 0), self.position, self.radius)
            
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.window.blit(rotated_surface, blit_position)
        mouse_pos = Vec2(pg.mouse.get_pos())
        self.window.blit(self.crosshair, pg.Rect(mouse_pos.x - self.cursor_img_rect.width/2, mouse_pos.y - self.cursor_img_rect.height/2, self.cursor_img_rect.width, self.cursor_img_rect.height))
        
        
        if util.DEBUG:
            pg.draw.line(self.window, pg.Color(0, 0, 255), self.position, self.position + self.velocity * 100, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.direction * 50, 3)
        
    # def rotate(self, manuverability : int) -> None:
    #     self.direction.rotate_ip(manuverability)
        
    def update(self, dt: float) -> None:
        super().update(dt)
        
        self.mouse_distance = pg.mouse.get_pos() - self.position
        if self.mouse_distance != Vec2(0, 0):
            self.direction = self.mouse_distance.normalize()
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity += pg.Vector2.normalize(self.direction) * self._speed * dt
            self.velocity.x = pg.math.clamp(self.velocity.x, -1, 1)
            self.velocity.y = pg.math.clamp(self.velocity.y, -1, 1)
        if keys[pg.K_s]:
            self.velocity = pg.Vector2(0,0)
        # if keys[pg.K_a]:
        #     self.rotate(-1)
        # if keys[pg.K_d]:
        #     self.rotate(1)
    
    def reset(self):
        self.position = pg.Vector2([ z / 2 for z in self.window.get_size() ])
        self.direction = Vec2(util.dir["UP"])
        self.velocity = Vec2(util.dir["ZERO"])
        

        