import tkinter as tk
import sys
import plotly.express as px
import plotly.graph_objects as go

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
    df['pareto_pts'] = df[objectives].values.tolist()
    new_pareto_pts = exclude_dominated_points(df['pareto_pts'].values)
    updated_df = df.loc[df['pareto_pts'].isin(new_pareto_pts)]
    
    return updated_df

def plot_2d(df, label, objectives):

    fig = px.scatter(
        df,
        x=objectives[0],
        y=objectives[1],
        hover_data={'IterationNumber': True},
    )

    fig.update_traces(mode='lines+markers')

    # Add annotations
    annotations = [
        dict(
            x=x,
            y=y,
            text=str(iteration),
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-20
        )
        for iteration, x, y in zip(df['IterationNumber'], df[objectives[0]], df[objectives[1]])
    ]
    fig.update_layout(annotations=annotations)

    fig.update_layout(
        title={'text':label,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
        )

    config = {
        'modeBarButtonsToAdd': [
            'downloadImage'
        ]
    }
    fig.show(config=config)


### Tk App ###

class App:
    def __init__(self, root, options, df, objectives):
        self.root = root
        self.options = options
        self.selected_option = []
        self.create_widgets()
        self.df = df
        self.objectives = objectives
        self.updated_df = excluded_dataframe(self.df, self.objectives)

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

    def plot_one_selected_option(self):

        if self.selected_options[0] == "Pareto":

            plot_2d(self.df, self.selected_options[0], self.objectives)

        else:

            plot_2d(self.updated_df, self.selected_options[0], self.objectives)


    def plot_multiple_selected_options(self):

        color = 'blue'  # Set the desired color value

        fig = px.scatter(
            self.df,
            x=self.objectives[0],
            y=self.objectives[1],
            hover_data={'IterationNumber': True},

            color_discrete_sequence=[color]
            )

        fig.add_trace(
            go.Scatter(
                x=self.updated_df[self.objectives[0]],
                y=self.updated_df[self.objectives[1]],
                mode='lines',
                hovertemplate=f"<br>{self.objectives[0]}=%{{x}}<br>{self.objectives[1]}=%{{y:.2f}}<extra></extra>",
                marker=dict(color=color)
            )
        )

        # Add annotations
        annotations = [
            dict(
                x=x,
                y=y,
                text=str(iteration),
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-20
            )
            for iteration, x, y in zip(self.updated_df['IterationNumber'], 
                                       self.updated_df[self.objectives[0]], 
                                       self.updated_df[self.objectives[1]])
        ]
        fig.update_layout(annotations=annotations)

        fig.update_layout(
            title={
            'text': "Pareto",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            }
        )

        config = {
            'modeBarButtonsToAdd': [
                'downloadImage'
            ]
        }
        fig.show(config=config)


    def exit_program(self):
        sys.exit()