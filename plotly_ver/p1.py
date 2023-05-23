import tkinter as tk
from tkinter import ttk
import sys
import plotly.graph_objects as go
import plotly.express as px

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

        fig = go.Figure()
        fig_title = "1d-plot: "

        for selected_option in self.selected_options:
            fig_title += (str(selected_option) + " ")
            fig.add_trace(go.Scatter(x=self.df['IterationNumber'], 
                                     y=self.df[selected_option], 
                                     mode='lines+markers', 
                                     name=selected_option,
                                     hovertemplate=f"{'IterationNumber'}=%{{x}}<br>{selected_option}=%{{y:.2f}}<extra></extra>"))

            if len(self.selected_options) <= 3:
                # Label each dot
                for iteration, x, y in zip(self.df['IterationNumber'], self.df['IterationNumber'], self.df[selected_option]):
                    fig.add_annotation(x=x, y=y, text=str(iteration), showarrow=True, arrowhead=1, ax=0, ay=-20)

        fig.update_layout(
            title={
            'text': fig_title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            xaxis_title='Iteration Number',
            yaxis_title='Option Values',
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickformat='g'),
            legend=dict(x=1, y=1)
        )

        config = {
            'modeBarButtonsToAdd': [
                'downloadImage'
            ]
        }
        fig.show(config=config)

    def plot_one_selected_option(self):
        selected_option = self.selected_options[0]

        color = 'blue'  # Set the desired color value

        fig = px.line(
            self.df,
            x='IterationNumber',
            y=selected_option,
            title="1d-plot: " + str(selected_option),
            labels={'IterationNumber': 'Iteration Number', selected_option: selected_option},
            hover_data={'IterationNumber': True, selected_option: ':.2f'},
            color_discrete_sequence=[color]
        )

        fig.add_trace(
            go.Scatter(
                x=self.df['IterationNumber'],
                y=self.df[selected_option],
                mode='markers',
                name=selected_option,
                hovertemplate=f"{'IterationNumber'}=%{{x}}<br>{selected_option}=%{{y:.2f}}<extra></extra>",
                marker=dict(color=color)
            )
        )

        # Label each dot
        for iteration, x, y in zip(self.df['IterationNumber'], self.df['IterationNumber'], self.df[selected_option]):
            fig.add_annotation(x=x, y=y, text=str(iteration), showarrow=True, arrowhead=1, ax=0, ay=-20)

        current_bound = self.bounds.Value[selected_option]

        if isinstance(current_bound, list):
            for i in current_bound:
                fig.add_shape(
                    type="line",
                    x0=self.df['IterationNumber'].min(),
                    y0=i,
                    x1=self.df['IterationNumber'].max(),
                    y1=i,
                    line=dict(color='red', dash='dash'),
                    name=self.bounds.Type[selected_option]
                )

        elif isinstance(current_bound, (int, float)):
            fig.add_shape(
                type="line",
                x0=self.df['IterationNumber'].min(),
                y0=current_bound,
                x1=self.df['IterationNumber'].max(),
                y1=current_bound,
                line=dict(color='red', dash='dash'),
                name=self.bounds.Type[selected_option]
            )

        fig.update_layout(
            title={
            'text': "1d-plot: " + str(selected_option),
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            xaxis_title='Iteration Number',
            yaxis_title=selected_option,
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickformat='g'),
            legend=dict(x=1, y=1)
        )
        
        config = {
            'modeBarButtonsToAdd': [
                'downloadImage'
            ]
        }
        fig.show(config=config)

    def exit_program(self):
        sys.exit()
