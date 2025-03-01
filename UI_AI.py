import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
from CV_AI import start_up  # Assuming this is your AI function4: NOT FOUND

# Variables to store file paths
path_to_crit = None
path_to_CVs = []  # Change to a list to store multiple file paths
processing_done = False  # Global flag to track progress

def browse_file():
    global path_to_crit
    path_to_crit = filedialog.askopenfilename()
    if path_to_crit:
        criteria_entry.delete(0, tk.END)
        criteria_entry.insert(0, path_to_crit)

def browse_file2():
    global path_to_CVs
    files = filedialog.askopenfilenames()
    if files:
        path_to_CVs = list(files)
        cvs_entry.delete(0, tk.END)
        cvs_entry.insert(0, ", ".join(path_to_CVs))

def update_progress():
    """ Continuously update progress bar while AI function is running. """
    global processing_done
    pb["value"] = 0  # Reset progress
    while not processing_done:  # Run until AI processing is done
        pb["value"] = (pb["value"] + 5) % 100  # Increase progress cyclically
        not_label.config(text=f"Processing... {pb['value']}%")  
        root.update_idletasks()
        time.sleep(0.2)  # Adjust speed if necessary

    pb["value"] = 100  # Ensure it reaches 100% when done
    not_label.config(text="DONE!")

def process_data():
    """ Runs the AI function and stops progress when done. """
    global processing_done
    processing_done = False  # Reset flag
    
    user_prompt = f"\nMaximum rating score must be: {max_rating_score.get().strip()}\n" \
                  f"To pass, the minimum score to pass must be: {min_passing_score.get().strip()}"

    response = start_up(path_to_crit, ";".join(path_to_CVs), user_prompt)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)
    output_text.config(state="disabled")

    processing_done = True  # Mark processing as done

def send():
    global processing_done
    processing_done = False  # Ensure the flag is reset

    error_label.config(text="Applicant's result:")

    if (path_to_crit and path_to_CVs) and (int(max_rating_score.get().strip()) > int(min_passing_score.get().strip())):
        not_label.config(text="Loading...")
        # Start progress bar updater
        threading.Thread(target=update_progress, daemon=True).start()
        # Start AI processing in a separate thread
        threading.Thread(target=process_data, daemon=True).start()
    elif not path_to_crit or not path_to_CVs:
        error_label.config(text="Error: Please select BOTH files.")
    else:
        error_label.config(text="Error: Minimum passing score must be\n SMALLER than Maximum ratings.")

def download():
    if output_text.compare("end-1c", "==", "1.0"):
        error_label.config(text="Error: No content to be downloaded")
    else: 
        a = output_text.get("1.0", "end-1c")
        print(a)
        folder_path = filedialog.askdirectory()
        down_file = folder_path + "/Applicants_result_file.txt"
        with open(down_file, "w", encoding='utf-8') as f:
            f.write(a)
            f.close()

# GUI Setup
root = tk.Tk()
root.title("CV Scanner AI")
root.geometry("400x350")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

criteria_label = tk.Label(frame, text="Criteria: ", font=("TkDefaultFont", 9, "bold"))
criteria_label.grid(row=0, column=0, sticky="w")

criteria_entry = tk.Entry(frame, width=40)
criteria_entry.grid(row=0, column=1, sticky="w")

criteria_browse_button = tk.Button(frame, text="Browse", command=browse_file)
criteria_browse_button.grid(row=0, column=2)

cvs_label = tk.Label(frame, text="CVs file(s): ", font=("TkDefaultFont", 9, "bold"))
cvs_label.grid(row=1, column=0, sticky="w")

cvs_entry = tk.Entry(frame, width=40)
cvs_entry.grid(row=1, column=1, sticky="w")

cvs_browse_button = tk.Button(frame, text="Browse", command=browse_file2)
cvs_browse_button.grid(row=1, column=2)

max_rating_score = tk.StringVar(value="10")
min_passing_score = tk.StringVar(value="5")

max_rating_label = tk.Label(frame, text="Max Rating:", font=("TkDefaultFont", 9, "bold"))
max_rating_label.grid(row=3, column=0, sticky="w")

max_rating_combobox = ttk.Combobox(frame, textvariable=max_rating_score, width=5)
max_rating_combobox['values'] = ("4", "5", "10", "40", "50", "100")
max_rating_combobox.current(2)
max_rating_combobox.grid(row=3, column=1, sticky="w")

min_passing_label = tk.Label(frame, text="Min rating:", font=("TkDefaultFont", 9, "bold"))
min_passing_label.grid(row=3, column=1, sticky="")

min_passing_combobox = ttk.Combobox(frame, textvariable=min_passing_score, width=5)
min_passing_combobox['values'] = ("2", "3", "5", "20", "25", "50")
min_passing_combobox.current(2)
min_passing_combobox.grid(row=3, column=1, sticky="e")

send_button = tk.Button(frame, text="Send", command=send)
send_button.grid(row=5, column=1, sticky="n")

error_label = tk.Label(frame, text="Welcome to CV Scanner AI", fg="red")
error_label.grid(row=6, column=1)

output_label = tk.Label(frame, text="Output: ", font=("TkDefaultFont", 9, "bold"))
output_label.grid(row=7, column=0, sticky="w")

output_text = tk.Text(frame, height=10, width=34, state="disabled")
output_text.grid(row=7, column=1, sticky="w")

download = tk.Button(frame, text="Export", command=download)
download.grid(row=7, column = 2)

pb = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=280, maximum=100)
pb.grid(row=8, column=0, columnspan=3, pady=10)

not_label = tk.Label(frame, text="Loading bar", fg="green")
not_label.grid(row=9, column=1)

root.mainloop()
