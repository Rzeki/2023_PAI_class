import pygame as pg
from pygame import Vector2 as Vec2
from GameObject import MovingObject
from Vehicle import Vehicle
from StateMachine import *
import util

class Enemy(Vehicle):
    def __init__(self, game_world, player: MovingObject) -> None:
        super().__init__(game_world, player)
        
        self.body = pg.image.load("assets\Bomb_03.png")
        self.body.convert_alpha()
        
        self.state_machine = StateMachine(self)
        self.state_machine.change_state(StartState())
        
        self._time = pg.time.get_ticks() + random.randint(3000,6000)
    
    def draw(self) -> None:
        if util.DEBUG:
            pg.draw.circle(self.window, pg.Color(255, 0, 0, 100), self.position, self.radius)
            
        angle = self.direction.angle_to(pg.Vector2(0,-1))
        rotated_surface = pg.transform.rotozoom(self.body, angle, 1.0)
        rotated_surface_size = pg.Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.window.blit(rotated_surface, blit_position)
        
        if util.DEBUG:
            pg.draw.line(self.window, pg.Color(0, 0, 255), self.position, self.position + self.velocity*100, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.direction*50, 3)

    # def die(self, enemy_poll : list) -> None:
    #     enemy_poll.remove(self)


