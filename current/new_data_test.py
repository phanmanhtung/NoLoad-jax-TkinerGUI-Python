import tkinter as tk
from tkinter import ttk
from p1 import App as App1
from p2 import App as App2
from p3 import App as App3
import xml.etree.ElementTree as ET
import pandas as pd
from ast import literal_eval

def preprocess_xml(xml_file_path):
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

  # Extract specifications from XML
  objective_functions = root.find("SPECIFICATIONS/ObjectiveFunctions")
  equality_constraints = root.find("SPECIFICATIONS/EqualityConstraints")
  inequality_constraints = root.find("SPECIFICATIONS/InequalityConstraints")
  free_outputs = root.find("SPECIFICATIONS/FreeOutputs")

  all_dfs_array = []

  # Extract objective function data
  objective_functions_data = []
  for obj_func in objective_functions.iter("Objective"):
      objective_name = obj_func.get("Name")
      objective_value = obj_func.get("Value")
      objective_functions_data.append({"ObjectiveName": objective_name, "ObjectiveValue": literal_eval(objective_value)})

  # Convert objective function data to DataFrame
  df_objective_functions = pd.DataFrame(objective_functions_data)
  df_objective_functions["Type"] = "objective"
  df_objective_functions.columns = ["Name", "Value", "Type"]

  objectives = df_objective_functions["Name"].values

  all_dfs_array.append(df_objective_functions)

  # Extract equality constraint data
  if equality_constraints is not None:
    equality_constraints_data = []
    for eq_constraint in equality_constraints.iter("EqualityConstraint"):
        constraint_name = eq_constraint.get("Name")
        constraint_value = eq_constraint.get("Value")
        equality_constraints_data.append({"ConstraintName": constraint_name, "ConstraintValue": literal_eval(constraint_value)})

    # Convert equality constraint data to DataFrame
    df_equality_constraints = pd.DataFrame(equality_constraints_data)

    df_equality_constraints["Type"] = "eq_cstr"
    df_equality_constraints.columns = ["Name", "Value", "Type"]

    all_dfs_array.append(df_equality_constraints)

  # Extract inequality constraint data
  if inequality_constraints is not None:
    inequality_constraints_data = []
    for ineq_constraint in inequality_constraints.iter("InequalityConstraint"):
        constraint_name = ineq_constraint.get("Name")
        constraint_value = ineq_constraint.get("Value")
        inequality_constraints_data.append({"ConstraintName": constraint_name, "ConstraintValue": literal_eval(constraint_value)})

    # Convert inequality constraint data to DataFrame
    df_inequality_constraints = pd.DataFrame(inequality_constraints_data)

    df_inequality_constraints["Type"] = "ineq_cstr"
    df_inequality_constraints.columns = ["Name", "Value", "Type"]

    all_dfs_array.append(df_inequality_constraints)

  # Extract free output data
  if free_outputs is not None:
    free_outputs_data = []
    for free_output in free_outputs.iter("FreeOutput"):
        output_name = free_output.get("Name")
        free_outputs_data.append({"OutputName": output_name})

    # Convert free output data to DataFrame
    df_free_outputs = pd.DataFrame(free_outputs_data)
  
    df_free_outputs["Type"] = "free"
    df_free_outputs.columns = ["Name", "Type"]

    # Filter out the objectives
    df_free_outputs = df_free_outputs[~df_free_outputs["Name"].isin(objectives)]

    all_dfs_array.append(df_free_outputs)

  specifications_df = pd.DataFrame(columns=["Name", "Value", "Type"])
  for i in all_dfs_array:
    specifications_df = pd.concat([specifications_df, i], axis=0)

  specifications_df = specifications_df.set_index('Name')

  return df, option_list, specifications_df, objectives

# Path to your XML file

xml_file_path = "data/example20_new.result"
df, option_list, specifications_df, objectives = preprocess_xml(xml_file_path)
bounds = {'p': [1.0, 20.0], 'f': [1.0, 1000.0], 'Ns': [1000.0, 1150.0],
          'Isa': [0.1, 100.0], 'j': [1.0, 10.0], 'g': [0.001, 1.0],
          'Ld': [0.001, 0.2], 'He': [0.001, 0.5], 'Lc': [0.001, 0.5],
          'Hc': [0.001, 0.5], 'Ps': [0.005, 1.0], 'ent': [0.002, 0.003],
          'd': [0.01, 0.1], 'Tinduit': [700.0, 720.0], 'Tbob': [100.0, 120.0]}

df_bounds = pd.DataFrame({'Value': bounds.values(), "Type": "bound"}, index=bounds.keys())
specifications_df = pd.concat([specifications_df, df_bounds], axis=0)

#unbounds = [x for x in option_list if x not in specifications_df.index]
#print(unbounds)
#specifications_df = specifications_df.reindex(specifications_df.index.union(unbounds))

### Tk App ###

root = tk.Tk()
root.title("Notebook")

# Create a tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create the first tab and add the App and ImageWindow instances from program1
tab1 = ttk.Frame(notebook)
app1 = App1(tab1, option_list, df, specifications_df)
notebook.add(tab1, text="1-var-iteration")

# Create the second tab and add the App and ImageWindow instances from program2
tab2 = ttk.Frame(notebook)
app2 = App2(tab2, df)
app2.update_options(option_list, option_list)
notebook.add(tab2, text="2-var-plot")

# Create the first tab and add the App and ImageWindow instances from program1
tab3 = ttk.Frame(notebook)
all_options3 = ["Updated_Pareto", "Pareto"]
app3 = App3(tab3, ["Updated_Pareto", "Pareto"], df, objectives)
notebook.add(tab3, text="Pareto")

root.mainloop()
