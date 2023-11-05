import pygame as pg
from pygame import Vector2 as Vec2

import util
from GameObject import MovingObject
from GameWorld import GameWorld
from SteeringBehaviors import SteeringBehaviors    


class Vehicle(MovingObject):

    def __init__(self, game_world : GameWorld, player : MovingObject) -> None:
        super().__init__(game_world.window)
        self.game_world = game_world
        self.mass = 500
        self.radius = 20
        self.position = pg.Vector2([ z-30 for z in self.window.get_size() ])
        self.direction = Vec2(util.dir["UP"])
        self.side = Vec2(util.dir["RIGHT"])
        self.steering = SteeringBehaviors(self, player)
    
    def update(self, dt : float) -> None:
        steering_force : Vec2 = self.steering.calculate()
        acceleration : Vec2 = steering_force/self.mass
        
        self.velocity += acceleration * dt
        self.velocity.x = pg.math.clamp(self.velocity.x, -1, 1)
        self.velocity.y = pg.math.clamp(self.velocity.y, -1, 1)
        
        self.position += self.velocity*dt
        
        if self.velocity.length_squared() > 0.00000001:   #check if needed
            self.direction = self.velocity.normalize()
            self.side = util.vec_perp(self.direction)
    
    def draw(self) -> None:
        pg.draw.circle(self.window, pg.Color(255, 0, 0, 100), self.position, self.radius)
        if util.DEBUG:
            pg.draw.line(self.window, pg.Color(0, 0, 255), self.position, self.position + self.velocity*100, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.direction*50, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.steering.wander_target, 3)
            # pg.draw.circle(self.window, pg.Color(255, 0, 255), 
            #                self.position + self.steering.wander_distance,
            #                self.steering.wander_radius)
            