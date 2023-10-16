import pygame as pg

class GameObject:
    def __init__(self) -> None:
        self.position = pg.Vector2(0,0)
        self.direction = pg.Vector2(0,0)
        self.velocity = pg.Vector2(0,0)
        self.speed = 0.001
        self.radius = 50
        self.clock = pg.time.Clock()
        
    def draw(self, surface) -> None:
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        
    def move(self, dt) -> None:
        # self.velocity = self.direction * self.speed
        self.position += self.velocity * dt
        