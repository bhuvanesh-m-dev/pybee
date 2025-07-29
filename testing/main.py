# main.py
import tkinter as tk
from app import PyBee

if __name__ == "__main__":
    """
    Main entry point for the PyBee application.
    """
    root = tk.Tk()
    app = PyBee(root)
    root.mainloop()

