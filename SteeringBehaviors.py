import pygame as pg
from pygame import Vector2 as Vec2
from GameObject import *
import util
import math

class SteeringBehaviors:
    
    def __init__(self, agent : MovingObject, player : MovingObject) -> None:
        self.agent : MovingObject = agent
        self.player : MovingObject = player
        
        #for some behaviors, see if it sticks
        self.add_agent_1 : MovingObject = None
        self.add_agent_2 : MovingObject = None
        self.world_point : Vec2 = None
        
        #for flee
        self.panic_distance : float = 600
        
        #for wander
        self.wander_radius : float = 10
        self.wander_distance : float = 10
        self.wander_jitter : float = 10
        self.wander_target : Vec2 = Vec2(self.wander_radius*math.cos(math.pi*2), self.wander_radius*math.sin(math.pi*2))

        #for obstacle detection
        self.min_detection_box_len : float = 80
        
        #for wall detection
        self.agent_feelers : [Vec2] = [Vec2(0.0), Vec2(0.0), Vec2(0.0)]
        self.feeler_length : float = 100
        
        #agent's final steering force
        self.steering_force : Vec2 = Vec2(0, 0)
        
        #TODO: make this more python'esque
        self.behaviors : dict = {
            "seek" : False, 
            "flee" : False, 
            "arrive" : False,
            "pursuit" : False,
            "evade" : False,
            "wander" : False,
            "avoid obstacles" : False,
            "avoid walls" : False,
            "separation" : False,
            "alignment" : False,
            "cohesion" : False,
            "interpose" : False,
            "hide" : False
            }
        self.seek_weight : float = 1
        self.flee_weight : float = 1
        self.arrive_weight : float = 1
        self.pursuit_weight : float = 1
        self.evade_weight : float = 0.1
        self.wander_weight : float = 1
        self.avoid_obst_weight : float = 30
        self.avoid_walls_weight : float = 30
        self.separation_weight : float = 20
        self.alignment_weight : float = 0.5
        self.cohesion_weight : float = 0.1
        self.interpose_weight : float = 1
        self.hide_weight : float = 3
    
    def calculate(self) -> Vec2:
        '''Calculate weighted truncated running sum w/ prioritization of currently enabled steering forces'''
        #this function is supposed to look like this, trust me -Ruby
        #use match statement goddamnit -Rzeki
        self.steering_force = Vec2(0,0)
        
        if self.behaviors["separation"] or self.behaviors["alignment"] or self.behaviors["cohesion"]:
            self.agent.tag_neighbors()
        
        if self.behaviors["avoid walls"]:
            force : Vec2 = self.avoid_walls()*self.avoid_walls_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["avoid obstacles"]:
            force : Vec2 = self.avoid_obstacles()*self.avoid_obst_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["evade"]:
            force : Vec2 = self.evade(self.player)*self.evade_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["flee"]:  
            force : Vec2 = self.flee(self.world_point)*self.flee_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        
        if self.behaviors["separation"]:
            force : Vec2 = self.separation(self.agent.game_world.moving_entities)*self.separation_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["alignment"]:
            force : Vec2 = self.alignment(self.agent.game_world.moving_entities)*self.alignment_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["cohesion"]:
            force : Vec2 = self.cohesion(self.agent.game_world.moving_entities)*self.cohesion_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        
        if self.behaviors["seek"]:  
            force : Vec2 = self.seek(self.world_point)*self.seek_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["arrive"]:
            force : Vec2 = self.arrive(self.world_point)*self.arrive_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["wander"]:
            force : Vec2 = self.wander()*self.wander_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["pursuit"]:
            force : Vec2 = self.pursuit(self.player)*self.pursuit_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        
        if self.behaviors["interpose"]:
            force : Vec2 = self.interpose(self.add_agent_1, self.add_agent_2)*self.interpose_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        if self.behaviors["hide"]:
            force : Vec2 = self.hide(self.player)*self.hide_weight
            if not self.accumulate_force(self.steering_force, force): return self.steering_force
        
        return self.steering_force
    
    #simplified for testing
    # def calculate(self) -> Vec2:
    #     return self.wander() + self.avoid_obstacles() + self.avoid_walls()

    def forward_comp(self) -> Vec2:
        '''Returns foreward component of agent's steering force'''
        return self.agent.direction.dot(self.steering_force)
    
    def side_comp(self) -> Vec2:
        '''Returns side component of agent's steering force'''
        return self.agent.side.dot(self.steering_force)
    
    def accumulate_force(self, running_total : Vec2, added_force : Vec2) -> bool :
        '''Chceck if newly added force does not excced agent's maximmum force'''
        remaining_mag : float = self.agent.max_force - running_total.length()
        if remaining_mag <= 0: return False
        
        if added_force.length() < remaining_mag:
            running_total += added_force
        else:
            running_total += added_force.normalize()*remaining_mag
        return True
    
    def start_behavior(self, behavior : str) -> None:
        '''Enable steering behavior'''
        self.behaviors[behavior] = True
    
    def end_behavior(self, behavior: str) -> None :
        '''Disable steering behavior'''
        self.behaviors[behavior] = False
       
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
    
    def pursuit(self, evader : MovingObject) -> Vec2:
        '''Pursuit target object.'''
        to_evader = evader.position - self.agent.position
        relative_heading = self.agent.direction.dot(evader.direction)
        
        if to_evader.dot(self.agent.direction) > 0 and relative_heading < -0.95:
            return self.seek(evader.position)
        else:
            look_ahead_time : float = to_evader.length()/(self.agent.max_speed+evader.speed())
            return self.seek(evader.position + evader.velocity*look_ahead_time)
    
    def evade(self, pursuer : MovingObject) -> Vec2 :
        '''Evade target object'''
        to_pursuer = pursuer.position - self.agent.position
        look_ahead_time : float = to_pursuer.length()/(self.agent.max_speed*3+pursuer.speed())
        return self.flee(pursuer.position + pursuer.velocity*look_ahead_time)
        
    def wander(self) -> Vec2:
        '''Random wandering behavior'''
        self.wander_target += Vec2(util.rand_clamped()*self.wander_jitter, util.rand_clamped()*self.wander_jitter)
        self.wander_target.normalize_ip()
        self.wander_target *= self.wander_radius
        
        target_local : Vec2 = self.wander_target + Vec2(self.wander_distance, 0)
        target_world : Vec2 = util.point_to_world_space(target_local, self.agent.direction, self.agent.side, self.agent.position)
        
        return target_world - self.agent.position
    
    def avoid_obstacles(self) -> Vec2:
        '''Avoid circular obstacles listed in GameWorld'''
        box_length : float = self.min_detection_box_len + (self.agent.speed()/self.agent.max_speed)*self.min_detection_box_len
        
        for obstacle in self.agent.game_world.obstacles:
            obstacle.tag = False
            range : Vec2 = obstacle.position - self.agent.position
            radius = box_length + obstacle.radius
            if range.length_squared() < radius**2:
                obstacle.tag = True
        
        closest_obstacle : GameObject = None
        dist_to_co : float = 99999
        co_in_local : Vec2 = None
        for obstacle in self.agent.game_world.obstacles:
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
        '''Avoid flat walls listen in GameWorld'''
        self.agent_feelers[0] = self.agent.position + self.feeler_length*self.agent.direction
        self.agent_feelers[1] = self.agent.position + self.feeler_length/2*self.agent.direction.rotate(math.pi/2*3.5)
        self.agent_feelers[1] = self.agent.position + self.feeler_length/2*self.agent.direction.rotate(math.pi/2*0.5)
        
        dist_to_closest_wall : float = util.MaxFloat
        closest_wall : GameObject = None
        closest_intersect_point : Vec2 = None
        steering_force : Vec2 = Vec2(0, 0)
        
        for feeler in self.agent_feelers:
            for wall in self.agent.game_world.walls:
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
            
    def separation(self, neighbors : list) -> Vec2:
        '''Steer agent away from neighbors'''
        steering_force : Vec2 = Vec2(0, 0)
        
        for entity in neighbors:
            # again, check !=
            if entity != self.agent and entity.tag and self.steering_force != Vec2(0,0):
                to_entity : Vec2 = self.agent.position - entity.position
                if to_entity != Vec2(0,0):
                    steering_force += Vec2.normalize(to_entity)/to_entity.length()
        
        return steering_force
    
    def alignment(self, neighbors : list) -> Vec2:
        '''Align neighbors directions'''
        average_heading : Vec2 = Vec2(0,0)
        neighbor_count : int = 0
        
        for entity in neighbors:
            if entity != self.agent and entity.tag:
                average_heading += entity.direction
                neighbor_count += 1
        
        if neighbor_count > 0:
            average_heading /= neighbor_count
            average_heading -= self.agent.direction
        
        return average_heading
    
    def cohesion(self, neighbors : list) -> Vec2:
        '''Move agent towards the center of mass of its neighbors'''
        center_of_mass : Vec2 = Vec2(0, 0)  
        steering_force : Vec2 = Vec2(0, 0)
        neighbor_count : int = 0
        
        for entity in neighbors:
            if entity != self.agent and entity.tag:
                center_of_mass += entity.position
                neighbor_count += 1
        
        if neighbor_count > 0:
            center_of_mass /= neighbor_count
            steering_force = self.seek(center_of_mass)
        
        return steering_force
            
    
    def interpose(self, agent_A : MovingObject, agent_B : MovingObject) -> Vec2:
        '''Move agent towards the mid-point between two other agents'''
        mid_point : Vec2 = (agent_A.position + agent_B.position)/2
        
        time_to_mid_point : float = Vec2.distance_to(self.agent.position, mid_point)/self.agent.max_speed
        
        A_pos : Vec2 = agent_A.position + agent_A.velocity*time_to_mid_point
        B_pos : Vec2 = agent_B.position + agent_B.velocity*time_to_mid_point
        
        mid_point = (A_pos+B_pos)/2
        
        return self.arrive(mid_point, 1)
    
    def hide(self, hunter : MovingObject) -> Vec2 :
        '''Hide from the hunter behind circular obstacles'''
        dist_to_closest : float = util.MaxFloat
        best_hiding_spot : Vec2 = None
        
        for obstacle in self.agent.game_world.obstacles:
            hiding_spot : Vec2 = self.get_hiding_pos(obstacle.position, obstacle.radius, hunter.position)
            
            dist : float = Vec2.distance_squared_to(hiding_spot, self.agent.position)
            
            if dist < dist_to_closest:
                dist_to_closest = dist
                best_hiding_spot = hiding_spot
        
        if dist_to_closest == util.MaxFloat:
            return self.evade(hunter)
        else: return self.arrive(best_hiding_spot, 1)
    
    def get_hiding_pos(self, obstacle_pos : Vec2, obstacle_radius : float, target_pos : Vec2) -> Vec2:
        dist_from_boundary : float = 60
        dist_away : float = obstacle_radius + dist_from_boundary
        
        to_obstacle : Vec2 = Vec2.normalize(obstacle_pos-target_pos)
        
        return (to_obstacle*dist_away) + obstacle_pos
                 
                        