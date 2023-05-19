import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys


class ImageWindow:
    def __init__(self, parent, fig, option):
        self.parent = parent
        self.fig = fig
        self.option = option
        self.window = tk.Toplevel(parent)
        self.window.title(option)
        self.window.geometry("+%d+%d" % (100, 100))
        self.create_canvas()
        self.create_image()

    def create_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_image(self):
        self.canvas.get_tk_widget().bind("<Button-1>", self.on_click)
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        x, y = event.x - self.last_x, event.y - self.last_y
        self.window.geometry("+%d+%d" % (self.window.winfo_x() + x, self.window.winfo_y() + y))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualization")
        self.root.geometry("400x300")
        self.options = ["scatter", "line", "bar"]
        self.selected_x = tk.StringVar()
        self.selected_y = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.option_frame = ttk.Frame(self.root)
        self.option_frame.pack(padx=10, pady=10)

        self.x_label = ttk.Label(self.option_frame, text="X:")
        self.x_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.x_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_x, values=self.options)
        self.x_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.y_label = ttk.Label(self.option_frame, text="Y:")
        self.y_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.y_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_y, values=self.options)
        self.y_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.plot_button = ttk.Button(self.option_frame, text="Plot", command=self.plot)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.exit_button = ttk.Button(self.option_frame, text="Exit", command=sys.exit)
        self.exit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def plot(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        fig, ax = plt.subplots()
        if selected_x == "scatter" and selected_y == "scatter":
            ax.scatter(x, y)
        elif selected_x == "line" and selected_y == "line":
            ax.plot(x, y)
        elif selected_x == "bar" and selected_y == "bar":
            ax.bar(x, y)

        window = ImageWindow(self.root, fig, f"{selected_x} vs {selected_y}")


root = tk.Tk()
app = App(root)
root.mainloop()
