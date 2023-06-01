import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

### Exclude Dominated Point ###

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

def excluded_dataframe(df, objectives):
    pareto_pts = df[objectives].values.tolist()
    new_pareto_pts = exclude_dominated_points(pareto_pts)
    updated_df = pd.DataFrame(new_pareto_pts, columns = objectives)
    return updated_df

### Functions to plot results ###

def plot_result(df, target, bound=[]):

    fig, ax = plt.subplots()
    ax.scatter(df['IterationNumber'], df[target])

    ax.grid()
    ax.set_xlabel("IterationNumber")
    ax.set_ylabel(target)
    ax.set_title(target)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.ticklabel_format(useOffset=False, style='plain')

    if isinstance(bound, list):
        for i in bound:
            ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')

    elif(isinstance(bound, int) or isinstance(bound, float)):
        ax.axhline(y=bound, color='red', linestyle='--', label='Horizontal Line')

    return fig

def plot_pareto(df, objectives):
  fig, ax = plt.subplots()
  ax.scatter(df[objectives[0]], df[objectives[1]])
  ax.set_xlabel(objectives[0])
  ax.set_ylabel(objectives[1])
  ax.ticklabel_format(useOffset=False, style='plain')
  ax.set_title("Pareto")

  return fig

def create_plot(option, option_list, df, bounds, objectives):
  updated_df = excluded_dataframe(df, objectives)
  if option == "Pareto": return plot_pareto(df, objectives)
  elif option == "Updated_Pareto" : return plot_pareto(updated_df, objectives)
  else:
    for i in range(len(option_list)):
       if option == option_list[i] : return plot_result(df, option, bounds[option])

### Tk App ###

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
    def __init__(self, root, options, option_list, df, bounds, objectives):
        self.root = root
        self.options = options
        self.selected_option = None
        self.create_widgets()
        self.option_list = option_list
        self.df = df
        self.bounds = bounds
        self.objectives = objectives

    def create_widgets(self):
        self.option_var = tk.StringVar(value=self.options)
        self.option_listbox = tk.Listbox(self.root, listvariable=self.option_var, selectmode=tk.SINGLE)
        self.option_listbox.pack(padx=10, pady=5)

        self.plot_button = tk.Button(self.root, text="Plot", command=self.plot_selected_option)
        self.plot_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

        # Create a context menu for the option listbox
        self.option_menu = tk.Menu(self.root, tearoff=False)
        self.option_menu.add_command(label="Additional Info", command=self.show_additional_info)
        self.option_listbox.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            if selected_option in self.bounds:
                bound_info = self.bounds[selected_option]
                # Update the label of the "Additional Info" menu item
                self.option_menu.entryconfigure(0, label=f"{selected_option} : {bound_info}")
                self.option_menu.tk_popup(event.x_root, event.y_root)
            else:
                # Update the label of the "Additional Info" menu item
                self.option_menu.entryconfigure(0, label=f"Info : {selected_option}")
                self.option_menu.tk_popup(event.x_root, event.y_root)  

    def show_additional_info(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            # Update the label of the "Additional Info" menu item
            self.option_menu.entryconfigure(0, label=f"Info {selected_option}")
            # Implement your logic here to display additional information
            print(f"Additional info for {selected_option}")

    def plot_selected_option(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            fig = create_plot(selected_option, self.option_list, self.df, self.bounds, self.objectives)
            window = ImageWindow(self.root, fig, selected_option)

    def exit_program(self):
        sys.exit()

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

### Exclude Dominated Point ###

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

def excluded_dataframe(df, objectives):
    pareto_pts = df[objectives].values.tolist()
    new_pareto_pts = exclude_dominated_points(pareto_pts)
    updated_df = pd.DataFrame(new_pareto_pts, columns = objectives)
    return updated_df

### Functions to plot results ###

def plot_result(df, target, bound=[]):

    fig, ax = plt.subplots()
    ax.scatter(df['IterationNumber'], df[target])

    ax.grid()
    ax.set_xlabel("IterationNumber")
    ax.set_ylabel(target)
    ax.set_title(target)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.ticklabel_format(useOffset=False, style='plain')

    if isinstance(bound, list):
        for i in bound:
            ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')

    elif(isinstance(bound, int) or isinstance(bound, float)):
        ax.axhline(y=bound, color='red', linestyle='--', label='Horizontal Line')

    return fig

def plot_pareto(df, objectives):
  fig, ax = plt.subplots()
  ax.scatter(df[objectives[0]], df[objectives[1]])
  ax.set_xlabel(objectives[0])
  ax.set_ylabel(objectives[1])
  ax.ticklabel_format(useOffset=False, style='plain')
  ax.set_title("Pareto")

  return fig

def create_plot(option, option_list, df, bounds, objectives):
  updated_df = excluded_dataframe(df, objectives)
  if option == "Pareto": return plot_pareto(df, objectives)
  elif option == "Updated_Pareto" : return plot_pareto(updated_df, objectives)
  else:
    for i in range(len(option_list)):
       if option == option_list[i] : return plot_result(df, option, bounds[option])

### Tk App ###

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
    def __init__(self, root, options, option_list, df, bounds, objectives):
        self.root = root
        self.options = options
        self.selected_option = None
        self.create_widgets()
        self.option_list = option_list
        self.df = df
        self.bounds = bounds
        self.objectives = objectives

    def create_widgets(self):
        self.option_var = tk.StringVar(value=self.options)
        self.option_listbox = tk.Listbox(self.root, listvariable=self.option_var, selectmode=tk.SINGLE)
        self.option_listbox.pack(padx=10, pady=5)

        self.plot_button = tk.Button(self.root, text="Plot", command=self.plot_selected_option)
        self.plot_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

        # Create a context menu for the option listbox
        self.option_menu = tk.Menu(self.root, tearoff=False)
        self.option_menu.add_command(label="Additional Info", command=self.show_additional_info)
        self.option_listbox.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            if selected_option in self.bounds:
                bound_info = self.bounds[selected_option]
                # Update the label of the "Additional Info" menu item
                self.option_menu.entryconfigure(0, label=f"{selected_option} : {bound_info}")
                self.option_menu.tk_popup(event.x_root, event.y_root)
            else:
                # Update the label of the "Additional Info" menu item
                self.option_menu.entryconfigure(0, label=f"Info : {selected_option}")
                self.option_menu.tk_popup(event.x_root, event.y_root)  

    def show_additional_info(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            # Update the label of the "Additional Info" menu item
            self.option_menu.entryconfigure(0, label=f"Info {selected_option}")
            # Implement your logic here to display additional information
            print(f"Additional info for {selected_option}")

    def plot_selected_option(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            selected_option = self.options[index]
            fig = create_plot(selected_option, self.option_list, self.df, self.bounds, self.objectives)
            window = ImageWindow(self.root, fig, selected_option)

    def exit_program(self):
        sys.exit()

