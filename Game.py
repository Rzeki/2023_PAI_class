import pygame as pg
import util

from GameWorld import GameWorld
from Player import Player


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running : bool = False
        self.window : pg.Surface = pg.display.set_mode((util.screen_wdth, util.screen_hgth))
        self.player = Player(self.window)
        self.clock = pg.time.Clock()
        self.game_world = GameWorld(self.window, self.player)
        
        self.start_screen = pg.image.load("assets\start.png")
        self.end_screen = pg.image.load("assets\over.png")
        
    # def start(self) -> None:
                
        
    def run(self) -> None:
        
        while not self.running:
            self.window.blit(self.start_screen, pg.Vector2(0,0))
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.running = True
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
        
        while self.running:
            dt : int = self.clock.tick(180)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    
            #===================DRAWING=============================        
            self.game_world.draw()
            self.player.draw()
            
            #===================COLLISION===========================
            self.player.check_boundaries()
            for enemy in self.game_world.moving_entities:
                enemy.check_boundaries()
                for other_enemy in self.game_world.moving_entities:
                    if enemy is not other_enemy:
                        enemy.collide_and_push(other_enemy)
                        
                
            for obst in self.game_world.obstacles:
                self.player.collide(obst)
                for enemy in self.game_world.moving_entities:
                    enemy.collide(obst)
                    if self.player.collide(enemy):
                        self.running = False #TODO: Game over
                for bullet in self.game_world.bullets:
                    bullet.collide(obst, self.game_world.bullets)
            
            
            #===================MOVEMENT============================
            self.game_world.update(dt)
            self.player.update(dt)
            
            
            #===================DEBUG============================
            # print(agent.velocity)        
                    
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()