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
    
    def calculate(self) -> Vec2:
        return self.wander()

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
        
        