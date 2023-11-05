import pygame as pg
from Player import Player
from Obstacles import *
from Enemy import Enemy


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running : bool = True
        self.window : pg.Surface = pg.display.set_mode((1200, 900))
        self.player = Player(self.window)
        self.clock = pg.time.Clock()
        self.obstacles = [
            Obstacle(self.window, 500, 200, 50),
            Obstacle(self.window, 150, 100, 30),
            Obstacle(self.window, 900, 600, 70),
            Obstacle(self.window, 1000, 300, 50)
        ]
        self.walls = [
            Wall(self.window, Vec2(0, 0), Vec2(self.window.get_size()[0], 0)),
            Wall(self.window, Vec2(self.window.get_size()[0], 0), Vec2(self.window.get_size()[0], self.window.get_size()[1])),
            Wall(self.window, Vec2(self.window.get_size()[0], self.window.get_size()[1]), Vec2(0, self.window.get_size()[1])),
            Wall(self.window, Vec2(0, self.window.get_size()[1]), Vec2(0, 0))
        ]
        
    def run(self) -> None:
        enemy = Enemy(self.window, self.obstacles, self.walls, self.player)
        while self.running:
            dt : int = self.clock.tick(90)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.player.velocity += pg.Vector2.normalize(self.player.direction) * self.player.speed * dt
                self.player.velocity.x = pg.math.clamp(self.player.velocity.x, -1, 1)
                self.player.velocity.y = pg.math.clamp(self.player.velocity.y, -1, 1)
            if keys[pg.K_s]:
                self.player.velocity = pg.Vector2(0,0)
            if keys[pg.K_a]:
                self.player.rotate(-3)
            if keys[pg.K_d]:
                self.player.rotate(3)
                    
            #===================DRAWING=============================        
            self.window.fill(pg.Color(0,0,0)) # BACKGROUND
            for obst in self.obstacles:
                obst.draw()
            for wall in self.walls:
                wall.draw()
            self.player.draw()
            enemy.draw()
            
            #===================COLLISION===========================
            self.player.check_boundaries()
            for obst in self.obstacles:
                self.player.collide(obst)
            
            
            #===================MOVEMENT============================
            self.player.move(dt)
            enemy.update(dt)
            
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()