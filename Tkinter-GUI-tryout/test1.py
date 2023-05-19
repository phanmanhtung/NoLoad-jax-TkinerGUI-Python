import tkinter as tk
from PIL import ImageTk
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import pandas as pd

import sys

import tkinter as tk
from PIL import ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

bounds={'x':[-2., 2.],'y':[-2, 2]}
ineq_cstr={'ctr1':[None, 0],'ctr2':[None, 0]}

def plot_result(df, target, bound):
  fig, ax = plt.subplots()
  ax.scatter(df['IterationNumber'], df[target])
  ax.grid()

  for i in bound:
     ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')
  return fig

def create_plot():
  return plot_result(df, 'x', bounds['x'])

class App:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.button = tk.Button(self.root, text="Open Results", command=self.open_results)
        self.button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()

    def open_results(self):
        fig = create_plot()
        window = ImageWindow(self.root, fig)

    def exit_program(self):
        self.root.destroy()
        sys.exit(0)

root = tk.Tk()
app = App(root)
root.mainloop()
