import pygame as pg
from GameObject import GameObject
from pygame import Vector2 as Vec2
import util
import math

class SteeringBehaviors:
    
    def __init__(self, agent : GameObject, player : GameObject) -> None:
        self.agent : GameObject = agent
        self.player : GameObject = player
        
        self.panic_distance : float = 150
        
        self.wander_radius : float = 10
        self.wander_distance : float = 10
        self.wander_jitter : float = 10
        self.wander_target : Vec2 = Vec2(self.wander_radius*math.cos(math.pi*2), self.wander_radius*math.sin(math.pi*2))
    
        self.min_detection_box_len : float = 40.0
        
        self.agent_feelers : [Vec2] = [Vec2(0.0), Vec2(0.0), Vec2(0.0)]
        self.feeler_length : float = 50
    
    def calculate(self) -> Vec2:
        return self.wander() + self.avoid_obstacles() + self.avoid_walls()

    def forward_comp(self) -> Vec2:
        pass
    
    def side_comp(self) -> Vec2:
        pass
    
    def seek(self, target : Vec2) -> Vec2:
        '''Seek target position.'''
        new_velocity : Vec2 = (target-self.agent.position)*self.agent.max_speed
        new_velocity.normalize_ip()
        
        return (new_velocity - self.agent.velocity)
    
    def flee(self, target : Vec2) -> Vec2:
        '''Flee if the target position is within panic distance.'''
        
        if(self.agent.position.distance_squared_to(target) > self.panic_distance*self.panic_distance) :
            return Vec2(0, 0)
        else :
            new_velocity : Vec2 = (self.agent.position - target)*self.agent.max_speed
            new_velocity.normalize_ip()
            
            return (new_velocity - self.agent.velocity)
    
    def arrive(self, target : Vec2, deceleration : int) -> Vec2:
        '''Arrive at target position.
            Decelaration: slow = 3, normal = 2, fast = 1'''
        to_target : Vec2 = target - self.agent.position
        dist : float = to_target.length()
        
        if dist > 0:
            deceleration_tweak : float = 0.3    #might move to class
            speed : float = dist / (deceleration * deceleration_tweak)
            speed = min(speed, self.agent.max_speed)
            
            new_velocity : Vec2 = to_target*speed/dist
            
            return (new_velocity - self.agent.velocity)
        else: return Vec2(0,0)
    
    def pursuit(self, evader : GameObject) -> Vec2:
        '''Pursuit target object.'''
        to_evader = evader.position - self.agent.position
        relative_heading = self.agent.direction.dot(evader.direction)
        
        if to_evader.dot(self.agent.direction) > 0 and relative_heading < -0.95:
            return self.seek(evader.position)
        else:
            look_ahead_time : float = to_evader.length()/(self.agent.max_speed+evader.speed)
            return self.seek(evader.position + evader.velocity*look_ahead_time)
    
    def evade(self, pursuer : GameObject) -> Vec2 :
        '''Evade target object'''
        to_pursuer = pursuer.position - self.agent.position
        look_ahead_time : float = to_pursuer.length()/(self.agent.max_speed+pursuer.speed)
        return self.flee(pursuer.position + pursuer.velocity*look_ahead_time)
        
    def wander(self) -> Vec2:
        self.wander_target += Vec2(util.rand_clamped()*self.wander_jitter, util.rand_clamped()*self.wander_jitter)
        self.wander_target.normalize_ip()
        self.wander_target *= self.wander_radius
        
        target_local : Vec2 = self.wander_target + Vec2(self.wander_distance, 0)
        target_world : Vec2 = util.point_to_world_space(target_local, self.agent.direction, self.agent.side, self.agent.position)
        
        return target_world - self.agent.position
    
    def avoid_obstacles(self) -> Vec2:
        box_length : float = self.min_detection_box_len + (self.agent.speed/self.agent.max_speed)*self.min_detection_box_len
        
        for obstacle in self.agent.obstacles:
            obstacle.tag = False
            range : Vec2 = obstacle.position - self.agent.position
            radius = box_length + obstacle.radius
            if range.length_squared() < radius*radius:
                obstacle.tag = True
        
        closest_obstacle : GameObject = None
        dist_to_co : float = 99999
        co_in_local : Vec2 = None
        for obstacle in self.agent.obstacles:
            if obstacle.tag:
                local_pos : Vec2 = util.point_to_local_space(obstacle.position, self.agent.direction, self.agent.side, self.agent.position)
                if local_pos.x >= 0:
                    expanded_rad : float = obstacle.radius + self.agent.radius
                    if abs(local_pos.y) < expanded_rad:
                        cX, cY = local_pos.x, local_pos.y
                        sqrt_part = math.sqrt(expanded_rad*expanded_rad - cY*cY)
                        ip : float = cX - sqrt_part
                        if ip <= 0.0:
                            ip = cX +sqrt_part
                        
                        if ip < dist_to_co:
                            dist_to_co = ip
                            closest_obstacle = obstacle
                            co_in_local = local_pos
        steering_force : Vec2 = None
        if closest_obstacle:
            multiplier : float = 1.0 + (box_length - co_in_local.x)/box_length
            breaking_weight : float = 2.0
            steering_force = Vec2(
                (closest_obstacle.radius - co_in_local.x)*breaking_weight,
                (closest_obstacle.radius - co_in_local.y)*multiplier
            )
            return util.vec_to_world_space(steering_force, self.agent.direction, self.agent.side)
        else: return Vec2(0.0, 0.0)
    
    def avoid_walls(self) -> Vec2:
        self.agent_feelers[0] = self.agent.position + self.feeler_length*self.agent.direction
        self.agent_feelers[1] = self.agent.position + self.feeler_length/2*self.agent.direction.rotate(math.pi/2*3.5)
        self.agent_feelers[1] = self.agent.position + self.feeler_length/2*self.agent.direction.rotate(math.pi/2*0.5)
        
        dist_to_closest_wall : float = 99999
        closest_wall : GameObject = None
        closest_intersect_point : Vec2 = None
        steering_force : Vec2 = Vec2(0, 0)
        
        for feeler in self.agent_feelers:
            for wall in self.agent.walls:
                intersect, dist, point = util.line_intersect(self.agent.position, feeler, wall.start, wall.end)
                if intersect:
                    if dist and point and dist < dist_to_closest_wall:
                        dist_to_closest_wall = dist
                        closest_wall = wall
                        closest_intersect_point = point
        
            if closest_wall:
                overshoot : Vec2 = feeler - closest_intersect_point
                steering_force = closest_wall.normal * overshoot.length()
        
        return steering_force
            
                        
                        
                        