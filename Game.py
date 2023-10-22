import pygame as pg
from Player import Player


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running : bool = True
        self.window : pg.Surface = pg.display.set_mode((1200, 900))
        self.player = Player()
        self.clock = pg.time.Clock()
        
    def run(self) -> None:
        while self.running:
            dt : int = self.clock.tick(90)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.player.velocity += pg.Vector2.normalize(self.player.direction) * self.player.speed * dt
            if keys[pg.K_s]:
                # self.player.velocity -= pg.Vector2.normalize(self.player.direction) * self.player.speed * dt
                self.player.velocity = pg.Vector2(0,0)
            if keys[pg.K_a]:
                self.player.rotate(-3)
            if keys[pg.K_d]:
                self.player.rotate(3)
                    
            self.player.check_boundaries(self.window)
                    
            self.window.fill(pg.Color(0,0,0))       
            self.player.draw(self.window)
            self.player.move(dt)
            
            print(self.player.velocity)
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()