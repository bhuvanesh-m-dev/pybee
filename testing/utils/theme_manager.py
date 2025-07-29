# utils/theme_manager.py
import tkinter as tk
from tkinter import ttk
import config

class ThemeManager:
    """
    Manages loading, applying, and switching UI themes.
    """
    def __init__(self, app, app_config):
        self.app = app
        self.config = app_config
        self.current_theme_name = self.config.get("theme", "dark")
        self.widgets = []

    def register_widget(self, widget, widget_type):
        """Register a widget to be themed."""
        self.widgets.append((widget, widget_type))

    def get_current_theme_colors(self):
        return config.THEMES.get(self.current_theme_name, config.THEMES["dark"])

    def toggle(self):
        """Switches between dark and light themes."""
        self.current_theme_name = "light" if self.current_theme_name == "dark" else "dark"
        self.config["theme"] = self.current_theme_name
        self.app.file_handler.save_config()
        self.apply()

    def apply(self):
        """Applies the current theme to all registered widgets."""
        theme = self.get_current_theme_colors()
        
        # --- Root and Main Frames ---
        self.app.root.configure(bg=theme["bg"])
        for child in self.app.root.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=theme["bg"])
        
        # --- TTK Widget Styling (Tabs, Combobox) ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=theme["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=theme["button_bg"], foreground=theme["button_fg"], padding=[10, 5], borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", theme["accent_color"])], foreground=[("selected", "white")])
        style.configure("TCombobox", selectbackground=theme["accent_color"], fieldbackground=theme["editor_bg"], background=theme["button_bg"], foreground=theme["fg"])

        # --- Apply to registered Tk widgets ---
        for widget, widget_type in self.widgets:
            try:
                if widget_type == "button":
                    widget.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["accent_color"], activeforeground="white", borderwidth=1)
                elif widget_type == "run_button":
                    widget.config(bg=theme["run_button_bg"], fg=theme["button_fg"], activebackground=theme["accent_color"], activeforeground="white", borderwidth=1)
                elif widget_type == "ask_button":
                     widget.config(bg=theme["ask_button_bg"], fg=theme["button_fg"], activebackground=theme["accent_color"], activeforeground="white", borderwidth=1)
                elif widget_type == "copy_button":
                     widget.config(bg=theme["copy_button_bg"], fg=theme["button_fg"], activebackground=theme["accent_color"], activeforeground="white", borderwidth=1)
                elif widget_type == "label":
                    widget.config(bg=theme["bg"], fg=theme["fg"])
                elif widget_type == "editor":
                    widget.config(bg=theme["editor_bg"], fg=theme["editor_fg"], insertbackground=theme["fg"], selectbackground=theme["accent_color"])
                elif widget_type == "output":
                    widget.config(bg=theme["output_bg"], fg=theme["output_fg"], insertbackground=theme["fg"], selectbackground=theme["accent_color"])
                elif widget_type == "listbox":
                    widget.config(bg=theme["editor_bg"], fg=theme["editor_fg"], selectbackground=theme["accent_color"], selectforeground="white")
            except tk.TclError:
                # Widget might have been destroyed
                pass

