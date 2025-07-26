# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pyperclip
from ollama_client import ask_ollama

def run_code():
    code = editor.get("1.0", tk.END)
    try:
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def send_prompt():
    prompt = prompt_input.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("No Prompt", "Please enter a prompt.")
        return
    response = ask_ollama(prompt)
    ollama_output.delete("1.0", tk.END)
    ollama_output.insert(tk.END, response)

def copy_output():
    pyperclip.copy(ollama_output.get("1.0", tk.END).strip())
    messagebox.showinfo("Copied", "Output copied to clipboard!")

app = tk.Tk()
app.title("Ankyger Editor")
app.geometry("900x600")

# ---- Tab Control ----
tabs = ttk.Notebook(app)
tabs.pack(fill="both", expand=True)

# =================== TAB 1: Code Editor ===================
editor_tab = tk.Frame(tabs, bg="black")
tabs.add(editor_tab, text="Editor")

editor = tk.Text(editor_tab, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12))
editor.pack(fill=tk.BOTH, expand=True)

run_button = tk.Button(editor_tab, text="▶ Run Code", command=run_code, bg="#4caf50", fg="white")
run_button.pack(fill=tk.X)

output_text = tk.Text(editor_tab, height=10, bg="#000", fg="lime", font=("Consolas", 10))
output_text.pack(fill=tk.BOTH)

# =================== TAB 2: Ollama LLM ===================
ollama_tab = tk.Frame(tabs, bg="#222")
tabs.add(ollama_tab, text="Ollama LLM")

prompt_label = tk.Label(ollama_tab, text="Prompt", bg="#222", fg="white")
prompt_label.pack(anchor="w", padx=10, pady=5)

prompt_input = tk.Text(ollama_tab, height=6, bg="#1e1e1e", fg="white", insertbackground="white")
prompt_input.pack(fill=tk.X, padx=10)

ask_button = tk.Button(ollama_tab, text="🧠 Ask Ollama", command=send_prompt, bg="#2196f3", fg="white")
ask_button.pack(fill=tk.X, padx=10, pady=5)

ollama_output = tk.Text(ollama_tab, height=15, bg="black", fg="cyan", font=("Courier", 10))
ollama_output.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

copy_button = tk.Button(ollama_tab, text="📋 Copy Output", command=copy_output, bg="#9c27b0", fg="white")
copy_button.pack(fill=tk.X, padx=10)

app.mainloop()
