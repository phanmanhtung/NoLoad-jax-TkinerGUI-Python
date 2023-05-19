import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class ImageWindow:
    def __init__(self, parent, fig):
        self.parent = parent
        self.fig = fig
        self.window = tk.Toplevel(parent)
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

def create_plot(option):
    if option == "scatter":
        # Example scatter plot
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Scatter Plot")
    
    elif option == "line":
        # Example line plot
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Line Plot")
    
    elif option == "bar":
        # Example bar plot
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Bar Plot")

    return fig

class App:
    def __init__(self, root, options):
        self.root = root
        self.options = options
        self.selected_option = None
        self.create_widgets()

    def create_widgets(self):
        self.option_var = tk.StringVar(value=self.options)
        self.option_listbox = tk.Listbox(self.root, listvariable=self.option_var, selectmode=tk.SINGLE)
        self.option_listbox.pack(padx=10, pady=5)

        self.plot_button = tk.Button(self.root, text="Plot", command=self.plot_selected_option)
        self.plot_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

    def plot_selected_option(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_option = self.options[index]
            fig = create_plot(self.selected_option)
            window = ImageWindow(self.root, fig)

    def exit_program(self):
        sys.exit()


root = tk.Tk()
options = ["scatter", "line", "bar"] # Define your options list here
app = App(root, options)
root.mainloop()
