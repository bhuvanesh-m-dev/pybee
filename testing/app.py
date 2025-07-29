# app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import json
import os
from ui.editor_tab import EditorTab
from ui.ollama_tab import OllamaTab
from utils.theme_manager import ThemeManager
from utils.file_handler import FileHandler
from ..utils import run_code   # This causes ImportError when running as a script
import config

class PyBee:
    """
    The main class for the PyBee application.
    This class orchestrates the UI, state, and core functionalities.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.file_handler = FileHandler(self)
        self.theme_manager = ThemeManager(self, self.file_handler.config)

        self.setup_ui()
        self.theme_manager.apply()

    def setup_ui(self):
        """
        Initializes the main user interface components.
        """
        self.root.title("PyBee")
        self.root.geometry(config.DEFAULT_GEOMETRY)
        self.root.configure(bg=self.theme_manager.get_current_theme_colors()["bg"])

        # --- Top Bar for global controls ---
        top_bar = tk.Frame(self.root, bg=self.theme_manager.get_current_theme_colors()["bg"])
        top_bar.pack(fill=tk.X, padx=5, pady=5)

        theme_button = tk.Button(
            top_bar, 
            text="Toggle Theme", 
            command=self.theme_manager.toggle
        )
        theme_button.pack(side=tk.RIGHT)
        self.theme_manager.register_widget(theme_button, "button")


        # --- Tab Control ---
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Initialize Tabs ---
        self.editor_tab = EditorTab(self, self.tabs)
        self.ollama_tab = OllamaTab(self, self.tabs)

