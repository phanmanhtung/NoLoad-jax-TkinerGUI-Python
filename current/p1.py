import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sys

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

def create_plot(option, options, df, bounds):
    for i in range(len(options)):
       if option == options[i] : return plot_result(df, option, bounds[option])

### Tk App ###


class App:
    def __init__(self, root, options, df, bounds):
        self.root = root
        self.options = options
        self.selected_options = []  # Keep track of selected options
        self.df = df
        self.bounds = bounds

        self.create_widgets()

    def create_widgets(self):

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self.root, columns=("Option", "Bound", "Specification", "Type"), show="headings")
        self.treeview.pack(padx=10, pady=5)

        # Add column headings
        self.treeview.heading("Option", text="Option")
        self.treeview.heading("Bound", text="Bound")
        self.treeview.heading("Specification", text="Specification")
        self.treeview.heading("Type", text="Type")

        # Define color tags based on type
        type_colors = {
            "eq_cstr": "green",
            "ineq_cstr": "red",
        }

        # Add options and additional information
        for option in self.options:
            type_ = self.bounds.Type[option]
            self.treeview.insert("", "end", values=(option, self.bounds.Value[option], "specification", type_), tags=(type_,))
            self.treeview.tag_configure(type_, foreground=type_colors.get(type_, "black"))

        # Create a scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Create a context menu for the Treeview
        self.option_menu = tk.Menu(self.root, tearoff=False)
        self.option_menu.add_command(label="Additional Info", command=self.show_additional_info)
        self.option_menu.entryconfigure(0, state="disabled")  # Disable the "Additional Info" menu item initially
        self.treeview.bind("<Button-3>", self.show_context_menu)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

    def show_context_menu(self, event):
        selection = self.treeview.selection()
        if selection:
            self.selected_options = [self.options[self.treeview.index(item)] for item in selection]  # Update selected options
            menu_label = f"Additional Info ({len(self.selected_options)} options selected)"
            self.option_menu.entryconfigure(0, label=menu_label)
            self.option_menu.entryconfigure(0, state="normal")  # Enable the "Additional Info" menu item
            if len(self.selected_options) > 1:
                self.option_menu.entryconfigure(1, label="Plot", command=self.plot_multiple_selected_options)
            else:
                self.option_menu.entryconfigure(1, label="Plot", command=self.plot_one_selected_option)
            self.option_menu.tk_popup(event.x_root, event.y_root)

    def show_additional_info(self):
        for selected_option in self.selected_options:
            print(f"Additional info for {selected_option}")


    def plot_multiple_selected_options(self):
        fig, ax = plt.subplots()
        for selected_option in self.selected_options:
            ax.plot(self.df['IterationNumber'], self.df[selected_option])
            ax.scatter(self.df['IterationNumber'], self.df[selected_option], label=f'{selected_option}')

            if len(self.selected_options) <= 3:
            # Label each dot
                for iteration, x, y in zip(self.df['IterationNumber'], self.df['IterationNumber'], self.df[selected_option]):
                    ax.annotate(iteration, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', va='bottom')

            ax.legend()
        ax.set_xlabel('Iteration Number')
        ax.set_ylabel('Option Values')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.ticklabel_format(useOffset=False, style='plain')
        
        plt.show()

    def plot_one_selected_option(self):
        
        selected_option = self.selected_options[0]

        fig, ax = plt.subplots()
        ax.plot(self.df['IterationNumber'], self.df[selected_option])
        ax.scatter(self.df['IterationNumber'], self.df[selected_option])

        # Label each dot
        for iteration, x, y in zip(self.df['IterationNumber'], self.df['IterationNumber'], self.df[selected_option]):
            ax.annotate(iteration, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', va='bottom')


        current_bound = self.bounds.Value[selected_option]
        if isinstance(current_bound, list):
            for i in current_bound:
                ax.axhline(y=i, color='red', linestyle='--', label=self.bounds.Type[selected_option])


        elif(isinstance(current_bound, int) or isinstance(current_bound, float)):
            ax.axhline(y=current_bound, color='red', linestyle='--', label=self.bounds.Type[selected_option])
            #window = ImageWindow(self.root, fig, selected_option)

        ax.grid()
        ax.set_xlabel("IterationNumber")
        ax.set_ylabel(selected_option)
        ax.set_title(selected_option)

        # Add the legend
        handles, labels = ax.get_legend_handles_labels()
        unique_handles = list(set(handles))
        unique_labels = list(set(labels))
        ax.legend(unique_handles, unique_labels, loc='upper right')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.ticklabel_format(useOffset=False, style='plain')
        
        plt.show()

    def exit_program(self):
        sys.exit()
