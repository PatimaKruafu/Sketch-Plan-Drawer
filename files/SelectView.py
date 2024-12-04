import tkinter as tk
from tkinter import filedialog

def change_camera_view(view):
    print(f"Changing camera view to {view}")

def show_projection(projection):
    print(f"Showing {projection} projection")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write("Save data")
        print(f"File saved to {file_path}")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        print(f"File loaded from {file_path}\nData: {data}")

app = tk.Tk()
app.title("Control Panel")

# Create frames for layout
frame_projections = tk.Frame(app)
frame_isometric_views = tk.Frame(app)
frame_save_load = tk.Frame(app)

# Projection buttons
projections = ["Front", "Top", "Side"]
for projection in projections:
    button = tk.Button(frame_projections, text=projection, command=lambda p=projection: show_projection(p))
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Camera view buttons
camera_views = ["Isometric 1", "Isometric 2", "Isometric 3", "Isometric 4"]
for view in camera_views:
    button = tk.Button(frame_isometric_views, text=view, command=lambda v=view: change_camera_view(v))
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Save and Load buttons
save_button = tk.Button(frame_save_load, text="Save", command=save_file)
save_button.grid(row=0, column=0, padx=5, pady=5)

load_button = tk.Button(frame_save_load, text="Load", command=load_file)
load_button.grid(row=0, column=1, padx=5, pady=5)

# Pack frames into the main window
frame_projections.pack(pady=10)
frame_isometric_views.pack(pady=10)
frame_save_load.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

app.mainloop()