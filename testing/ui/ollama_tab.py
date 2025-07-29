# ui/ollama_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from ollama_client import ask_ollama
import config

class OllamaTab:
    """
    Manages the UI and functionality of the 'Ollama AI' tab.
    """
    def __init__(self, app, tabs_control):
        self.app = app
        self.theme_manager = app.theme_manager

        self.frame = tk.Frame(tabs_control, bg=self.theme_manager.get_current_theme_colors()["bg"])
        tabs_control.add(self.frame, text="Ollama AI")

        self._setup_widgets()

    def _setup_widgets(self):
        # --- Model Selection ---
        model_frame = tk.Frame(self.frame, bg=self.theme_manager.get_current_theme_colors()["bg"])
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        model_label = tk.Label(model_frame, text="Select Model:")
        model_label.pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value=config.OLLAMA_MODELS[0])
        model_menu = ttk.Combobox(model_frame, textvariable=self.model_var, values=config.OLLAMA_MODELS, state="readonly")
        model_menu.pack(side=tk.LEFT, padx=5)

        self.theme_manager.register_widget(model_label, "label")

        # --- Prompt and Output ---
        prompt_label = tk.Label(self.frame, text="Your Prompt:")
        prompt_label.pack(anchor="w", padx=10)
        self.prompt_input = tk.Text(self.frame, height=5, wrap=tk.WORD)
        self.prompt_input.pack(fill=tk.X, padx=10, pady=(0,5))

        self.ask_button = tk.Button(self.frame, text="🐝 Ask PyBee", command=self.send_prompt)
        self.ask_button.pack(fill=tk.X, padx=10, pady=5)
        
        response_label = tk.Label(self.frame, text="PyBee's Response:")
        response_label.pack(anchor="w", padx=10)
        self.ollama_output = tk.Text(self.frame, height=15, font=("Courier", 10), wrap=tk.WORD)
        self.ollama_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,5))

        self.copy_button = tk.Button(self.frame, text="📋 Copy Output", command=self.copy_output)
        self.copy_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Register widgets with the theme manager
        self.theme_manager.register_widget(prompt_label, "label")
        self.theme_manager.register_widget(response_label, "label")
        self.theme_manager.register_widget(self.prompt_input, "editor")
        self.theme_manager.register_widget(self.ollama_output, "output")
        self.theme_manager.register_widget(self.ask_button, "ask_button")
        self.theme_manager.register_widget(self.copy_button, "copy_button")


    def send_prompt(self):
        prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Input Error", "Please enter a prompt.")
            return
        
        model = self.model_var.get()
        self.ollama_output.delete("1.0", tk.END)
        self.ollama_output.insert(tk.END, f"Asking Ollama with model '{model}'... please wait.")
        self.app.root.update_idletasks()

        try:
            response = ask_ollama(prompt, model)
        except Exception as e:
            response = f"An error occurred: {e}"

        self.ollama_output.delete("1.0", tk.END)
        self.ollama_output.insert(tk.END, response)

    def copy_output(self):
        try:
            pyperclip.copy(self.ollama_output.get("1.0", tk.END).strip())
            messagebox.showinfo("Success", "Output copied to clipboard!")
        except pyperclip.PyperclipException as e:
            messagebox.showerror("Clipboard Error", f"Could not copy to clipboard: {e}")

