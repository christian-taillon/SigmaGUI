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
input_panel = tk.Frame(window, width=200, height=400, bg="white")
input_panel.pack(side=tk.LEFT)

input_label = tk.Label(input_panel, text="Input:")
input_label.pack()

input_text = tk.Text(input_panel, width=30, height=10)
input_text.pack()

# Create the output panel
output_panel = tk.Frame(window, width=400, height=400, bg="white")
output_panel.pack(side=tk.RIGHT)

output_label = tk.Label(output_panel, text="Output:")
output_label.pack()

output_text = tk.Text(output_panel, width=50, height=10)
output_text.pack()

# Create the backend input field
backend_label = tk.Label(input_panel, text="Backend:")
backend_label.pack()

backends = get_backend_list()
backend_var = tk.StringVar(input_panel)
backend_var.set(backends[0] if backends else "")  # Set the default value
backend_dropdown = tk.OptionMenu(input_panel, backend_var, *backends)
backend_dropdown.pack()

# Create the pipeline input field
pipeline_label = tk.Label(input_panel, text="Pipeline:")
pipeline_label.pack()

pipelines = get_pipeline_list()
pipeline_var = tk.StringVar(input_panel)
pipeline_var.set(pipelines[0] if pipelines else "")  # Set the default value
pipeline_dropdown = tk.OptionMenu(input_panel, pipeline_var, *pipelines)
pipeline_dropdown.pack()

# Create the process button
process_button = tk.Button(input_panel, text="Process", command=process_text)
process_button.pack()

# Start the GUI main loop
window.mainloop()
