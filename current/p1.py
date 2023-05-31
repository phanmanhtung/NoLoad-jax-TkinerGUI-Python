import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sys
import math

### Tk App ###

class App:
    def __init__(self, root, options, df, specifications):
        self.root = root
        self.options = options
        self.selected_options = []  # Keep track of selected options
        self.df = df
        self.specifications = specifications

        self.create_widgets()

    def change_color(self, color):
        selected_items = self.treeview.selection()
        for item in selected_items:
            self.treeview.tag_configure(color, foreground=color, background="white")

    def create_widgets(self):

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self.root, columns=("Variable", "Min", "Max", "Value", "Type", "Input/Output"), show="headings")
        self.treeview.pack(padx=10, pady=5)

        # Add column headings
        self.treeview.heading("Variable", text="Variable")
        self.treeview.heading("Min", text="Min")
        self.treeview.heading("Max", text="Max")
        self.treeview.heading("Value", text="Value")
        self.treeview.heading("Type", text="Type")
        self.treeview.heading("Input/Output", text="Input/Output")

        # Define color tags based on type and min/max columns
        type_colors = {
            "bound": "blue",
            "constrained": "blue",
            "obj": "blue",
            "fixed": "blue",
            "free": "blue",
        }
        min_color = "blue"
        max_color = "red"

        # Add options and additional information
        for option in self.options:
            type_ = self.specifications.Type[option]
            value = self.specifications.Value[option]

            if isinstance(value, list) and type_=="bounds":
                min_value, max_value = value
                value_text = ""

            elif isinstance(value, list) and type_=="ineq_cstr":
                min_value, max_value = "", ""
                value_text = str(value[0]) + "      " + str(value[1])

            elif (isinstance(value, int) or isinstance(value, float)) and not math.isnan(value):
                min_value = ""
                max_value = ""
                value_text = value
                print(value)
            else:
                min_value = ""
                max_value = ""
                value_text = ""

            #input_output = self.specifications.InputOutput[option]

            # Insert the item and apply color tags
            item = self.treeview.insert("", "end", values=(option, min_value, max_value, value_text, type_, "input_output"))

            # Apply color tags to cells in min and max columns
            self.treeview.item(item, tags=(min_value, max_value))

        # Apply color tags to min and max columns
        self.treeview.tag_configure(min_color, foreground=min_color)
        self.treeview.tag_configure(max_color, foreground=max_color)

        # Apply colors to min and max columns
        self.treeview.tag_bind(min_color, "<<TreeviewSelect>>", lambda event: self.change_color(min_color))
        self.treeview.tag_bind(max_color, "<<TreeviewSelect>>", lambda event: self.change_color(max_color))

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
        color = "midnightblue"

        fig, ax = plt.subplots()
        ax.plot(self.df['IterationNumber'], self.df[selected_option], color=color)
        ax.scatter(self.df['IterationNumber'], self.df[selected_option], color=color)

        # Label each dot
        for iteration, x, y in zip(self.df['IterationNumber'], self.df['IterationNumber'], self.df[selected_option]):
            ax.annotate(iteration, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', va='bottom')

        current_spec = self.specifications.Value[selected_option]
        current_type = self.specifications.Type[selected_option]
        
        if isinstance(current_spec, list) and current_type=="bounds":
            ax.axhline(y=current_spec[1], color='red', linestyle='--', label=current_type)
            ax.axhline(y=current_spec[0], color='blue', linestyle='--', label=current_type)

        elif isinstance(current_spec, list):
            for i in current_spec:
                ax.axhline(y=i, color='grey', linestyle='--', label=current_type)

        elif(isinstance(current_spec, int) or isinstance(current_spec, float) and not math.isnan(current_spec)):
            ax.axhline(y=current_spec, color='black', linestyle='--', label=current_type)

        ax.grid()
        ax.set_xlabel("IterationNumber")
        ax.set_ylabel(selected_option)
        ax.set_title(selected_option)

        '''
        # Add the legend
        handles, labels = ax.get_legend_handles_labels()
        unique_handles = list(set(handles))
        unique_labels = list(set(labels))
        ax.legend(unique_handles, unique_labels, loc='upper right')
        '''

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.ticklabel_format(useOffset=False, style='plain')
        
        plt.show()

    def exit_program(self):
        sys.exit()
