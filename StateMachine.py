import pygame as pg
from pygame import Vector2 as Vec2
            

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
    
class Evade(State):
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        agent.steering.start_behavior("evade")
        pass
    
    def execute_state(self, agent) -> None:
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
        if agent.steering.player.position.distance_to(agent.position) < agent.steering.panic_distance:
            agent.group_timer = pg.time.get_ticks() + 20000
            agent.state_machine.change_state(Evade())
        
    
    def exit_state(self, agent) -> None:
        agent.steering.end_behavior("wander")
        pass

#=====================STATE MACHINE================================================================================

class StateMachine:
    
    def __init__(self, owner) -> None:
        self._owner = owner
        self._current_state : State = StartState()
        self._previous_state : State = None
        self._global_state : State = None
        self.group_timer = pg.time.set_timer(pg.USEREVENT, 1000)
        
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
            
        if pg.time.get_ticks() > self._owner.group_timer:
            self.change_state(Hide())
            
        
            
            
    def change_state(self, new_state : State) -> None :
        if self._current_state and new_state:
            self._previous_state = self._current_state
            self._current_state.exit_state(self._owner)
            self._current_state = new_state
            self._current_state.enter_state(self._owner)
    
    def revert_to_previous_state(self) -> None :
        self.change_state(self._previous_state)
    
    def is_in_state(self, query_state : State) -> bool :
        if query_state == self._current_state:
            return True
        else : return False


