import pygame as pg
from pygame import Vector2 as Vec2
from Obstacles import *
from GameObject import *
from Vehicle import Vehicle


class GameWorld:
    def __init__(self, window : pg.surface, player : MovingObject) -> None:
        self.window = window
        self.window_w, self.window_h = window.get_size()
        self.player : MovingObject = player
        #container of all the moving entities
        self.moving_entities : list[MovingObject] = [
            Vehicle(self, self.player),
            Vehicle(self, self.player),
            Vehicle(self, self.player),
            Vehicle(self, self.player),
            Vehicle(self, self.player)
        ]
        #all circular obstacles
        self.obstacles = [
            Obstacle(window, 500, 200, 70),
            Obstacle(window, 150, 100, 50),
            Obstacle(window, 1600, 900, 70),
            Obstacle(window, 1000, 300, 100)
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
        
        #in book used for user inputted position
        #but we can and I guess hsould use it for enemy steering
        #it will come up later when coding proper simulation behavior
        self.crosshair : Vec2 = Vec2(self.window_w/2, self.window_h/2)
        
        for entity in self.moving_entities:
            entity.steering.start_behavior("wander")
            entity.steering.start_behavior("avoid walls")
            entity.steering.start_behavior("avoid obstacles")
            entity.steering.start_behavior("evade")
            
    
    def update(self, dt : float) -> None :
        for entity in self.moving_entities:
            entity.update(dt)
        
    def draw(self) -> None :
        self.window.fill(pg.Color(0,0,0)) # BACKGROUND
        for obst in  self.obstacles:
            obst.draw()
        for wall in self.walls:
            wall.draw()
        for entity in self.moving_entities:
            entity.draw()