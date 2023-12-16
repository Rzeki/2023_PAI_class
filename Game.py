import pygame as pg
import util

from GameWorld import GameWorld
from Player import Player


class Game:
    def __init__(self) -> None:
        pg.init()
        self.window : pg.Surface = pg.display.set_mode((util.screen_wdth, util.screen_hgth))
        self.player = Player(self.window)
        self.clock = pg.time.Clock()
        self.game_world = GameWorld(self.window, self.player)
        
        self.start_screen = pg.image.load("assets\start.png")
        self.end_screen = pg.image.load("assets\over.png")
        self.running : bool = False
        self.game_over : bool = False
        
    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()    
#===========START MENU==================================================
            if not self.running and not self.game_over:
                self.window.blit(self.start_screen, pg.Vector2(0,0))
                pg.display.update()
                
                keys = pg.key.get_pressed()
                if keys[pg.K_SPACE]:
                    self.running = True
#===========GAME LOOP====================================================
            elif self.running:
                self.update()
#===========GAME OVER====================================================
            elif self.game_over:
                self.window.blit(self.end_screen, pg.Vector2(0,0))
                pg.display.update()
                
                keys = pg.key.get_pressed()
                if keys[pg.K_r]:
                    self.player.reset()
                    self.game_world = GameWorld(self.window, self.player)
                    self.running = True
                    self.game_over = False
                
                
    def update(self) -> None:
        
        dt : int = self.clock.tick(180)
                
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
                    self.game_over = True
                    self.running = False
            for bullet in self.game_world.bullets:
                bullet.collide(obst, self.game_world.bullets)
        
        
        #===================MOVEMENT============================
        self.game_world.update(dt)
        self.player.update(dt)
        
        
        #===================DEBUG============================
        # print(agent.velocity)        
                
                
        pg.display.update()
            
            
        
        
if __name__=="__main__":
    
    Game().run()