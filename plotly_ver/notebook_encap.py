import tkinter as tk
from tkinter import ttk
from p1 import App as App1
from p2 import App as App2
from p3 import App as App3
import xml.etree.ElementTree as ET
import pandas as pd

class MyApp:
    def __init__(self):
        self.xml_file_path = "data/example20.result"
        self.bounds = {'p': [1.0, 20.0], 'f': [1.0, 1000.0], 'Ns': [1000.0, 1150.0],
                       'Isa': [0.1, 100.0], 'j': [1.0, 10.0], 'g': [0.001, 1.0],
                       'Ld': [0.001, 0.2], 'He': [0.001, 0.5], 'Lc': [0.001, 0.5],
                       'Hc': [0.001, 0.5], 'Ps': [0.005, 1.0], 'ent': [0.002, 0.003],
                       'd': [0.01, 0.1], 'Tinduit': [700.0, 720.0], 'Tbob': [100.0, 120.0]}
        self.objectives = {'Volume': [0.0, 1.], 'PertesTotales': [0.0, 900.0]}
        self.eq_cstr = {'Debit': 60.0, 'Pression': 27.0}
        self.ineq_cstr = {'Vsa': [200., 325.0], 'ctrle': [0.0, 5.0], 'ctrld': [0.0, 5.0],
                          'BsDent': [0.1, 1.7], 'BsCulasse': [0.1, 1.7], 'BsDentExterne': [0.1, 1.7]}

    def preprocess_xml(self, xml_file_path):
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
            outputs_data = {output_elem.get("Name"): float(output_elem.get("Value")) for output_elem in
                            outputs.iter("Output")}

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
        return df, option_list

    def combine_all_bounds(self, bounds=None, objectives=None, eq_cstr=None, ineq_cstr=None, *args):
        combined_df = pd.DataFrame()

        if bounds:
            df_bounds = pd.DataFrame({'Value': bounds.values(), "Type": "bound"}, index=bounds.keys())
            combined_df = pd.concat([combined_df, df_bounds], axis=0)

        if objectives:
            df_objectives = pd.DataFrame({'Value': objectives.values(), "Type": "objective"}, index=objectives.keys())
            combined_df = pd.concat([combined_df, df_objectives], axis=0)

        if eq_cstr:
            df_eq_cstr = pd.DataFrame({'Value': eq_cstr.values(), "Type": "eq_cstr"}, index=eq_cstr.keys())
            combined_df = pd.concat([combined_df, df_eq_cstr], axis=0)

        if ineq_cstr:
            df_ineq_cstr = pd.DataFrame({'Value': ineq_cstr.values(), "Type": "ineq_cstr"}, index=ineq_cstr.keys())
            combined_df = pd.concat([combined_df, df_ineq_cstr], axis=0)

        return combined_df

    def run(self):
        df, option_list = self.preprocess_xml(self.xml_file_path)

        # all_bounds is in type DataFrame
        all_bounds = self.combine_all_bounds(bounds=self.bounds, objectives=self.objectives, eq_cstr=self.eq_cstr,
                                             ineq_cstr=self.ineq_cstr)
        #unbounds = [x for x in option_list if x not in all_bounds]
        #all_bounds = all_bounds.reindex(all_bounds.index.union(unbounds))
        objectives = list(self.objectives.keys())

        ### Tk App ###

        root = tk.Tk()
        root.title("Notebook")

        # Create a tabbed interface
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create the first tab and add the App and ImageWindow instances from program1
        tab1 = ttk.Frame(notebook)
        app1 = App1(tab1, option_list, df, all_bounds)
        notebook.add(tab1, text="1-var-iteration")

        # Create the second tab and add the App and ImageWindow instances from program2
        tab2 = ttk.Frame(notebook)
        app2 = App2(tab2, df)
        app2.update_options(option_list, option_list)
        notebook.add(tab2, text="2-var-plot")

        # Create the first tab and add the App and ImageWindow instances from program1
        tab3 = ttk.Frame(notebook)
        app3 = App3(tab3, ["Updated_Pareto", "Pareto"], df, objectives)
        notebook.add(tab3, text="Pareto")

        root.mainloop()

if __name__ == '__main__':
    my_app = MyApp()
    my_app.run()
