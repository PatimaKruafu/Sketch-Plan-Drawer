import json
import tkinter as tk
from tkinter import filedialog, messagebox

points = []

# ฟังก์ชันสำหรับเพิ่มจุดพิกัด
def add_point(x, y, z):
    points.append({'x': x, 'y': y, 'z': z})
    update_points_display()

# ฟังก์ชันสำหรับบันทึกจุดพิกัดลงในไฟล์
def save_points():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, 'w') as file:
            json.dump(points, file)
        messagebox.showinfo("Save Points", "Points saved successfully!")

# ฟังก์ชันสำหรับโหลดจุดพิกัดจากไฟล์
def load_points():
    global points
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, 'r') as file:
            points = json.load(file)
        update_points_display()
        messagebox.showinfo("Load Points", "Points loaded successfully!")

# ฟังก์ชันสำหรับลบจุดพิกัด
def delete_point(index):
    if 0 <= index < len(points):
        del points[index]
        update_points_display()
        messagebox.showinfo("Delete Point", "Point deleted successfully!")
    else:
        messagebox.showerror("Delete Point", "Invalid index!")

# ฟังก์ชันสำหรับอัปเดตการแสดงผลจุดพิกัด
def update_points_display():
    points_display.delete(1.0, tk.END)
    for i, point in enumerate(points):
        points_display.insert(tk.END, f"{i}: x: {point['x']}, y: {point['y']}, z: {point['z']}\n")

# ฟังก์ชันสำหรับเพิ่มจุดพิกัดจากอินพุตของผู้ใช้
def add_point_from_input():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        add_point(x, y, z)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for x, y, and z.")

# ฟังก์ชันสำหรับลบจุดพิกัดจากอินพุตของผู้ใช้
def delete_point_from_input():
    try:
        index = int(entry_index.get())
        delete_point(index)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid index.")

# สร้างหน้าต่างหลักของโปรแกรม
root = tk.Tk()
root.title("Point Manager")

# สร้างอินพุตสำหรับ x, y, z
tk.Label(root, text="x:").grid(row=0, column=0)
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)

tk.Label(root, text="y:").grid(row=1, column=0)
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)

tk.Label(root, text="z:").grid(row=2, column=0)
entry_z = tk.Entry(root)
entry_z.grid(row=2, column=1)

# สร้างปุ่มสำหรับเพิ่มจุดพิกัด
tk.Button(root, text="Add Point", command=add_point_from_input).grid(row=3, column=0, columnspan=2)

# สร้างปุ่มสำหรับบันทึกจุดพิกัดลงในไฟล์
tk.Button(root, text="Save Points", command=save_points).grid(row=4, column=0, columnspan=2)

# สร้างปุ่มสำหรับโหลดจุดพิกัดจากไฟล์
tk.Button(root, text="Load Points", command=load_points).grid(row=5, column=0, columnspan=2)

# สร้างอินพุตสำหรับดัชนีที่ต้องการลบ
tk.Label(root, text="Index to delete:").grid(row=6, column=0)
entry_index = tk.Entry(root)
entry_index.grid(row=6, column=1)

# สร้างปุ่มสำหรับลบจุดพิกัด
tk.Button(root, text="Delete Point", command=delete_point_from_input).grid(row=7, column=0, columnspan=2)

# สร้างพื้นที่สำหรับแสดงผลจุดพิกัด
points_display = tk.Text(root, height=10, width=30)
points_display.grid(row=8, column=0, columnspan=2)

# เริ่มต้นโปรแกรม
root.mainloop()