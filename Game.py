import pygame as pg
from GameWorld import GameWorld
from Player import Player
from Vehicle import Vehicle


class Game:
    def __init__(self) -> None:
        pg.init()
        self.running : bool = True
        self.window : pg.Surface = pg.display.set_mode((1200, 900))
        self.player = Player(self.window)
        self.clock = pg.time.Clock()
        self.game_world = GameWorld(self.window)
        
    def run(self) -> None:
        agent = Vehicle(self.game_world, self.player)
        agent.steering.start_behavior("wander")
        agent.steering.start_behavior("avoid walls")
        agent.steering.start_behavior("avoid obstacles")
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
            self.game_world.draw()
            self.player.draw()
            agent.draw()
            
            #===================COLLISION===========================
            self.player.check_boundaries()
            for obst in self.game_world.obstacles:
                self.player.collide(obst)
            
            
            #===================MOVEMENT============================
            self.player.update(dt)
            agent.update(dt)
            
            
                    
            pg.display.update()
            
        pg.quit()
            
        
        
if __name__=="__main__":
    Game().run()