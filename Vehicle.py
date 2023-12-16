import pygame as pg
from pygame import Vector2 as Vec2

import util
from GameObject import MovingObject
from SteeringBehaviors import SteeringBehaviors  
import random  


class Vehicle(MovingObject):

    def __init__(self, game_world, player : MovingObject) -> None:
        super().__init__(game_world.window)
        self.game_world = game_world
        self.mass = 2000
        self.radius = 20
        self.position = random.choice([Vec2(60,60), Vec2(util.screen_wdth - 60, 60), Vec2(60, util.screen_hgth - 60), Vec2(util.screen_wdth - 60, util.screen_hgth - 60)])
        self.direction = Vec2(util.dir["UP"])
        self.side = Vec2(util.dir["RIGHT"])
        self.steering = SteeringBehaviors(self, player)
        
        self.neighborhood_radius = 200
    
    def update(self, dt : float) -> None:
        steering_force : Vec2 = self.steering.calculate()
        acceleration : Vec2 = steering_force/self.mass
        
        self.velocity += acceleration * dt
        self.velocity.x = pg.math.clamp(self.velocity.x, -self.max_speed, self.max_speed)
        self.velocity.y = pg.math.clamp(self.velocity.y, -self.max_speed, self.max_speed)
        
        self.position += self.velocity*dt
        
        if self.velocity.length_squared() > 0.00001:   #check if needed
            self.direction = self.velocity.normalize()
            self.side = util.vec_perp(self.direction)
            
            # self.smooth_direction.insert(0, self.direction)
            # if len(self.smooth_direction) > self.num_last_directions:
            #     self.smooth_direction.pop()
            
            # test = Vec2(0,0)
            # for v in self.smooth_direction:
            #     test.x += v.x
            #     test.y += v.y
            # self.average_direction = test/len(self.smooth_direction)
            
                
        
        # for testing
        # wdth, hgth = self.window.get_size()
        # util.wrap_around(self.position, wdth, hgth)
    
    def draw(self) -> None:
        if util.DEBUG:
            pg.draw.circle(self.window, pg.Color(255, 0, 0, 100), self.position, self.radius)
            pg.draw.line(self.window, pg.Color(0, 0, 255), self.position, self.position + self.velocity*100, 3)
            pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.direction*50, 3)
            # pg.draw.line(self.window, pg.Color(255, 0, 255), self.position, self.position + self.steering.wander_target, 3)
            # pg.draw.circle(self.window, pg.Color(255, 0, 255), 
            #                self.position + self.steering.wander_distance,
            #                self.steering.wander_radius)
    
    def tag_neighbors(self) -> None:
        '''Tag other agents within radius'''
        for entity in self.game_world.moving_entities:
            entity.tag = False

            to_entity : Vec2 = entity.position - self.position
            range : float = self.neighborhood_radius + entity.radius
            
            #check if != works
            if entity is not self and to_entity.length_squared() < range*range:
                entity.tag = True
                
    def count_neighbors(self) -> int:
        '''count other agents within radius'''
        counter = 0
        for entity in self.game_world.moving_entities:
            entity.tag = False      
            to_entity : Vec2 = entity.position - self.position
            range : float = self.neighborhood_radius + entity.radius
            #check if != works
            if entity is not self and to_entity.length_squared() < range*range:
                counter += 1  
        
        return counter