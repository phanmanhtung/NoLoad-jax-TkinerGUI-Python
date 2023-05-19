import tkinter as tk
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

def create_plot(option, option_list, df, bounds):
    for i in range(len(option_list)):
       if option == option_list[i] : return plot_result(df, option, bounds[option])

### Tk App ###

class App:
    def __init__(self, root, options, option_list, df, bounds):
        self.root = root
        self.options = options
        self.selected_options = []  # Keep track of selected options
        self.create_widgets()
        self.option_list = option_list
        self.df = df
        self.bounds = bounds

    def create_widgets(self):
        self.option_var = tk.StringVar(value=self.options)
        self.option_listbox = tk.Listbox(self.root, listvariable=self.option_var, selectmode=tk.EXTENDED)
        self.option_listbox.pack(padx=10, pady=5)

        #self.plot_button = tk.Button(self.root, text="Plot", command=self.plot_selected_options)
        #self.plot_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

        # Create a context menu for the option listbox
        self.option_menu = tk.Menu(self.root, tearoff=False)
        self.option_menu.add_command(label="Additional Info", command=self.show_additional_info)
        self.option_listbox.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        selection = self.option_listbox.curselection()
        if selection:
            self.selected_options = [self.options[index] for index in selection]  # Update selected options
            menu_label = f"Additional Info ({len(self.selected_options)} options selected)"
            self.option_menu.entryconfigure(0, label=menu_label)
            if len(self.selected_options)>1:
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

        current_bound = self.bounds[selected_option]
        if isinstance(current_bound, list):
            for i in current_bound:
                ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')

        elif(isinstance(current_bound, int) or isinstance(current_bound, float)):
            ax.axhline(y=current_bound, color='red', linestyle='--', label='Horizontal Line')
            #window = ImageWindow(self.root, fig, selected_option)

        ax.grid()
        ax.set_xlabel("IterationNumber")
        ax.set_ylabel(selected_option)
        ax.set_title(selected_option)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.ticklabel_format(useOffset=False, style='plain')
        
        plt.show()

    def exit_program(self):
        sys.exit()
