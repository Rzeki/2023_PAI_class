import pygame as pg
from pygame import Vector2 as Vec2
from Obstacles import *
from GameObject import *
from Enemy import Enemy
from Bullet import Bullet


class GameWorld:
    def __init__(self, window : pg.surface, player : MovingObject) -> None:
        self.window = window
        self.window_w, self.window_h = window.get_size()
        self.player : MovingObject = player
        self.spawnrate = pg.time.get_ticks() + 500
        
        #container of all the moving entities
        self.moving_entities : list[Enemy] = [Enemy(self, self.player) for _ in range(0,5) ]
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
        #container of bullets
        self.bullets : list[Bullet] = []
        self.can_shoot : bool = True
        

    
    def update(self, dt : float) -> None :
        
        if pg.time.get_ticks() > self.player.shoot_cooldown:
            self.can_shoot = True 
            
        if pg.time.get_ticks() > self.spawnrate:
            self.spawnrate = pg.time.get_ticks() + 500
            self.moving_entities.append(Enemy(self, self.player))
            
        if pg.mouse.get_pressed()[0]:
            if self.can_shoot:
                self.can_shoot = False
                self.player.shoot_cooldown = pg.time.get_ticks() + 50
                self.bullets.append(Bullet(self.window, self.player.position, self.player.direction))
            # #SHOTGUN
            # self.bullets.append(Bullet(self.window, self.player.position, self.player.direction.rotate(5)))
            # self.bullets.append(Bullet(self.window, self.player.position, self.player.direction.rotate(-5)))
        
        for entity in self.moving_entities:
            entity.update(dt)
            entity.state_machine.update()
            for bullet in self.bullets:     #enemy dies hit by a bullet
                if bullet.collide(entity, self.bullets) and (entity in self.moving_entities):
                    self.moving_entities.remove(entity)
        for bullet in self.bullets:
            bullet.update(dt)
            
        
    def draw(self) -> None :
        self.window.fill(pg.Color(0,0,0)) # BACKGROUND
        for obst in  self.obstacles:
            obst.draw()
        for wall in self.walls:
            wall.draw()
        for entity in self.moving_entities:
            entity.draw()
        for bullet in self.bullets:
            bullet.draw()