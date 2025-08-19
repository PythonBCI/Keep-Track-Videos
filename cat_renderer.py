#!/usr/bin/env python3
"""
Cat Renderer Module
Draws the animated cat with smooth graphics and anatomically correct proportions
"""

import tkinter as tk
import math
from typing import Tuple, Dict, List

class CatRenderer:
    """Renders the animated cat with smooth graphics"""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.cat_objects = {}  # Store canvas object IDs for smooth updates
        
        # Cat colors and styling
        self.colors = {
            'body': '#8B4513',      # Saddle brown
            'body_highlight': '#A0522D',  # Sienna
            'limbs': '#654321',     # Dark brown
            'head': '#8B4513',      # Saddle brown
            'ears': '#654321',      # Dark brown
            'tail': '#654321',      # Dark brown
            'eyes': '#FFD700',      # Gold
            'pupils': '#000000',    # Black
            'nose': '#FF69B4',      # Hot pink
            'whiskers': '#FFFFFF',  # White
            'paws': '#8B4513'      # Saddle brown
        }
        
        # Animation smoothing
        self.smoothing_factor = 0.8
        
    def draw_cat(self, cat_data: Dict):
        """Draw the complete cat with all its parts"""
        # Clear previous cat objects
        self._clear_cat()
        
        # Draw body
        self._draw_body(cat_data['body'])
        
        # Draw limbs
        self._draw_limbs(cat_data['limbs'])
        
        # Draw tail
        self._draw_tail(cat_data['tail'])
        
        # Draw head
        self._draw_head(cat_data['head'], cat_data['blink'], cat_data['ear_twitch'])
        
        # Draw whiskers
        self._draw_whiskers(cat_data['head'])
        
    def _clear_cat(self):
        """Remove all cat-related canvas objects"""
        for obj_id in self.cat_objects.values():
            if obj_id:
                self.canvas.delete(obj_id)
        self.cat_objects.clear()
        
    def _draw_body(self, body_data: Dict):
        """Draw the main cat body with smooth curves"""
        x, y = body_data['x'], body_data['y']
        width, height = body_data['width'], body_data['height']
        angle = body_data['angle']
        
        # Create smooth oval body
        body_id = self.canvas.create_oval(
            x - width//2, y - height//2,
            x + width//2, y + height//2,
            fill=self.colors['body'],
            outline=self.colors['body_highlight'],
            width=2,
            tags='cat_body'
        )
        
        # Add body highlight
        highlight_id = self.canvas.create_oval(
            x - width//3, y - height//3,
            x + width//3, y + height//3,
            fill=self.colors['body_highlight'],
            outline='',
            tags='cat_body_highlight'
        )
        
        # Rotate body
        self.canvas.rotate(body_id, angle, x, y)
        self.canvas.rotate(highlight_id, angle, x, y)
        
        self.cat_objects['body'] = body_id
        self.cat_objects['body_highlight'] = highlight_id
        
    def _draw_limbs(self, limbs_data: Dict):
        """Draw all four limbs with smooth articulation"""
        for limb_name, limb_data in limbs_data.items():
            base_x, base_y = limb_data['base']
            end_x, end_y = limb_data['end']
            
            # Draw limb as a smooth curve
            limb_id = self.canvas.create_line(
                base_x, base_y, end_x, end_y,
                fill=self.colors['limbs'],
                width=8,
                capstyle=tk.ROUND,
                smooth=True,
                tags=f'cat_limb_{limb_name}'
            )
            
            # Draw paw at the end
            paw_id = self.canvas.create_oval(
                end_x - 6, end_y - 6,
                end_x + 6, end_y + 6,
                fill=self.colors['paws'],
                outline=self.colors['limbs'],
                width=2,
                tags=f'cat_paw_{limb_name}'
            )
            
            self.cat_objects[f'limb_{limb_name}'] = limb_id
            self.cat_objects[f'paw_{limb_name}'] = paw_id
            
    def _draw_tail(self, tail_data: List[Dict]):
        """Draw the tail with smooth wave-like curves"""
        if not tail_data:
            return
            
        # Create smooth tail curve
        points = []
        for segment in tail_data:
            points.extend([segment['start'][0], segment['start'][1]])
        # Add final end point
        if tail_data:
            points.extend([tail_data[-1]['end'][0], tail_data[-1]['end'][1]])
            
        if len(points) >= 4:
            tail_id = self.canvas.create_line(
                *points,
                fill=self.colors['tail'],
                width=6,
                smooth=True,
                capstyle=tk.ROUND,
                tags='cat_tail'
            )
            self.cat_objects['tail'] = tail_id
            
            # Add tail tip
            if tail_data:
                tip_x, tip_y = tail_data[-1]['end']
                tip_id = self.canvas.create_oval(
                    tip_x - 4, tip_y - 4,
                    tip_x + 4, tip_y + 4,
                    fill=self.colors['tail'],
                    outline=self.colors['body_highlight'],
                    width=1,
                    tags='cat_tail_tip'
                )
                self.cat_objects['tail_tip'] = tip_id
                
    def _draw_head(self, head_data: Dict, blink: bool, ear_twitch: bool):
        """Draw the cat head with ears, eyes, and nose"""
        x, y = head_data['x'], head_data['y']
        angle = head_data['angle']
        
        # Head base
        head_id = self.canvas.create_oval(
            x - 20, y - 20,
            x + 20, y + 20,
            fill=self.colors['head'],
            outline=self.colors['body_highlight'],
            width=2,
            tags='cat_head'
        )
        
        # Ears
        ear_offset = 2 if ear_twitch else 0
        left_ear_id = self.canvas.create_polygon(
            x - 15, y - 25 + ear_offset,
            x - 25, y - 35 + ear_offset,
            x - 15, y - 15 + ear_offset,
            fill=self.colors['ears'],
            outline=self.colors['body_highlight'],
            width=1,
            tags='cat_left_ear'
        )
        
        right_ear_id = self.canvas.create_polygon(
            x + 15, y - 25 + ear_offset,
            x + 25, y - 35 + ear_offset,
            x + 15, y - 15 + ear_offset,
            fill=self.colors['ears'],
            outline=self.colors['body_highlight'],
            width=1,
            tags='cat_right_ear'
        )
        
        # Eyes
        if not blink:
            # Open eyes
            left_eye_id = self.canvas.create_oval(
                x - 12, y - 8,
                x - 6, y - 2,
                fill=self.colors['eyes'],
                outline=self.colors['body_highlight'],
                width=1,
                tags='cat_left_eye'
            )
            
            right_eye_id = self.canvas.create_oval(
                x + 6, y - 8,
                x + 12, y - 2,
                fill=self.colors['eyes'],
                outline=self.colors['body_highlight'],
                width=1,
                tags='cat_right_eye'
            )
            
            # Pupils
            left_pupil_id = self.canvas.create_oval(
                x - 10, y - 6,
                x - 8, y - 4,
                fill=self.colors['pupils'],
                outline='',
                tags='cat_left_pupil'
            )
            
            right_pupil_id = self.canvas.create_oval(
                x + 8, y - 6,
                x + 10, y - 4,
                fill=self.colors['pupils'],
                outline='',
                tags='cat_right_pupil'
            )
            
            self.cat_objects['left_pupil'] = left_pupil_id
            self.cat_objects['right_pupil'] = right_pupil_id
        else:
            # Closed eyes (simple lines)
            left_eye_id = self.canvas.create_line(
                x - 12, y - 5,
                x - 6, y - 5,
                fill=self.colors['body_highlight'],
                width=2,
                tags='cat_left_eye'
            )
            
            right_eye_id = self.canvas.create_line(
                x + 6, y - 5,
                x + 12, y - 5,
                fill=self.colors['body_highlight'],
                width=2,
                tags='cat_right_eye'
            )
            
        # Nose
        nose_id = self.canvas.create_oval(
            x - 2, y + 2,
            x + 2, y + 6,
            fill=self.colors['nose'],
            outline=self.colors['body_highlight'],
            width=1,
            tags='cat_nose'
        )
        
        # Store object IDs
        self.cat_objects['head'] = head_id
        self.cat_objects['left_ear'] = left_ear_id
        self.cat_objects['right_ear'] = right_ear_id
        self.cat_objects['left_eye'] = left_eye_id
        self.cat_objects['right_eye'] = right_eye_id
        self.cat_objects['nose'] = nose_id
        
        # Rotate head
        self.canvas.rotate(head_id, angle, x, y)
        self.canvas.rotate(left_ear_id, angle, x, y)
        self.canvas.rotate(right_ear_id, angle, x, y)
        self.canvas.rotate(left_eye_id, angle, x, y)
        self.canvas.rotate(right_eye_id, angle, x, y)
        self.canvas.rotate(nose_id, angle, x, y)
        
        if not blink:
            self.canvas.rotate(self.cat_objects['left_pupil'], angle, x, y)
            self.canvas.rotate(self.cat_objects['right_pupil'], angle, x, y)
            
    def _draw_whiskers(self, head_data: Dict):
        """Draw cat whiskers"""
        x, y = head_data['x'], head_data['y']
        
        # Left whiskers
        left_whisker1_id = self.canvas.create_line(
            x - 20, y + 5,
            x - 35, y + 3,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_left_whisker1'
        )
        
        left_whisker2_id = self.canvas.create_line(
            x - 20, y + 8,
            x - 35, y + 8,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_left_whisker2'
        )
        
        left_whisker3_id = self.canvas.create_line(
            x - 20, y + 11,
            x - 35, y + 13,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_left_whisker3'
        )
        
        # Right whiskers
        right_whisker1_id = self.canvas.create_line(
            x + 20, y + 5,
            x + 35, y + 3,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_right_whisker1'
        )
        
        right_whisker2_id = self.canvas.create_line(
            x + 20, y + 8,
            x + 35, y + 8,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_right_whisker2'
        )
        
        right_whisker3_id = self.canvas.create_line(
            x + 20, y + 11,
            x + 35, y + 13,
            fill=self.colors['whiskers'],
            width=2,
            tags='cat_right_whisker3'
        )
        
        # Store whisker IDs
        self.cat_objects['left_whisker1'] = left_whisker1_id
        self.cat_objects['left_whisker2'] = left_whisker2_id
        self.cat_objects['left_whisker3'] = left_whisker3_id
        self.cat_objects['right_whisker1'] = right_whisker1_id
        self.cat_objects['right_whisker2'] = right_whisker2_id
        self.cat_objects['right_whisker3'] = right_whisker3_id
        
    def update_cat(self, cat_data: Dict):
        """Update existing cat objects for smooth animation"""
        # For smooth updates, we'll redraw the entire cat
        # This ensures perfect limb articulation and smooth movement
        self.draw_cat(cat_data)
        
    def add_canvas_rotation_support(self):
        """Add rotation support to the canvas if not already present"""
        if not hasattr(self.canvas, 'rotate'):
            def rotate(self, item_id, angle, x, y):
                """Rotate a canvas item around a point"""
                # Get current coordinates
                coords = self.coords(item_id)
                if len(coords) >= 2:
                    # Apply rotation transformation
                    rad = math.radians(angle)
                    cos_a = math.cos(rad)
                    sin_a = math.sin(rad)
                    
                    new_coords = []
                    for i in range(0, len(coords), 2):
                        dx = coords[i] - x
                        dy = coords[i + 1] - y
                        new_x = x + dx * cos_a - dy * sin_a
                        new_y = y + dx * sin_a + dy * cos_a
                        new_coords.extend([new_x, new_y])
                    
                    self.coords(item_id, *new_coords)
            
            # Add rotation method to canvas
            tk.Canvas.rotate = rotate