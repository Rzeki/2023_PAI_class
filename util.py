import random
from pygame import Vector2 as Vec2

DEBUG : bool = True

# WHY WON"T IT FXXXX WORK
dir : dict = {
    "UP": (0,-1),
    "DOWN": (0,1),
    "LEFT": (-1,0),
    "RIGHT": (1,0),
    "ZERO": (0,0)
}

def rand_clamped() -> float:
    return random.random()-random.random()

def wrap_around(pos : Vec2, max_x : int, max_y : int) -> None:
    if pos.x > max_x: pos.x = 0.0
    if pos.x < 0: pos.x = max_x
    if pos.y < 0: pos.y = max_y
    if pos.y > max_y: pos.y = 0.0

def vec_perp(vec : Vec2) -> Vec2:
    return Vec2(1, -vec.x/vec.y)

def point_to_world_space(point : Vec2, agent_dir : Vec2, agent_side : Vec2, agent_pos : Vec2) -> Vec2:
    return Vec2(
        agent_dir.x*point.x + agent_side.x*point.y + agent_pos.x,
        agent_dir.y*point.x + agent_side.y*point.y + agent_pos.y
    )
    # transform matrix
    # dir.x     dir.y     0
    # side.x    side.y    0
    # pos.x     pos.y  1