# config.py

# --- Application Constants ---
CONFIG_FILE = "pybee_config.json"
DEFAULT_GEOMETRY = "900x700"
RECENT_FILES_LIMIT = 10

# --- Model Definitions ---
OLLAMA_MODELS = ["tinyllama", "llama2", "gemma:2b", "phi"] 

# --- Theme Colors ---
THEMES = {
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#d0d0d0",
        "editor_bg": "#1e1e1e",
        "editor_fg": "white",
        "output_bg": "#000000",
        "output_fg": "#00ff00",
        "button_bg": "#4a4a4a",
        "button_fg": "white",
        "accent_color": "#007acc",
        "run_button_bg": "#4caf50",
        "ask_button_bg": "#2196f3",
        "copy_button_bg": "#9c27b0",
    },
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "editor_bg": "#ffffff",
        "editor_fg": "black",
        "output_bg": "#e0e0e0",
        "output_fg": "blue",
        "button_bg": "#dcdcdc",
        "button_fg": "black",
        "accent_color": "#0078d7",
        "run_button_bg": "#66bb6a",
        "ask_button_bg": "#42a5f5",
        "copy_button_bg": "#ab47bc",
    }
}

