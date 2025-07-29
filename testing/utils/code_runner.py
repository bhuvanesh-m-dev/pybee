# utils/code_runner.py
import subprocess

def run_code(editor_tab_instance):
    """
    Executes the Python code from the editor in a separate process
    and displays the output.
    """
    code = editor_tab_instance.editor.get("1.0", "end")
    output_widget = editor_tab_instance.output_text
    
    output_widget.delete("1.0", "end")
    
    if not code.strip():
        output_widget.insert("end", "No code to run.")
        return

    try:
        # Using CREATE_NO_WINDOW flag to prevent console popup on Windows
        result = subprocess.check_output(
            ["python", "-c", code], 
            stderr=subprocess.STDOUT, 
            text=True, 
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    except FileNotFoundError:
        result = "Error: Python interpreter not found. Make sure Python is in your system's PATH."
    except Exception as e:
        result = f"An unexpected error occurred during execution:\n{e}"
        
    output_widget.insert("end", result)

