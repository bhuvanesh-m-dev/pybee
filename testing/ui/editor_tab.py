# ui/editor_tab.py
import tkinter as tk
from tkinter import PanedWindow
import os
from utils import run_code

class EditorTab:
    """
    Manages the UI and functionality of the 'Editor' tab.
    """
    def __init__(self, app, tabs_control):
        self.app = app
        self.theme_manager = app.theme_manager
        self.file_handler = app.file_handler
        
        self.frame = tk.Frame(tabs_control, bg=self.theme_manager.get_current_theme_colors()["bg"])
        tabs_control.add(self.frame, text="Editor")

        self._setup_widgets()
        # Populate the listbox after all widgets have been created
        self.update_recent_files_display()

    def _setup_widgets(self):
        # --- Editor Controls ---
        controls_frame = tk.Frame(self.frame, bg=self.theme_manager.get_current_theme_colors()["bg"])
        controls_frame.pack(fill=tk.X, padx=5, pady=2)
        
        open_btn = tk.Button(controls_frame, text="Open", command=self.file_handler.open)
        save_btn = tk.Button(controls_frame, text="Save", command=self.file_handler.save)
        self.run_btn = tk.Button(controls_frame, text="▶ Run Code", command=lambda: run_code(self))

        open_btn.pack(side=tk.LEFT, padx=2)
        save_btn.pack(side=tk.LEFT, padx=2)
        self.run_btn.pack(side=tk.LEFT, padx=2)

        self.theme_manager.register_widget(open_btn, "button")
        self.theme_manager.register_widget(save_btn, "button")
        self.theme_manager.register_widget(self.run_btn, "run_button")

        # --- Editor Panes (Resizable) ---
        editor_panes = PanedWindow(self.frame, orient=tk.HORIZONTAL, bg=self.theme_manager.get_current_theme_colors()["bg"], sashwidth=8)
        editor_panes.pack(fill=tk.BOTH, expand=True)

        # --- Pane 1: Recent Files ---
        recent_files_frame = tk.Frame(editor_panes, width=200)
        editor_panes.add(recent_files_frame, stretch="never")
        
        recent_label = tk.Label(recent_files_frame, text="Recent Files")
        recent_label.pack(anchor="w")
        self.recent_files_listbox = tk.Listbox(recent_files_frame, height=15)
        self.recent_files_listbox.pack(fill=tk.BOTH, expand=True)
        self.recent_files_listbox.bind("<Double-1>", self.file_handler.open_selected_recent)

        self.theme_manager.register_widget(recent_label, "label")
        self.theme_manager.register_widget(self.recent_files_listbox, "listbox")

        # --- Pane 2: Code and Output ---
        code_output_frame = PanedWindow(editor_panes, orient=tk.VERTICAL, bg=self.theme_manager.get_current_theme_colors()["bg"], sashwidth=8)
        editor_panes.add(code_output_frame, stretch="always")

        self.editor = tk.Text(code_output_frame, font=("Consolas", 12), undo=True, wrap=tk.WORD)
        code_output_frame.add(self.editor, stretch="always")

        self.output_text = tk.Text(code_output_frame, height=10, font=("Consolas", 10), wrap=tk.WORD)
        code_output_frame.add(self.output_text, stretch="never")
        
        self.theme_manager.register_widget(self.editor, "editor")
        self.theme_manager.register_widget(self.output_text, "output")

    def update_recent_files_display(self):
        """Populates the recent files listbox with the current list from the file_handler."""
        self.recent_files_listbox.delete(0, tk.END)
        for f in self.file_handler.recent_files:
            self.recent_files_listbox.insert(tk.END, os.path.basename(f))

