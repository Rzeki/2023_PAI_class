import pygame as pg
from Gamer import Player


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running = True
        self.window = pg.display.set_mode((900, 900))
        self.player = Player()
        self.clock = pg.time.Clock()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(90)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                # try:
                #     self.player.velocity = pg.Vector2.normalize(self.player.direction) * self.player.speed
                # except ValueError:
                self.player.velocity += pg.Vector2.normalize(self.player.direction) * self.player.speed * dt
            if keys[pg.K_s]:
                self.player.velocity = pg.Vector2(0,0)
            if keys[pg.K_a]:
                self.player.rotate(-3)
            if keys[pg.K_d]:
                self.player.rotate(3)
                    
           
                    
            self.window.fill(pg.Color(0,0,0))       
            self.player.draw(self.window)
            self.player.move(dt)
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()