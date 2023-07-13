import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog, LEFT, Y, BOTH

class ProductCheckbox(tk.Checkbutton):
    def __init__(self, master=None, product_name=None, **kwargs):
        self.var = tk.BooleanVar()
        super().__init__(master, text=os.path.basename(product_name), variable=self.var, **kwargs)
        self.product_name = product_name

    def process(self, sold_folder):
        if self.var.get():
            shutil.move(self.product_name, os.path.join(sold_folder, os.path.basename(self.product_name)))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.folder_to_scan_button = tk.Button(self)
        self.folder_to_scan_button["text"] = "Choose Source Folder"
        self.folder_to_scan_button["command"] = self.choose_folder_to_scan
        self.folder_to_scan_button.pack(side="top")

        self.sold_folder_button = tk.Button(self)
        self.sold_folder_button["text"] = "Choose Sold Folder"
        self.sold_folder_button["command"] = self.choose_sold_folder
        self.sold_folder_button.pack(side="top")

        self.save_button = tk.Button(self)
        self.save_button["text"] = "Save"
        self.save_button["command"] = self.save
        self.save_button.pack(side="bottom")

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill=Y)

        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill=BOTH, expand=True)

        self.checkbox_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.checkbox_frame, anchor='nw')

        self.checkbox_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(canvas))

        self.scrollbar.config(command=self.canvas.yview)

        self.checkboxes = []

    def choose_folder_to_scan(self):
        folder_to_scan = filedialog.askdirectory()
        self.clear_checkboxes()
        if folder_to_scan:
            self.folder_to_scan = folder_to_scan
            self.display_folders(self.folder_to_scan)

    def display_folders(self, folder_to_scan):
        for folder in os.listdir(folder_to_scan):
            full_folder_path = os.path.join(folder_to_scan, folder)
            if os.path.isdir(full_folder_path):
                checkbox = ProductCheckbox(self.checkbox_frame, product_name=full_folder_path)
                checkbox.pack(side="top", anchor="w")
                self.checkboxes.append(checkbox)

    def choose_sold_folder(self):
        self.sold_folder = filedialog.askdirectory()

    def clear_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.destroy()
        self.checkboxes = []

    def save(self, event=None):
        if not hasattr(self, 'sold_folder'):
            messagebox.showinfo("Error", "Please select a Sold Folder")
            return

        for checkbox in self.checkboxes:
            checkbox.process(self.sold_folder)

        self.clear_checkboxes()

        messagebox.showinfo("Success", "Processed all checked items")

        self.display_folders(self.folder_to_scan)

    def on_frame_configure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

root = tk.Tk()
root.title("Simple Inventory Manager")

# Size the window to 50% of the screen size
window_width = int(root.winfo_screenwidth() * 0.5)
window_height = int(root.winfo_screenheight() * 0.5)
root.geometry(f"{window_width}x{window_height}")

app = Application(master=root)

# Bind Enter key to save function
root.bind('<Return>', app.save)

# Bind mouse scrollwheel to scrolling function
root.bind("<MouseWheel>", app.on_mousewheel)

app.mainloop()