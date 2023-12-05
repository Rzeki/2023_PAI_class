import pygame as pg
from pygame import Vector2 as Vec2

class State:
    def __init__(self) -> None:
        pass
    
    def enter_state(self, agent) -> None:
        pass
    
    def execute_state(self, agent) -> None:
        pass
    
    def exit_state(self, agent) -> None :
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


#=====================STATE MACHINE================================================================================

class StateMachine:
    
    def __init__(self, owner) -> None:
        self._owner = owner
        self._current_state : State = None
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


