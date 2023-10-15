import pygame as pg
from Gamer import Player

class Game:
    def __init__(self) -> None:
        pg.init()
        self.running = True
        self.window = pg.display.set_mode((900, 900))
        self.player = Player()
        
    def run(self):
        while self.running:
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    
            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.player.direction.x = 1
            if keys[pg.K_s]:
                self.player.direction.x = 0
            if keys[pg.K_a]:
                self.player.direction.rotate_ip(-0.1)
                self.player.body = pg.transform.rotate(self.player.body, -1)
            if keys[pg.K_d]:
                self.player.direction.rotate_ip(0.1)
                self.player.body = pg.transform.rotate(self.player.body, 1)
                    
           
                    
            self.window.fill(pg.Color(0,0,0))       
            self.player.draw()
            self.player.move()
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()