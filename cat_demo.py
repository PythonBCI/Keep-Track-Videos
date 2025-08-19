#!/usr/bin/env python3
"""
Cat Animation Demo
Showcases the fluid, anatomically correct cat animation system
"""

import tkinter as tk
import time
import threading
from cat_animation import CatBody
from cat_renderer import CatRenderer

class CatDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐱 Cat Animation Demo - Fluid & Anatomically Correct")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Create main canvas
        self.canvas = tk.Canvas(
            self.root,
            bg='#34495e',
            width=800,
            height=500,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Create cat
        self.cat = CatBody(400, 250)
        self.cat_renderer = CatRenderer(self.canvas)
        self.cat_renderer.add_canvas_rotation_support()
        
        # Add decorations
        self._add_decorations()
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        
        # Control panel
        self._create_control_panel()
        
        # Animation loop
        self.animation_running = True
        self.animation_thread = threading.Thread(target=self.animation_loop, daemon=True)
        self.animation_thread.start()
        
        # Instructions
        self._show_instructions()
        
    def _add_decorations(self):
        """Add decorative elements to the canvas"""
        # Ground
        self.canvas.create_rectangle(0, 450, 800, 500, fill='#27ae60', outline='')
        
        # Grass
        for i in range(0, 800, 15):
            self.canvas.create_line(
                i, 450, i + 8, 500,
                fill='#2ecc71', width=2
            )
            
        # Floating particles
        for i in range(15):
            x = self._random_x()
            y = self._random_y()
            self.canvas.create_oval(
                x, y, x + 4, y + 4,
                fill='#f39c12', tags='particle'
            )
            
        # Some trees in background
        for i in range(3):
            x = 100 + i * 250
            self._draw_tree(x, 400)
            
    def _draw_tree(self, x, y):
        """Draw a simple tree"""
        # Trunk
        self.canvas.create_rectangle(x-5, y-60, x+5, y, fill='#8B4513', outline='')
        # Leaves
        self.canvas.create_oval(x-25, y-80, x+25, y-20, fill='#228B22', outline='')
        
    def _random_x(self):
        """Generate random x coordinate"""
        import random
        return random.randint(50, 750)
        
    def _random_y(self):
        """Generate random y coordinate"""
        import random
        return random.randint(50, 400)
        
    def _create_control_panel(self):
        """Create control panel for cat behavior"""
        control_frame = tk.Frame(self.root, bg='#34495e')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Speed control
        tk.Label(control_frame, text="Cat Speed:", bg='#34495e', fg='white').pack(side='left', padx=5)
        self.speed_scale = tk.Scale(
            control_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient='horizontal',
            bg='#34495e',
            fg='white',
            highlightthickness=0,
            command=self._on_speed_change
        )
        self.speed_scale.set(0.8)
        self.speed_scale.pack(side='left', padx=5)
        
        # Random movement button
        tk.Button(
            control_frame,
            text="🎯 Random Target",
            command=self._random_target,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold')
        ).pack(side='left', padx=10)
        
        # Reset position button
        tk.Button(
            control_frame,
            text="🏠 Reset Position",
            command=self._reset_position,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold')
        ).pack(side='left', padx=10)
        
        # Info label
        self.info_label = tk.Label(
            control_frame,
            text="Click anywhere to move the cat!",
            bg='#34495e',
            fg='#f39c12',
            font=('Arial', 10, 'bold')
        )
        self.info_label.pack(side='right', padx=10)
        
    def _show_instructions(self):
        """Show demo instructions"""
        instructions = """
🐱 Cat Animation Demo

Features:
• Anatomically correct limb articulation
• Smooth, fluid movement
• Realistic walking animation
• Interactive click-to-move
• Natural tail and head movement
• Blinking and ear twitching

Controls:
• Click anywhere to move the cat
• Adjust speed with the slider
• Use buttons for random movement
• Watch the smooth limb coordination!
        """
        
        # Create info window
        info_window = tk.Toplevel(self.root)
        info_window.title("Demo Instructions")
        info_window.geometry("400x300")
        info_window.configure(bg='#2c3e50')
        
        text_widget = tk.Text(
            info_window,
            bg='#34495e',
            fg='white',
            font=('Arial', 10),
            wrap='word',
            padx=10,
            pady=10
        )
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', instructions)
        text_widget.config(state='disabled')
        
    def on_canvas_click(self, event):
        """Handle canvas clicks"""
        self.cat.set_target(event.x, event.y)
        self.info_label.config(text=f"Moving to ({event.x}, {event.y})")
        
    def on_mouse_move(self, event):
        """Handle mouse movement for cat following"""
        # Cat slightly follows mouse when close
        distance = ((event.x - self.cat.x) ** 2 + (event.y - self.cat.y) ** 2) ** 0.5
        if distance < 100:
            # Subtle attraction to mouse
            self.cat.target_x += (event.x - self.cat.x) * 0.001
            self.cat.target_y += (event.y - self.cat.y) * 0.001
            
    def _on_speed_change(self, value):
        """Handle speed slider change"""
        self.cat.speed = float(value)
        
    def _random_target(self):
        """Set random target for cat"""
        import random
        x = random.randint(100, 700)
        y = random.randint(100, 400)
        self.cat.set_target(x, y)
        self.info_label.config(text=f"Random target: ({x}, {y})")
        
    def _reset_position(self):
        """Reset cat to center"""
        self.cat.set_target(400, 250)
        self.info_label.config(text="Reset to center")
        
    def animation_loop(self):
        """Main animation loop"""
        last_time = time.time()
        
        while self.animation_running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Update cat
            self.cat.update(dt)
            
            # Get cat data and update display
            cat_data = self.cat.get_drawing_data()
            self.root.after(0, self._update_display, cat_data)
            
            # 60 FPS
            time.sleep(1/60)
            
    def _update_display(self, cat_data):
        """Update cat display"""
        try:
            self.cat_renderer.update_cat(cat_data)
        except Exception as e:
            print(f"Display update error: {e}")
            
    def run(self):
        """Run the demo"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        self.animation_running = False
        if hasattr(self, 'animation_thread') and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1)
        self.root.destroy()

if __name__ == "__main__":
    demo = CatDemo()
    demo.run()