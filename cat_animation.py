#!/usr/bin/env python3
"""
Cat Animation Module
Provides fluid, anatomically correct cat movement with smooth limb articulation
"""

import math
import random
import time
from typing import Tuple, List, Dict

class CatLimb:
    """Represents a single cat limb with proper joint constraints"""
    
    def __init__(self, name: str, base_pos: Tuple[float, float], length: float, 
                 angle: float = 0, joint_limits: Tuple[float, float] = (-45, 45)):
        self.name = name
        self.base_pos = list(base_pos)
        self.length = length
        self.angle = angle
        self.joint_limits = joint_limits
        self.target_angle = angle
        self.animation_speed = 0.1
        
    def update(self, dt: float):
        """Smoothly update limb angle towards target"""
        angle_diff = self.target_angle - self.angle
        self.angle += angle_diff * self.animation_speed * dt
        
    def set_target_angle(self, angle: float):
        """Set target angle within joint limits"""
        self.target_angle = max(self.joint_limits[0], min(self.joint_limits[1], angle))
        
    def get_end_pos(self) -> Tuple[float, float]:
        """Calculate end position of limb"""
        end_x = self.base_pos[0] + math.cos(math.radians(self.angle)) * self.length
        end_y = self.base_pos[1] + math.sin(math.radians(self.angle)) * self.length
        return (end_x, end_y)
        
    def get_mid_pos(self) -> Tuple[float, float]:
        """Calculate middle position of limb for drawing"""
        mid_x = self.base_pos[0] + math.cos(math.radians(self.angle)) * self.length * 0.5
        mid_y = self.base_pos[1] + math.sin(math.radians(self.angle)) * self.length * 0.5
        return (mid_x, mid_y)

