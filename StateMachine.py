import pygame as pg
from pygame import Vector2 as Vec2
import random
import util
            

class State:
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        pass
    
    def execute_state(self, agent) -> None:
        pass
    
    def exit_state(self, agent) -> None:
        pass
    
class StartState(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("avoid obstacles")
        agent.steering.start_behavior("avoid walls")
        agent.steering.start_behavior("separation")

        pass
    
    def execute_state(self, agent) -> None:
        agent.state_machine.change_state(Wander())
        pass
    
    def exit_state(self, agent) -> None:
        pass
    
class GlobalState(State):
    def __init__(self) -> None:
        super().__init__()    
        
    def enter_state(self, agent) -> None:
        pass
    
    def execute_state(self, agent) -> None:
        pass
    
    def exit_state(self, agent) -> None :
        pass


class Hide(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("hide")
        pass
    
    def execute_state(self, agent) -> None:
        pass
    
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("hide")
        pass
    
class Pursuit(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("pursuit")
        pass
    
    def execute_state(self, agent) -> None:
        pass
    
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("pursuit")
        pass
    
class Evade(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("evade")
        pass
    
    def execute_state(self, agent) -> None:
        if agent.steering.player.position.distance_to(agent.position) > agent.steering.panic_distance:
            if util.DEBUG:
                agent.body.fill((255, 255, 255, 255))
            agent.state_machine.change_state(Group())
        
        pass
    
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("evade")
        pass
    
class Wander(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("wander")
        pass
    
    def execute_state(self, agent) -> None:
        if agent.steering.player.position.distance_to(agent.position) < agent.steering.evade_distance:
            agent.group_timer = pg.time.get_ticks() + 10000
            if util.DEBUG:
                agent.body.fill((170, 170, 170, 255))
            agent.state_machine.change_state(Evade())
            
     
        if pg.time.get_ticks() > agent.group_timer:
            if util.DEBUG:
                agent.body.fill((255, 255, 255, 255))
            agent.state_machine.change_state(Group())
            
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("wander")
        pass
    
    
class Group(State):
    def __init__(self) -> None:   
        pass
    
    def enter_state(self, agent) -> None:
        agent.group_timer = pg.time.get_ticks() + 10000
        agent.steering.start_behavior("separation")
        agent.steering.start_behavior("alignment")
        agent.steering.start_behavior("cohesion")
        agent.steering.start_behavior("hide")
    
    
    def execute_state(self, agent) -> None: 
        neighbours: list = agent.get_neighbors()  
        for neighbour in neighbours:
            if not neighbour.state_machine.is_in_state("Group"):
                neighbours.remove(neighbour)
        
        clr = (random.randint(0,255),random.randint(0,255),random.randint(0,255),255)
        
        if len(neighbours) >= 3: 
            for neighbour in neighbours:      
                if util.DEBUG:
                    neighbour.body.fill(clr)
                neighbour.state_machine.change_state(Pursuit())
        
            if util.DEBUG:
                agent.body.fill(clr)
            agent.state_machine.change_state(Pursuit())
        
    
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("hide")
        pass

#=====================STATE MACHINE================================================================================

class StateMachine:
    
    def __init__(self, owner) -> None:
        self._owner = owner
        self._current_state : State = StartState()
        self._previous_state : State = None
        self._global_state : State = None
        
    def set_current_state(self, state : State) -> None : self._current_state = state
    def get_current_state(self) -> State : return self._current_state
    
    def set_global_state(self, state : State) -> None : self._global_state = state
    def get_global_state(self) -> State : return self._global_state
    
    def set_previous_state(self, state : State) -> None : self._previous_state = state
    def get_previous_state(self) -> State : self._previous_state
    
    def update(self) -> None :
        if self._global_state:
            self._global_state.execute_state(self._owner)
        
        if self._current_state:
            self._current_state.execute_state(self._owner)
            
            
        # keys = pg.key.get_pressed()
        # if keys[pg.K_n]: #fix this
        #     self.change_state(Pursuit())
            
        
            
            
    def change_state(self, new_state : State) -> None :
        if self._current_state and new_state:
            self._previous_state = self._current_state
            self._current_state.exit_state(self._owner)
            self._current_state = new_state
            self._current_state.enter_state(self._owner)
    
    def revert_to_previous_state(self) -> None :
        self.change_state(self._previous_state)
    
    def is_in_state(self, query_state : str) -> bool :
        if query_state == self._current_state.__class__.__name__:
            return True
        else : return False


