import tkinter as tk
from PIL import ImageTk
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import pandas as pd

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

# Path to your XML file
xml_file_path = "rosenbrock.result"

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Extract data from XML
data = []
for iteration in root.iter("Iteration"):
    iteration_number = int(iteration.get("Number"))
    is_best_solution = iteration.get("isBestSolution")
    is_solution = iteration.get("isSolution")
    inputs = iteration.find("Inputs")
    outputs = iteration.find("Outputs")

    inputs_data = {input_elem.get("Name"): float(input_elem.get("Value")) for input_elem in inputs.iter("Input")}
    outputs_data = {output_elem.get("Name"): float(output_elem.get("Value")) for output_elem in outputs.iter("Output")}

    iteration_data = {
        "IterationNumber": iteration_number,
        "IsBestSolution": is_best_solution,
        "IsSolution": is_solution,
        **inputs_data,
        **outputs_data
    }
    data.append(iteration_data)

# Convert data to DataFrame
df = pd.DataFrame(data)
option_list = df.columns[3:].values.tolist()

# Define all bounds here
bounds={'x':[-2., 2.],'y':[-2, 2], 'ctr1':[0],'ctr2':[0]}
unbounds=option_list -bounds.keys()
for i in unbounds:
  bounds[i] = []

def plot_result(df, target, bound=[]):
  fig, ax = plt.subplots()
  ax.scatter(df['IterationNumber'], df[target])
  ax.grid()

  for i in bound:
     ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')
  return fig

def create_plot(option):
  for i in range(len(option_list)):
    if option == option_list[i] : return plot_result(df, option, bounds[option])

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
            selected_option = self.options[index]
            fig = create_plot(selected_option)
            window = ImageWindow(self.root, fig, selected_option)


    def exit_program(self):
        sys.exit()

root = tk.Tk()
options = option_list # Define your options list here
app = App(root, options)
root.mainloop()

