import tkinter as tk
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import pandas as pd

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys


# Path to your XML file
xml_file_path = "example20.result"

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
bounds = {'p': [1.0, 20.0], 'f': [1.0, 1000.0], 'Ns': [1000.0, 1150.0],
          'Isa': [0.1, 100.0], 'j': [1.0, 10.0], 'g': [0.001, 1.0],
          'Ld': [0.001, 0.2], 'He': [0.001, 0.5], 'Lc': [0.001, 0.5],
          'Hc': [0.001, 0.5], 'Ps': [0.005, 1.0], 'ent': [0.002, 0.003],
          'd': [0.01, 0.1], 'Tinduit': [700.0, 720.0], 'Tbob': [100.0, 120.0]}
unbounds = option_list - bounds.keys()
objectives=['Volume','PertesTotales']

for i in unbounds:
  bounds[i] = []


### Exclude Dominated Point ###

pareto_pts = df[objectives].values.tolist()

def exclude_dominated_points(pareto_front):
    """Filters a list of points in the Pareto front to exclude any dominated points.
    
    Args:
        pareto_front (list): A list of lists representing points in the Pareto front.
    
    Returns:
        A filtered list of lists representing non-dominated points in the Pareto front.
    """
    filtered_pareto_front = []
    for i, point1 in enumerate(pareto_front):
        dominated = False
        for j, point2 in enumerate(pareto_front):
            if i == j:
                continue
            if all(p1 >= p2 for p1, p2 in zip(point1, point2)):
                dominated = True
                break
        if not dominated:
            filtered_pareto_front.append(point1)
    return filtered_pareto_front

new_pareto_pts = exclude_dominated_points(pareto_pts)
updated_df = pd.DataFrame(new_pareto_pts, columns = objectives)


### Functions to plot results

def plot_result(df, target, bound=[]):
  fig, ax = plt.subplots()
  ax.scatter(df['IterationNumber'], df[target])
  ax.grid()

  for i in bound:
     ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')

  ax.set_xlabel("IterationNumber")
  ax.set_ylabel(target)
  ax.set_title(target)
  ax.xaxis.set_major_locator(MaxNLocator(integer=True))

  return fig

def plot_pareto(df):
  fig, ax = plt.subplots()
  ax.scatter(df[objectives[0]], df[objectives[1]])
  ax.set_xlabel(objectives[0])
  ax.set_ylabel(objectives[1])
  ax.set_title("Pareto")

  return fig

def create_plot(option):
  if option == "Pareto": return plot_pareto(df)
  elif option == "Updated_Pareto" : return plot_pareto(updated_df)
  else:
    for i in range(len(option_list)):
       if option == option_list[i] : return plot_result(df, option, bounds[option])

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
options = ["Updated_Pareto", "Pareto"] + option_list # Define your options list here
app = App(root, options)	
root.mainloop()