class CatBody:
    """Main cat body with all limbs and smooth movement"""
    
    def __init__(self, x: float, y: float):
        # Body dimensions
        self.x = x
        self.y = y
        self.width = 60
        self.height = 40
        self.body_angle = 0
        
        # Movement
        self.target_x = x
        self.target_y = y
        self.speed = 0.8
        self.walk_cycle = 0
        self.walk_speed = 2.0
        
        # Limb definitions (relative to body center)
        self.limbs = {
            'front_left': CatLimb('front_left', (-25, -15), 25, 0, (-30, 30)),
            'front_right': CatLimb('front_right', (-25, 15), 25, 0, (-30, 30)),
            'back_left': CatLimb('back_left', (25, -15), 25, 0, (-30, 30)),
            'back_right': CatLimb('back_right', (25, 15), 25, 0, (-30, 30))
        }
        
        # Tail segments
        self.tail_segments = []
        for i in range(5):
            self.tail_segments.append({
                'angle': 0,
                'length': 15 - i * 2,
                'target_angle': 0
            })
        
        # Head
        self.head_angle = 0
        self.head_target_angle = 0
        
        # Animation state
        self.state = 'idle'  # idle, walking, running, sitting
        self.state_timer = 0
        self.blink_timer = 0
        self.ear_twitch_timer = 0
        
    def update(self, dt: float):
        """Update cat animation and movement"""
        # Update walk cycle
        self.walk_cycle += self.walk_speed * dt
        
        # Smooth movement towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:
            self.state = 'walking'
            # Move towards target
            move_x = (dx / distance) * self.speed * dt
            move_y = (dy / distance) * self.speed * dt
            self.x += move_x
            self.y += move_y
            
            # Update body angle to face movement direction
            target_angle = math.degrees(math.atan2(dy, dx))
            angle_diff = target_angle - self.body_angle
            # Normalize angle difference
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360
            self.body_angle += angle_diff * 0.1 * dt
            
            # Animate limbs for walking
            self._animate_walking(dt)
        else:
            self.state = 'idle'
            self._animate_idle(dt)
        
        # Update head movement
        self._update_head(dt)
        
        # Update tail
        self._update_tail(dt)
        
        # Update timers
        self.state_timer += dt
        self.blink_timer += dt
        self.ear_twitch_timer += dt
        
        # Random state changes
        if self.state_timer > random.uniform(3, 8):
            self._change_random_state()
            self.state_timer = 0
            
    def _animate_walking(self, dt: float):
        """Animate limbs for walking motion"""
        cycle = self.walk_cycle
        
        # Front limbs (opposite phase)
        front_left_angle = math.sin(cycle) * 20
        front_right_angle = math.sin(cycle + math.pi) * 20
        
        # Back limbs (opposite phase from front)
        back_left_angle = math.sin(cycle + math.pi) * 20
        back_right_angle = math.sin(cycle) * 20
        
        # Apply angles with smooth transitions
        self.limbs['front_left'].set_target_angle(front_left_angle)
        self.limbs['front_right'].set_target_angle(front_right_angle)
        self.limbs['back_left'].set_target_angle(back_left_angle)
        self.limbs['back_right'].set_target_angle(back_right_angle)
        
        # Update all limbs
        for limb in self.limbs.values():
            limb.update(dt)
            
    def _animate_idle(self, dt: float):
        """Animate limbs for idle state"""
        # Gentle swaying motion
        sway = math.sin(self.state_timer * 0.5) * 5
        
        for limb_name, limb in self.limbs.items():
            if 'left' in limb_name:
                limb.set_target_angle(sway)
            else:
                limb.set_target_angle(-sway)
            limb.update(dt)
            
    def _update_head(self, dt: float):
        """Update head movement and orientation"""
        # Head follows body angle with slight delay
        target_head_angle = self.body_angle + random.uniform(-10, 10)
        head_diff = target_head_angle - self.head_angle
        
        # Normalize angle difference
        while head_diff > 180:
            head_diff -= 360
        while head_diff < -180:
            head_diff += 360
            
        self.head_angle += head_diff * 0.05 * dt
        
    def _update_tail(self, dt: float):
        """Update tail movement with wave-like motion"""
        base_tail_angle = self.body_angle + 180  # Tail points opposite to body
        
        for i, segment in enumerate(self.tail_segments):
            # Wave motion that propagates down the tail
            wave_offset = i * 0.3
            wave_amplitude = 15 - i * 2
            target_angle = base_tail_angle + math.sin(self.state_timer * 2 + wave_offset) * wave_amplitude
            
            # Smooth transition
            angle_diff = target_angle - segment['angle']
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360
                
            segment['angle'] += angle_diff * 0.1 * dt
            
    def _change_random_state(self):
        """Randomly change cat state"""
        if random.random() < 0.3:
            # Random movement
            self.target_x += random.uniform(-100, 100)
            self.target_y += random.uniform(-100, 100)
            
            # Keep within bounds
            self.target_x = max(50, min(950, self.target_x))
            self.target_y = max(50, min(650, self.target_y))
            
    def set_target(self, x: float, y: float):
        """Set target position for cat to walk to"""
        self.target_x = x
        self.target_y = y
        
    def get_drawing_data(self) -> Dict:
        """Get all data needed for drawing the cat"""
        # Calculate limb positions relative to body
        limb_positions = {}
        for name, limb in self.limbs.items():
            # Transform limb base position by body rotation
            cos_a = math.cos(math.radians(self.body_angle))
            sin_a = math.sin(math.radians(self.body_angle))
            
            # Rotate limb base position
            rotated_x = limb.base_pos[0] * cos_a - limb.base_pos[1] * sin_a
            rotated_y = limb.base_pos[0] * sin_a + limb.base_pos[1] * cos_a
            
            # Add body position
            world_base = (self.x + rotated_x, self.y + rotated_y)
            
            # Calculate end position
            end_pos = limb.get_end_pos()
            world_end = (self.x + rotated_x + (end_pos[0] - limb.base_pos[0]), 
                        self.y + rotated_y + (end_pos[1] - limb.base_pos[1]))
            
            limb_positions[name] = {
                'base': world_base,
                'end': world_end,
                'mid': ((world_base[0] + world_end[0]) / 2, (world_base[1] + world_end[1]) / 2)
            }
        
        # Calculate tail positions
        tail_positions = []
        last_pos = (self.x, self.y)
        for segment in self.tail_segments:
            cos_a = math.cos(math.radians(segment['angle']))
            sin_a = math.sin(math.radians(segment['angle']))
            
            end_x = last_pos[0] + cos_a * segment['length']
            end_y = last_pos[1] + sin_a * segment['length']
            
            tail_positions.append({
                'start': last_pos,
                'end': (end_x, end_y)
            })
            last_pos = (end_x, end_y)
        
        # Calculate head position
        head_x = self.x + math.cos(math.radians(self.body_angle)) * 35
        head_y = self.y + math.sin(math.radians(self.body_angle)) * 35
        
        return {
            'body': {
                'x': self.x,
                'y': self.y,
                'width': self.width,
                'height': self.height,
                'angle': self.body_angle
            },
            'head': {
                'x': head_x,
                'y': head_y,
                'angle': self.head_angle
            },
            'limbs': limb_positions,
            'tail': tail_positions,
            'state': self.state,
            'blink': self.blink_timer < 0.1,  # Blink every few seconds
            'ear_twitch': self.ear_twitch_timer < 0.05
        }