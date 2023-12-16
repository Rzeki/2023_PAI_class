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
        
        self.state_machine = StateMachine(self)
        self.state_machine.change_state(StartState())
        
        self.group_timer = pg.time.get_ticks() + 20000
    
    def draw(self) -> None:
        if util.DEBUG:
            super().draw()
        self.window.blit(self.body, self.position - Vec2(self.radius-2.5, self.radius-2.5))

    # def die(self, enemy_poll : list) -> None:
    #     enemy_poll.remove(self)


