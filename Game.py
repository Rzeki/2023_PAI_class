import pygame as pg
from Player import Player
from Wall import Wall


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running : bool = True
        self.window : pg.Surface = pg.display.set_mode((1200, 900))
        self.player = Player()
        self.clock = pg.time.Clock()
        self.walls = []
        self.walls = [
            Wall(500, 200, 50),
            Wall(150, 100, 30),
            Wall(900, 600, 70),
            Wall(1000, 300, 50)
        ]
        
    def run(self) -> None:
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
            for wall in self.walls:
                wall.draw(self.window)
            self.player.draw(self.window)
            
            #===================COLLISION===========================
            self.player.check_boundaries(self.window)
            for wall in self.walls:
                self.player.collide(wall)
            
            
            #===================MOVEMENT============================
            self.player.move(dt)
            
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()