# Author: Christian Taillon
# Date: 2023-06-02
#
# Description:
# This tool creates a cross-platform GUI that allows users to write text into an input panel.
# By selecting a backend and pipeline from the dropdown menus and clicking the "Process" button,
# the tool passes the user's input to the sigma command-line tool. The output is displayed in an
# output panel. The user's input is temporarily saved in a YAML file, which is used as input for
# the sigma tool. After the command is processed, the temporary file is deleted. This is only because I don't know how to do it otherwise.


import tkinter as tk
import subprocess
import tempfile
import os

def get_backend_list():
    backends = [
        "splunk",
        "insightidr",
        "qradar",
        "elasticsearch",
        "opensearch"
    ]
    return backends

def get_pipeline_list():
    pipelines = [
        "sysmon",
        "crowdstrike_fdr",
        "splunk_windows",
        "splunk_sysmon_acceleration",
        "splunk_cim",
        "ecs_windows",
        "ecs_windows_old",
        "ecs_zeek_beats",
        "ecs_zeek_corelight",
        "zeek",
        "windows"
    ]
    return pipelines

def process_text():
    text = input_text.get("1.0", tk.END).strip()
    backend = backend_var.get().strip()
    pipeline = pipeline_var.get().strip()

    try:
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".yaml") as temp_file:
            temp_file.write(text)
            temp_file_name = temp_file.name

        # Build the command
        command = f"sigma convert -t {backend} -p {pipeline} {temp_file_name}"

        # Run the command and capture the output
        output = subprocess.check_output(command, shell=True, encoding='utf-8')

        # Update the output text
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)
    except subprocess.CalledProcessError as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {e}")
    finally:
        # Delete the temporary file
        if temp_file_name:
            os.remove(temp_file_name)

# Create the main window
window = tk.Tk()
window.title("Sigma Tool")
window.geometry("600x400")

# Create the input panel
input_panel = tk.Frame(window, bg="white")
input_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

input_label = tk.Label(input_panel, text="Input:", font=("Arial", 14, "bold"))
input_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

input_text = tk.Text(input_panel, width=30, height=10)
input_text.pack(padx=10, pady=(0, 10))

# Create the backend input field
backend_label = tk.Label(input_panel, text="Backend:", font=("Arial", 12))
backend_label.pack(anchor=tk.W, padx=10)

backends = get_backend_list()
backend_var = tk.StringVar(input_panel)
backend_var.set(backends[0] if backends else "")  # Set the default value
backend_dropdown = tk.OptionMenu(input_panel, backend_var, *backends)
backend_dropdown.pack(padx=10, pady=(0, 10), fill=tk.X)

# Create the pipeline input field
pipeline_label = tk.Label(input_panel, text="Pipeline:", font=("Arial", 12))
pipeline_label.pack(anchor=tk.W, padx=10)

pipelines = get_pipeline_list()
pipeline_var = tk.StringVar(input_panel)
pipeline_var.set(pipelines[0] if pipelines else "")  # Set the default value
pipeline_dropdown = tk.OptionMenu(input_panel, pipeline_var, *pipelines)
pipeline_dropdown.pack(padx=10, pady=(0, 10), fill=tk.X)

# Create the process button
process_button = tk.Button(window, text="Process", font=("Arial", 14), command=process_text)
process_button.pack(side=tk.BOTTOM, pady=10)

# Create the output panel
output_panel = tk.Frame(window, bg="white")
output_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

output_label = tk.Label(output_panel, text="Output:", font=("Arial", 14, "bold"))
output_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

output_text = tk.Text(output_panel, width=50, height=10)
output_text.pack(padx=10, pady=(0, 10))

# Start the GUI main loop
window.mainloop()
