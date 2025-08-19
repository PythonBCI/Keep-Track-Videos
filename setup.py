#!/usr/bin/env python3
"""
Setup script for Desktop Cat - Video Quest Game
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="desktop-cat",
    version="1.0.0",
    description="A standalone desktop video quest game for managing and tracking video content",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/desktop-cat",
    packages=find_packages(),
    py_modules=["desktop_cat"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Video",
        "Topic :: Productivity",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        "console_scripts": [
            "desktop-cat=desktop_cat:main",
        ],
        "gui_scripts": [
            "desktop-cat-gui=desktop_cat:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="desktop, game, video, quest, productivity, tkinter",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/desktop-cat/issues",
        "Source": "https://github.com/yourusername/desktop-cat",
        "Documentation": "https://github.com/yourusername/desktop-cat#readme",
    },
)