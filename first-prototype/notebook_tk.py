<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
from p1 import App as App1
from p2 import App as App2

import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import ttk

def preprocess_xml(xml_file_path, all_bounds):
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
  unbounds = option_list - all_bounds.keys()

  for i in unbounds:
    all_bounds[i] = "free"
  
  # P2 data
  all_options = {}

  for i in range(len(option_list)):
    # Append a key/value pair
    all_options[option_list[i]] = df[option_list[i]].values.tolist()

  return df, option_list, all_options

def combine_dictionaries(*args):
    combined_dict = {}
    for dictionary in args:
        combined_dict.update(dictionary)
    return combined_dict

# Path to your XML file

xml_file_path = "data/example20.result"
bounds = {'p': [1.0, 20.0], 'f': [1.0, 1000.0], 'Ns': [1000.0, 1150.0],
          'Isa': [0.1, 100.0], 'j': [1.0, 10.0], 'g': [0.001, 1.0],
          'Ld': [0.001, 0.2], 'He': [0.001, 0.5], 'Lc': [0.001, 0.5],
          'Hc': [0.001, 0.5], 'Ps': [0.005, 1.0], 'ent': [0.002, 0.003],
          'd': [0.01, 0.1], 'Tinduit': [700.0, 720.0], 'Tbob': [100.0, 120.0]}
objectives={'Volume':[0.0,1.], 'PertesTotales':[0.0,900.0]}

eq_cstr={'Debit': 60.0, 'Pression': 27.0} # equality constraints
ineq_cstr={'Vsa': [200., 325.0], 'ctrle': [0.0, 5.0],'ctrld': [0.0, 5.0], 'BsDent':  [0.1, 1.7], 
           'BsCulasse':[0.1, 1.7],'BsDentExterne': [0.1, 1.7]}

all_bounds = combine_dictionaries(bounds, objectives, eq_cstr, ineq_cstr)
df, option_list, all_options = preprocess_xml(xml_file_path, all_bounds)
objectives = list(objectives.keys())
'''

xml_file_path = "data/Biobj.result"
obj_dict={'f1':[0.,2.],'f2':[0.,2.]}
bound_dict={'z1':[-5, 5], 'z2':[-5, 5]}
objectives = list(obj_dict.keys())
all_bounds = combine_dictionaries(obj_dict, objectives, bound_dict)
df, option_list, all_options = preprocess_xml(xml_file_path, all_bounds)
'''

root = tk.Tk()
root.title("Notebook")

# Create a tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create the first tab and add the App and ImageWindow instances from program1
tab1 = ttk.Frame(notebook)
all_options1 = ["Updated_Pareto", "Pareto"] + option_list # Define your all_options list here
app1 = App1(tab1, all_options1, option_list, df, all_bounds, objectives)
#image_window1 = ImageWindow1(tab1)
notebook.add(tab1, text="Program 1")

# Create the second tab and add the App and ImageWindow instances from program2
tab2 = ttk.Frame(notebook)
app2 = App2(tab2, all_options)
app2.update_options(option_list, option_list)
#image_window2 = ImageWindow2(tab2)
notebook.add(tab2, text="Program 2")

root.mainloop()
=======
import tkinter as tk
from tkinter import ttk
from p1 import App as App1
from p2 import App as App2

import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import ttk

def preprocess_xml(xml_file_path, all_bounds):
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
  unbounds = option_list - all_bounds.keys()

  for i in unbounds:
    all_bounds[i] = "free"
  
  # P2 data
  all_options = {}

  for i in range(len(option_list)):
    # Append a key/value pair
    all_options[option_list[i]] = df[option_list[i]].values.tolist()

  return df, option_list, all_options

def combine_dictionaries(*args):
    combined_dict = {}
    for dictionary in args:
        combined_dict.update(dictionary)
    return combined_dict

# Path to your XML file

xml_file_path = "example20.result"
bounds = {'p': [1.0, 20.0], 'f': [1.0, 1000.0], 'Ns': [1000.0, 1150.0],
          'Isa': [0.1, 100.0], 'j': [1.0, 10.0], 'g': [0.001, 1.0],
          'Ld': [0.001, 0.2], 'He': [0.001, 0.5], 'Lc': [0.001, 0.5],
          'Hc': [0.001, 0.5], 'Ps': [0.005, 1.0], 'ent': [0.002, 0.003],
          'd': [0.01, 0.1], 'Tinduit': [700.0, 720.0], 'Tbob': [100.0, 120.0]}
objectives={'Volume':[0.0,1.], 'PertesTotales':[0.0,900.0]}

eq_cstr={'Debit': 60.0, 'Pression': 27.0} # equality constraints
ineq_cstr={'Vsa': [200., 325.0], 'ctrle': [0.0, 5.0],'ctrld': [0.0, 5.0], 'BsDent':  [0.1, 1.7], 
           'BsCulasse':[0.1, 1.7],'BsDentExterne': [0.1, 1.7]}

all_bounds = combine_dictionaries(bounds, objectives, eq_cstr, ineq_cstr)
df, option_list, all_options = preprocess_xml(xml_file_path, all_bounds)
objectives = list(objectives.keys())
'''

xml_file_path = "Biobj.result"
obj_dict={'f1':[0.,2.],'f2':[0.,2.]}
bound_dict={'z1':[-5, 5], 'z2':[-5, 5]}
objectives = list(obj_dict.keys())
all_bounds = combine_dictionaries(obj_dict, objectives, bound_dict)
df, option_list, all_options = preprocess_xml(xml_file_path, all_bounds)
'''

root = tk.Tk()
root.title("Notebook")

# Create a tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create the first tab and add the App and ImageWindow instances from program1
tab1 = ttk.Frame(notebook)
all_options1 = ["Updated_Pareto", "Pareto"] + option_list # Define your all_options list here
app1 = App1(tab1, all_options1, option_list, df, all_bounds, objectives)
#image_window1 = ImageWindow1(tab1)
notebook.add(tab1, text="Program 1")

# Create the second tab and add the App and ImageWindow instances from program2
tab2 = ttk.Frame(notebook)
app2 = App2(tab2, all_options)
app2.update_options(option_list, option_list)
#image_window2 = ImageWindow2(tab2)
notebook.add(tab2, text="Program 2")

root.mainloop()
>>>>>>> main
