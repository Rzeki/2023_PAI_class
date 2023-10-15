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
                # try:
                #     self.player.velocity = pg.Vector2.normalize(self.player.direction) * self.player.speed
                # except ValueError:
                self.player.velocity += self.player.direction * self.player.speed
            if keys[pg.K_s]:
                self.player.velocity = pg.Vector2(0,0)
            if keys[pg.K_a]:
                self.player.direction.rotate_ip(-0.3)
                # self.player.velocity.rotate_ip(-0.1)
            if keys[pg.K_d]:
                self.player.direction.rotate_ip(0.3)
                # self.player.velocity.rotate_ip(0.1)
                    
           
                    
            self.window.fill(pg.Color(0,0,0))       
            self.player.draw(self.window)
            self.player.move()
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()