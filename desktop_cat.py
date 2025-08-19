#!/usr/bin/env python3
"""
Desktop Cat - Video Quest Game
A standalone desktop application for managing video quests and leveling up!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time

class DesktopCat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Cat - Video Quest Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Game data
        self.game_data = {
            'level': 1,
            'xp': 0,
            'total_watched': 0,
            'streak': 0,
            'achievement_score': 0,
            'videos': {
                'priority': [],
                'backlog': [],
                'completed': []
            },
            'last_watch_date': None
        }
        
        # Achievements
        self.achievements = [
            {'id': 'first_watch', 'name': 'First Steps', 'desc': 'Complete your first video!', 'xp': 50},
            {'id': 'streak_3', 'name': 'Getting Warmed Up', 'desc': '3 day watching streak!', 'xp': 100},
            {'id': 'watch_10', 'name': 'Video Veteran', 'desc': 'Watch 10 videos total!', 'xp': 200},
            {'id': 'streak_7', 'name': 'Weekly Warrior', 'desc': '7 day watching streak!', 'xp': 300},
            {'id': 'priority_clear', 'name': 'Priority Master', 'desc': 'Clear all priority quests!', 'xp': 150},
        ]
        
        self.unlocked_achievements = []
        self.load_game_data()
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Main header
        header_frame = tk.Frame(self.root, bg='#34495e', height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Level display
        self.level_label = tk.Label(
            header_frame, 
            text=f"Level {self.game_data['level']}", 
            font=('Arial', 24, 'bold'),
            fg='#f39c12',
            bg='#34495e'
        )
        self.level_label.pack(pady=10)
        
        # XP bar
        xp_frame = tk.Frame(header_frame, bg='#34495e')
        xp_frame.pack(pady=5)
        
        tk.Label(xp_frame, text="XP:", fg='white', bg='#34495e').pack(side='left')
        self.xp_progress = ttk.Progressbar(
            xp_frame, 
            length=300, 
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.xp_progress.pack(side='left', padx=5)
        
        self.xp_label = tk.Label(xp_frame, text="0/100", fg='white', bg='#34495e')
        self.xp_label.pack(side='left', padx=5)
        
        # Stats bar
        stats_frame = tk.Frame(header_frame, bg='#34495e')
        stats_frame.pack(pady=5)
        
        self.stats_labels = {}
        for stat in ['Total Watched', 'Streak', 'Achievement Score']:
            label = tk.Label(
                stats_frame, 
                text=f"{stat}: 0", 
                fg='white', 
                bg='#34495e',
                font=('Arial', 10)
            )
            label.pack(side='left', padx=10)
            self.stats_labels[stat] = label
        
        # Quest zones
        zones_frame = tk.Frame(self.root, bg='#2c3e50')
        zones_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create three zones
        self.zones = {}
        zone_configs = [
            ('priority', '🔥 Priority Quests', '#e74c3c'),
            ('backlog', '📚 Backlog Quests', '#f39c12'),
            ('completed', '✅ Completed Quests', '#27ae60')
        ]
        
        for i, (zone_id, title, color) in enumerate(zone_configs):
            zone_frame = tk.Frame(zones_frame, bg='#34495e', relief='raised', bd=2)
            zone_frame.grid(row=0, column=i, sticky='nsew', padx=5)
            zones_frame.grid_columnconfigure(i, weight=1)
            
            # Zone header
            tk.Label(
                zone_frame, 
                text=title, 
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=color,
                pady=5
            ).pack(fill='x')
            
            # Input frame
            input_frame = tk.Frame(zone_frame, bg='#34495e')
            input_frame.pack(fill='x', padx=10, pady=5)
            
            entry = tk.Entry(input_frame, font=('Arial', 10))
            entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
            
            add_btn = tk.Button(
                input_frame,
                text="Add",
                command=lambda z=zone_id, e=entry: self.add_video(z, e),
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold')
            )
            add_btn.pack(side='right')
            
            # Video list
            listbox = tk.Listbox(
                zone_frame,
                bg='#2c3e50',
                fg='white',
                font=('Arial', 10),
                selectmode='single',
                height=15
            )
            listbox.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Buttons frame
            btn_frame = tk.Frame(zone_frame, bg='#34495e')
            btn_frame.pack(fill='x', padx=10, pady=5)
            
            if zone_id != 'completed':
                watch_btn = tk.Button(
                    btn_frame,
                    text="Watch",
                    command=lambda z=zone_id, lb=listbox: self.watch_video(z, lb),
                    bg='#27ae60',
                    fg='white',
                    font=('Arial', 10, 'bold')
                )
                watch_btn.pack(side='left', padx=5)
            
            delete_btn = tk.Button(
                btn_frame,
                text="Delete",
                command=lambda z=zone_id, lb=listbox: self.delete_video(z, lb),
                bg='#e74c3c',
                fg='white',
                font=('Arial', 10, 'bold')
            )
            delete_btn.pack(side='right', padx=5)
            
            self.zones[zone_id] = {
                'frame': zone_frame,
                'listbox': listbox,
                'entry': entry,
                'color': color
            }
        
        # Achievement display
        achievement_frame = tk.Frame(self.root, bg='#34495e')
        achievement_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            achievement_frame,
            text="🏆 Achievements",
            font=('Arial', 12, 'bold'),
            fg='#f39c12',
            bg='#34495e'
        ).pack()
        
        self.achievement_text = tk.Text(
            achievement_frame,
            height=4,
            bg='#2c3e50',
            fg='white',
            font=('Arial', 9),
            wrap='word'
        )
        self.achievement_text.pack(fill='x', padx=10, pady=5)
        
        # Save button
        save_btn = tk.Button(
            self.root,
            text="💾 Save Game",
            command=self.save_game_data,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            pady=5
        )
        save_btn.pack(pady=10)
        
        # Configure styles
        style = ttk.Style()
        style.configure('Custom.Horizontal.TProgressbar', 
                       troughcolor='#2c3e50', 
                       background='#27ae60')
        
    def add_video(self, category, entry):
        title = entry.get().strip()
        if not title:
            return
            
        video = {
            'id': int(time.time() * 1000),
            'title': title,
            'date_added': datetime.now().isoformat(),
            'category': category
        }
        
        self.game_data['videos'][category].append(video)
        entry.delete(0, tk.END)
        
        # Add XP for adding videos
        self.gain_xp(10)
        self.update_display()
        
    def watch_video(self, category, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a video to watch!")
            return
            
        index = selection[0]
        video = self.game_data['videos'][category][index]
        
        # Remove from current category
        self.game_data['videos'][category].pop(index)
        
        # Add to completed
        video['category'] = 'completed'
        video['completed_date'] = datetime.now().isoformat()
        self.game_data['videos']['completed'].append(video)
        
        # Calculate XP based on category
        xp_gain = 50
        if category == 'priority':
            xp_gain = 100
        elif category == 'backlog':
            xp_gain = 75
            
        # Update streak
        today = datetime.now().date()
        if self.game_data['last_watch_date']:
            last_date = datetime.fromisoformat(self.game_data['last_watch_date']).date()
            if last_date == today - timedelta(days=1) or last_date == today:
                if last_date != today:
                    self.game_data['streak'] += 1
                    xp_gain += self.game_data['streak'] * 10
            else:
                self.game_data['streak'] = 1
        else:
            self.game_data['streak'] = 1
            
        self.game_data['last_watch_date'] = today.isoformat()
        self.game_data['total_watched'] += 1
        
        self.gain_xp(xp_gain)
        self.check_achievements()
        self.update_display()
        
        messagebox.showinfo("Success", f"Video completed! +{xp_gain} XP")
        
    def delete_video(self, category, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a video to delete!")
            return
            
        index = selection[0]
        video = self.game_data['videos'][category][index]
        
        if messagebox.askyesno("Confirm", f"Delete '{video['title']}'?"):
            self.game_data['videos'][category].pop(index)
            self.update_display()
            
    def gain_xp(self, amount):
        self.game_data['xp'] += amount
        
        # Level up check
        xp_needed = self.game_data['level'] * 100
        if self.game_data['xp'] >= xp_needed:
            self.game_data['level'] += 1
            self.game_data['xp'] -= xp_needed
            messagebox.showinfo("LEVEL UP!", f"You're now Level {self.game_data['level']}! 🚀")
            
    def check_achievements(self):
        for achievement in self.achievements:
            if achievement['id'] not in self.unlocked_achievements:
                unlocked = False
                
                if achievement['id'] == 'first_watch':
                    unlocked = self.game_data['total_watched'] >= 1
                elif achievement['id'] == 'streak_3':
                    unlocked = self.game_data['streak'] >= 3
                elif achievement['id'] == 'watch_10':
                    unlocked = self.game_data['total_watched'] >= 10
                elif achievement['id'] == 'streak_7':
                    unlocked = self.game_data['streak'] >= 7
                elif achievement['id'] == 'priority_clear':
                    unlocked = (len(self.game_data['videos']['priority']) == 0 and 
                              self.game_data['total_watched'] > 0)
                
                if unlocked:
                    self.unlocked_achievements.append(achievement['id'])
                    self.game_data['achievement_score'] += achievement['xp']
                    self.gain_xp(achievement['xp'])
                    messagebox.showinfo("Achievement Unlocked!", 
                                      f"{achievement['name']}: {achievement['desc']} 🏆")
                    
    def update_display(self):
        # Update level and XP
        self.level_label.config(text=f"Level {self.game_data['level']}")
        
        xp_needed = self.game_data['level'] * 100
        self.xp_progress['maximum'] = xp_needed
        self.xp_progress['value'] = self.game_data['xp']
        self.xp_label.config(text=f"{self.game_data['xp']}/{xp_needed}")
        
        # Update stats
        self.stats_labels['Total Watched'].config(text=f"Total Watched: {self.game_data['total_watched']}")
        self.stats_labels['Streak'].config(text=f"Streak: {self.game_data['streak']}")
        self.stats_labels['Achievement Score'].config(text=f"Achievement Score: {self.game_data['achievement_score']}")
        
        # Update video lists
        for category, zone in self.zones.items():
            listbox = zone['listbox']
            listbox.delete(0, tk.END)
            
            for video in self.game_data['videos'][category]:
                listbox.insert(tk.END, video['title'])
                
        # Update achievements
        achievement_text = "Unlocked: "
        if self.unlocked_achievements:
            unlocked_names = [a['name'] for a in self.achievements if a['id'] in self.unlocked_achievements]
            achievement_text += ", ".join(unlocked_names)
        else:
            achievement_text += "None yet"
            
        achievement_text += f"\n\nAvailable: "
        available_names = [a['name'] for a in self.achievements if a['id'] not in self.unlocked_achievements]
        achievement_text += ", ".join(available_names) if available_names else "All unlocked!"
        
        self.achievement_text.delete(1.0, tk.END)
        self.achievement_text.insert(1.0, achievement_text)
        
    def save_game_data(self):
        try:
            with open('desktop_cat_save.json', 'w') as f:
                json.dump(self.game_data, f, indent=2)
            messagebox.showinfo("Success", "Game saved successfully! 💾")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game: {e}")
            
    def load_game_data(self):
        try:
            if os.path.exists('desktop_cat_save.json'):
                with open('desktop_cat_save.json', 'r') as f:
                    self.game_data = json.load(f)
        except Exception as e:
            print(f"Failed to load save data: {e}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopCat()
    app.run()