import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from CV_AI import start_up
import threading

#Let user choose how much to pass

path_to_crit = None
path_to_CVs = None

def probar(stoporgo):
    # root window
    root = tk.Tk()
    root.geometry('300x120')
    root.title('Progressbar Demo')
    root.grid()

    # progressbar
    pb = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    # place the progressbar
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
    if stoporgo != 0:
        pb.start()
    else:
        pb.stop()
    root.mainloop()

def browse_file():
    global path_to_crit
    # Open a file dialog and store the selected file's path
    path_to_crit = filedialog.askopenfilename()
    if path_to_crit:
        criteria_entry.delete(0, tk.END)      # Clear existing text
        criteria_entry.insert(0, path_to_crit)  # Insert the file path

def browse_file2():
    global path_to_CVs
    path_to_CVs = filedialog.askopenfilename()
    if path_to_CVs:
        cvs_entry.delete(0, tk.END)
        cvs_entry.insert(0, path_to_CVs)

def send2get(user_prompt):
    response = start_up(path_to_crit, path_to_CVs, user_prompt)
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)
    output_text.config(state="disabled")

def start_progress_bar():
    pb.start()

def stop_progress_bar():
    pb.stop()

def send():
    error_label.config(text="Applicant's result:")
    not_label.config(text="Loading...")
    if (path_to_crit != None or path_to_CVs != None) and (int(max_rating_score.get().strip()) > int(min_passing_score.get().strip())):
        user_prompt = f"\nMaximum rating score must be: {max_rating_score.get().strip()}\nTo pass, the minimum score to pass must be: {min_passing_score.get().strip()}"
        start_progress_bar()  # Start the progress bar

        # Run send2get in a separate thread
        def task():
            try:
                send2get(user_prompt)
            finally:
                stop_progress_bar()  # Stop the progress bar after the task completes
                not_label.config(text="DONE!")

        t = threading.Thread(target=task)
        t.start()
    elif path_to_crit == None or path_to_CVs == None:
        error_label.config(text="Error: Please select BOTH files.")
    else:
        error_label.config(text="Error: Minimum passing score must be\n SMALLER than the Maximum ratings.")

# Create the main window
root = tk.Tk()
root.title("CV Scanner AI")
root.geometry("400x350")
root.resizable(False, False)

# Create form-style layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Criteria file selection row
criteria_label = tk.Label(frame, text="Criteria: ", anchor="w", width=8, font=("TkDefaultFont", 9, "bold"))
criteria_label.grid(row=0, column=0, sticky="w")

criteria_entry = tk.Entry(frame, width=40, state="normal")
criteria_entry.grid(row=0, column=1, sticky="w")

criteria_browse_button = tk.Button(frame, text="Browse", command=browse_file, activebackground="blue", activeforeground="white", height=1, width=7, pady=1,
                    font=("TkDefaultFont", 9, "normal"))
criteria_browse_button.grid(row=0, column=2)

# CVs file selection row
cvs_label = tk.Label(frame, text="CVs file: ", anchor="w", width=8, font=("TkDefaultFont", 9, "bold"))
cvs_label.grid(row=1, column=0, sticky="w")

cvs_entry = tk.Entry(frame, width=40, state="normal")
cvs_entry.grid(row=1, column=1, sticky="w")

cvs_browse_button = tk.Button(frame, text="Browse", command=browse_file2, activebackground="blue", activeforeground="white", height=1, width=7, pady=1,
                    font=("TkDefaultFont", 9, "normal"))
cvs_browse_button.grid(row=1, column=2)

# Additional variables
max_rating_score = tk.StringVar(value="10")  # Default value

# Add "Maximum rating score" label and Combobox near the prompt input
max_rating_label = tk.Label(frame, text="Max Rating:", anchor="w", width=10, font=("TkDefaultFont", 9, "bold"))
max_rating_label.grid(row=3, column=0, sticky="w")  # Adjust grid placement for proximity to prompt input

max_rating_combobox = ttk.Combobox(frame, textvariable=max_rating_score, width=5)
max_rating_combobox['values'] = ("4", "5", "10", "40", "50", "100")  # Set values for the combobox
max_rating_combobox.current(2)  # Default to the 3rd value ("10")
max_rating_combobox.grid(row=3, column=1, sticky="w")  # Adjust grid placement

# Choose minimum passing score label similar to the Maximum
min_passing_label = tk.Label(frame, text="Min rating:", anchor="w", width=10, font=("TkDefaultFont", 9, "bold"))
min_passing_label.grid(row=3, column=1, sticky="")

min_passing_score = tk.StringVar(value="5")

min_passing_combobox = ttk.Combobox(frame, textvariable=min_passing_score, width=5)
min_passing_combobox['values'] = ("2", "3", "5", "20", "25", "50")
min_passing_combobox.current(2)  # Default to the 3rd value ("5") as 5 is half of 10
min_passing_combobox.grid(row=3, column=1, sticky="e")

# Space between input and output
space = tk.Label(frame, text="", anchor="w", width=10, font=("TkDefaultFont", 9, "bold"))
space.grid(row=4, column=1, sticky="e")

# Send button
send_button = tk.Button(frame, text="Send", command=send, activebackground="green", activeforeground="white", height=2, width=8, pady=1,
                    font=("TkDefaultFont", 10, "normal"))
send_button.grid(row=5, column=1, sticky="n")

# Error label
error_label = tk.Label(frame, text="Hello, welcome to CV scanning AI", fg="red")
error_label.grid(row=6, column=1, sticky="")

# Output text area
output_label = tk.Label(frame, text="Output: ", anchor="w", width=8, font=("TkDefaultFont", 9, "bold"))
output_label.grid(row=7, column=0, sticky="w")
output_text = tk.Text(frame, height=10, width=34, state="disabled")
output_text.grid(row=7, column=1, sticky="w")

# Progress bar
pb = ttk.Progressbar(frame, orient='horizontal', mode='indeterminate', length=280)
pb.grid(row=8, column=0, columnspan=3, pady=10)

# Notif bar
not_label = tk.Label(frame, text="Loading bar", fg="green")
not_label.grid(row=9, column=1, sticky="n")

# Run the application
root.mainloop()

#bùm chát bum-bùm bùm bùm v - chát bum
