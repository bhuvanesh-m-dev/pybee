# utils/file_handler.py
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import config

class FileHandler:
    """
    Handles file operations like opening, saving, and managing recent files.
    """
    def __init__(self, app):
        self.app = app
        self.config = self._load_config()
        self.recent_files = self.config.get("recent_files", [])

    def _load_config(self):
        try:
            with open(config.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_config(self):
        self.config["recent_files"] = self.recent_files
        with open(config.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def open(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                defaultextension=".py",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
            )
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.app.editor_tab.editor.delete("1.0", tk.END)
                self.app.editor_tab.editor.insert(tk.END, content)
                self.app.root.title(f"PyBee - {os.path.basename(filepath)}")
                self._add_to_recent_files(filepath)
            except Exception as e:
                messagebox.showerror("Error Opening File", f"Could not open file: {e}")
    
    def save(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(self.app.editor_tab.editor.get("1.0", tk.END))
                self.app.root.title(f"PyBee - {os.path.basename(filepath)}")
                self._add_to_recent_files(filepath)
            except Exception as e:
                messagebox.showerror("Error Saving File", f"Could not save file: {e}")

    def _add_to_recent_files(self, filepath):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.recent_files = self.recent_files[:config.RECENT_FILES_LIMIT]
        
        # Call the editor tab's own method to update its display
        self.app.editor_tab.update_recent_files_display()
        
        self.save_config()

    def open_selected_recent(self, event=None):
        # This method is safe because it's only called after initialization
        selected_indices = self.app.editor_tab.recent_files_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            if selected_index < len(self.recent_files):
                filepath = self.recent_files[selected_index]
                self.open(filepath)

