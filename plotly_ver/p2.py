import tkinter as tk
from tkinter import ttk
import sys
import plotly.express as px

class App:
    def __init__(self, root, df):
        self.root = root
        self.x_options = []  # Empty list for X options initially
        self.y_options = []  # Empty list for Y options initially
        self.selected_x = tk.StringVar()
        self.selected_y = tk.StringVar()
        self.create_widgets()
        self.df = df

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

        self.plot_button = ttk.Button(self.option_frame, text="Plot according Iteration", command=self.plot_iter)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.plot_button = ttk.Button(self.option_frame, text="Plot according Sorted X", command=self.plot_sorted_X)
        self.plot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.exit_button = ttk.Button(self.option_frame, text="Exit", command=sys.exit)
        self.exit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    def update_options(self, x_options, y_options):
        self.x_options = x_options
        self.y_options = y_options
        self.x_combobox['values'] = self.x_options
        self.y_combobox['values'] = self.y_options

    def plot_iter(self):

        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        fig = px.scatter(
            self.df,
            x=selected_x,
            y=selected_y,
            hover_data={'IterationNumber': True},
            title=f"{selected_x} vs {selected_y}",
            labels={selected_x: selected_x, selected_y: selected_y},
        )

        fig.update_traces(mode='lines+markers')

        # Add annotations
        for iteration, x, y in zip(self.df['IterationNumber'], self.df[selected_x], self.df[selected_y]):
            fig.add_annotation(x=x, y=y, text=str(iteration), showarrow=True, arrowhead=1, ax=0, ay=-20)

        fig.update_layout(
            title={'text':f"{selected_x} vs {selected_y}",
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            xaxis_title=selected_x,
            yaxis_title=selected_y,
            hovermode='closest',
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickformat='g'),
        )

        config = {
            'modeBarButtonsToAdd': [
                'downloadImage'
            ]
        }
        
        fig.show(config=config)


    def plot_sorted_X(self):

        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        sorted_X_df = self.df.sort_values(by=[selected_x])

        fig = px.scatter(
            sorted_X_df,
            x=selected_x,
            y=selected_y,
            hover_data={'IterationNumber': True},
            title=f"{selected_x} vs {selected_y}",
            labels={selected_x: selected_x, selected_y: selected_y},
        )

        fig.update_traces(mode='lines+markers')

        # Add annotations
        for iteration, x, y in zip(sorted_X_df['IterationNumber'], sorted_X_df[selected_x], sorted_X_df[selected_y]):
            fig.add_annotation(x=x, y=y, text=str(iteration), showarrow=True, arrowhead=1, ax=0, ay=-20)

        fig.update_layout(
            title={'text':f"{selected_x} vs {selected_y}",
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            xaxis_title=selected_x,
            yaxis_title=selected_y,
            hovermode='closest',
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickformat='g'),
        )

        config = {
            'modeBarButtonsToAdd': [
                'downloadImage'
            ]
        }
        
        fig.show(config=config)