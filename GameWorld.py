import pygame as pg
from pygame import Vector2 as Vec2
from Obstacles import *
from GameObject import *
from Enemy import Enemy


class GameWorld:
    def __init__(self, window : pg.surface, player : MovingObject) -> None:
        self.window = window
        self.window_w, self.window_h = window.get_size()
        self.player : MovingObject = player
        
        #container of all the moving entities
        self.moving_entities : list[Enemy] = [
            Enemy(self, self.player),
            Enemy(self, self.player),
            Enemy(self, self.player),
            Enemy(self, self.player),
            Enemy(self, self.player)
        ]
        #all circular obstacles
        self.obstacles = [
            Obstacle(window, 700, 300, 50),
            Obstacle(window, 700, 780, 50),
            Obstacle(window, 1200, 300, 50),
            Obstacle(window, 1200, 780, 50),
            Obstacle(window, 1600, 300, 50),
            Obstacle(window, 1600, 780, 50),
            Obstacle(window, 300, 780, 50),
            Obstacle(window, 300, 300, 50)
        ]
        #bounding walls
        self.walls = [
            Wall(window, Vec2(0, 0), Vec2(self.window_w, 0)),
            Wall(window, Vec2(self.window_w, 0), Vec2(self.window_w, self.window_h)),
            Wall(window, Vec2(self.window_w, self.window_h), Vec2(0, self.window_h)),
            Wall(window, Vec2(0, self.window_h), Vec2(0, 0))
        ]
        #for pausing motion
        self.pause : bool = False
        
        # for entity in self.moving_entities:
        #     entity.steering.start_behavior("wander")
        #     entity.steering.start_behavior("avoid walls")
        #     entity.steering.start_behavior("avoid obstacles")
        #     entity.steering.start_behavior("evade")
        #     entity.steering.start_behavior("hide")
            
    
    def update(self, dt : float) -> None :
        for entity in self.moving_entities:
            entity.update(dt)
            entity.state_machine.update()
        
        # for event in pg.event.get():
        #     if event.type == pg.USEREVENT:
        #         self.moving_entities.append(Enemy(self, self.player))
        keys = pg.key.get_pressed()
        if keys[pg.K_k]: #fix this
            self.moving_entities.append(Enemy(self, self.player))
            
        
    def draw(self) -> None :
        self.window.fill(pg.Color(0,0,0)) # BACKGROUND
        for obst in  self.obstacles:
            obst.draw()
        for wall in self.walls:
            wall.draw()
        for entity in self.moving_entities:
            entity.draw()