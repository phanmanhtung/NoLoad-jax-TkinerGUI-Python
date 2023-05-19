<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
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

    def create_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


class App:
    def __init__(self, root, myoptions):
        self.root = root
        #self.root.title("Data Visualization")
        #self.root.geometry("400x300")
        self.x_options = []  # Empty list for X options initially
        self.y_options = []  # Empty list for Y options initially
        self.selected_x = tk.StringVar()
        self.selected_y = tk.StringVar()
        self.create_widgets()
        self.myoptions = myoptions

    def create_widgets(self):
        self.option_frame = ttk.Frame(self.root)
        self.option_frame.pack(padx=10, pady=10)

        self.x_label = ttk.Label(self.option_frame, text="X:")
        self.x_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.x_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_x, values=self.x_options)
        self.x_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.y_label = ttk.Label(self.option_frame, text="Y:")
        self.y_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.y_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_y, values=self.y_options)
        self.y_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.plot_button = ttk.Button(self.option_frame, text="Plot", command=self.plot)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.exit_button = ttk.Button(self.option_frame, text="Exit", command=sys.exit)
        self.exit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def update_options(self, x_options, y_options):
        self.x_options = x_options
        self.y_options = y_options
        self.x_combobox['values'] = self.x_options
        self.y_combobox['values'] = self.y_options

    def plot(self):
        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        # Get the arrays of values for the selected options
        x_values = self.myoptions[selected_x]
        y_values = self.myoptions[selected_y]

        fig, ax = plt.subplots()
        ax.scatter(x_values, y_values)
        ax.set_xlabel(selected_x)
        ax.set_ylabel(selected_y)
        ax.set_title(f"{selected_x} vs {selected_y}")

        # Avoid scientific notations
        ax.ticklabel_format(useOffset=False, style='plain')

        window = ImageWindow(self.root, fig, f"{selected_x} vs {selected_y}")

=======
import tkinter as tk
from tkinter import ttk
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

    def create_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


class App:
    def __init__(self, root, myoptions):
        self.root = root
        #self.root.title("Data Visualization")
        #self.root.geometry("400x300")
        self.x_options = []  # Empty list for X options initially
        self.y_options = []  # Empty list for Y options initially
        self.selected_x = tk.StringVar()
        self.selected_y = tk.StringVar()
        self.create_widgets()
        self.myoptions = myoptions

    def create_widgets(self):
        self.option_frame = ttk.Frame(self.root)
        self.option_frame.pack(padx=10, pady=10)

        self.x_label = ttk.Label(self.option_frame, text="X:")
        self.x_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.x_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_x, values=self.x_options)
        self.x_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.y_label = ttk.Label(self.option_frame, text="Y:")
        self.y_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.y_combobox = ttk.Combobox(self.option_frame, textvariable=self.selected_y, values=self.y_options)
        self.y_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.plot_button = ttk.Button(self.option_frame, text="Plot", command=self.plot)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.exit_button = ttk.Button(self.option_frame, text="Exit", command=sys.exit)
        self.exit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def update_options(self, x_options, y_options):
        self.x_options = x_options
        self.y_options = y_options
        self.x_combobox['values'] = self.x_options
        self.y_combobox['values'] = self.y_options

    def plot(self):
        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        # Get the arrays of values for the selected options
        x_values = self.myoptions[selected_x]
        y_values = self.myoptions[selected_y]

        fig, ax = plt.subplots()
        ax.scatter(x_values, y_values)
        ax.set_xlabel(selected_x)
        ax.set_ylabel(selected_y)
        ax.set_title(f"{selected_x} vs {selected_y}")

        # Avoid scientific notations
        ax.ticklabel_format(useOffset=False, style='plain')

        window = ImageWindow(self.root, fig, f"{selected_x} vs {selected_y}")

>>>>>>> main
