# 🐱 Desktop Cat - Video Quest Game

A standalone desktop application for managing video quests and leveling up! Transform your video watching into an exciting RPG-style adventure.

## ✨ Features

- **🎯 Priority Quests**: Mark important videos that need immediate attention
- **📚 Backlog Quests**: Keep track of videos you want to watch later
- **✅ Completed Quests**: Celebrate your achievements and track progress
- **🚀 XP & Leveling**: Gain experience points and level up as you complete videos
- **🔥 Streaks**: Build watching streaks for bonus XP
- **🏆 Achievements**: Unlock special achievements for milestones
- **💾 Save System**: Your progress is automatically saved locally
- **🎨 Beautiful UI**: Modern, intuitive interface with smooth animations

## 🚀 Quick Start

### Option 1: Run Directly (Python Required)
```bash
# Make sure you have Python 3.6+ installed
python3 desktop_cat.py
```

### Option 2: Use the Launcher
```bash
python3 run.py
```

### Option 3: Install and Run
```bash
# Install the package
pip install -e .

# Run from anywhere
desktop-cat
```

## 📦 Building Standalone Executables

Create standalone executables that your friends can run without installing Python:

### Prerequisites
- Python 3.6+
- PyInstaller (will be installed automatically)

### Build Process
```bash
# Run the automated build script
python3 build.py
```

This will:
1. Check dependencies
2. Build the executable
3. Create a distribution package
4. Generate a zip file ready to share

### What Gets Created
- `dist/DesktopCat/` - Folder containing the executable and all dependencies
- `DesktopCat-[OS]-[ARCH].zip` - Ready-to-share package

## 🎮 How to Play

1. **Add Videos**: Type video titles in any of the three zones and click "Add"
2. **Organize**: Move videos between Priority (urgent), Backlog (later), and Completed
3. **Watch Videos**: Select a video and click "Watch" to mark it complete
4. **Earn XP**: Gain experience points for adding and completing videos
5. **Level Up**: Reach XP thresholds to increase your level
6. **Build Streaks**: Watch videos daily to maintain streaks for bonus XP
7. **Unlock Achievements**: Complete milestones to earn special rewards

## 🏆 Achievement System

- **First Steps**: Complete your first video (+50 XP)
- **Getting Warmed Up**: 3-day watching streak (+100 XP)
- **Video Veteran**: Watch 10 videos total (+200 XP)
- **Weekly Warrior**: 7-day watching streak (+300 XP)
- **Priority Master**: Clear all priority quests (+150 XP)

## 💾 Save System

Your game progress is automatically saved to `desktop_cat_save.json` in the same directory. This includes:
- Current level and XP
- Video lists for all categories
- Achievement progress
- Watching streaks
- Total statistics

## 🛠️ Development

### Project Structure
```
desktop_cat/
├── desktop_cat.py      # Main application
├── run.py              # Simple launcher
├── build.py            # Build automation script
├── desktop_cat.spec    # PyInstaller configuration
├── setup.py            # Package setup
├── requirements.txt    # Dependencies (none external)
└── README.md           # This file
```

### Dependencies
- **Python 3.6+**: For f-strings and modern features
- **tkinter**: Built-in GUI framework (included with Python)
- **No external packages required!**

### Building from Source
```bash
# Clone the repository
git clone <your-repo-url>
cd desktop-cat

# Install in development mode
pip install -e .

# Run the application
desktop-cat
```

## 📱 Distribution

### For Friends (No Python Required)
1. Run `python3 build.py` on your machine
2. Share the generated `DesktopCat-[OS]-[ARCH].zip` file
3. Friends extract and run the executable directly

### Cross-Platform Support
- **Windows**: `.exe` file with all dependencies
- **macOS**: App bundle with launcher script
- **Linux**: Binary with shell launcher script

## 🔧 Troubleshooting

### Common Issues

**"tkinter not found"**
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On CentOS/RHEL: `sudo yum install tkinter`
- On macOS: Usually included with Python

**"Permission denied" on Linux/Mac**
- Make launcher executable: `chmod +x run.sh`

**App won't start**
- Check Python version: `python3 --version` (needs 3.6+)
- Verify all files are in the same directory

### Getting Help
1. Check the console output for error messages
2. Ensure Python 3.6+ is installed
3. Verify all required files are present

## 🎨 Customization

### Colors and Themes
Edit the color values in `desktop_cat.py`:
```python
# Zone colors
zone_configs = [
    ('priority', '🔥 Priority Quests', '#e74c3c'),    # Red
    ('backlog', '📚 Backlog Quests', '#f39c12'),     # Orange
    ('completed', '✅ Completed Quests', '#27ae60'),  # Green
]
```

### Adding New Achievements
Extend the achievements list in the `__init__` method:
```python
self.achievements.append({
    'id': 'custom_achievement',
    'name': 'Custom Achievement',
    'desc': 'Description here',
    'xp': 100
})
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve the documentation

---

**Happy Questing! 🐱✨**

*Transform your video watching into an epic adventure with Desktop Cat!*
