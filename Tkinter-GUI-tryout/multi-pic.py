import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class ImageWindow:
    def __init__(self, parent, image_path):
        self.parent = parent
        self.image_path = image_path
        self.window = tk.Toplevel(parent)
        self.window.title(os.path.basename(image_path))
        self.window.geometry("+%d+%d" % (100, 100))
        self.load_image()
        self.create_canvas()
        self.create_image()

    def load_image(self):
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, width=self.image.width, height=self.image.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_image(self):
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        x, y = event.x - self.last_x, event.y - self.last_y
        self.window.geometry("+%d+%d" % (self.window.winfo_x() + x, self.window.winfo_y() + y))

class App:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.button.pack()

    def open_image(self):
        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
        if filename:
            window = ImageWindow(self.root, filename)

root = tk.Tk()
app = App(root)
root.mainloop()
