import random
from pygame import Vector2 as Vec2

DEBUG : bool = True
screen_wdth, screen_hgth = 1920, 1080

MaxFloat : float = 99999

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

def random_position() -> Vec2:
    return Vec2(random.randint(1, screen_wdth), random.randint(1, screen_hgth))

# def wrap_around(pos : Vec2, max_x : int, max_y : int) -> None:
#     if pos.x > max_x: pos.x = 0.0
#     if pos.x < 0: pos.x = max_x
#     if pos.y < 0: pos.y = max_y
#     if pos.y > max_y: pos.y = 0.0

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
    # pos.x     pos.y     1
    
def point_to_local_space(point : Vec2, agent_dir : Vec2, agent_side : Vec2, agent_pos : Vec2) -> Vec2:
    Tx : float = -agent_pos.dot(agent_dir)
    Ty : float = -agent_pos.dot(agent_side)
    
    return Vec2(
        agent_dir.x*point.x + agent_dir.y*point.y + Tx,
        agent_side.x*point.x + agent_side.y*point.y + Ty
    )
    
    # transform matrix
    # dir.x     side.x    0
    # dir.y     side.y    0
    # Tx        Ty        1
    
def vec_to_world_space(vec : Vec2, agent_dir : Vec2, agent_side : Vec2) -> Vec2:
    return Vec2(
        agent_dir.x*vec.x + agent_side.x*vec.y,
        agent_dir.y*vec.x + agent_side.y*vec.y
    )
    # transform matrix
    # dir.x     dir.y     0
    # side.x    side.y    0
    # 0         0         1

def line_intersect(A : Vec2, B : Vec2, C : Vec2, D : Vec2) -> (bool, float, Vec2):
    rTop : float = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
    rBot : float = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
    sTop : float = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)
    sBot : float = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
    
    if rBot == 0 or sBot == 0:
        return False, None, None

    r, s = rTop/rBot, sTop/sBot
    
    if r>0 and r<1 and s>0 and s<1:
        return True, Vec2.distance_to(A, B)*r, A+r*(B-A)
    else: return False, 0, None