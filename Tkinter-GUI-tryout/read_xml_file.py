# Path to your XML file
xml_file_path = "rosenbrock.result"


import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import pandas as pd

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

bounds={'x':[-2., 2.],'y':[-2, 2]}
ineq_cstr={'ctr1':[None, 0],'ctr2':[None, 0]}	

def plot_result(df, target, bound):
  fig, ax = plt.subplots()
  ax.scatter(df['IterationNumber'], df[target])
  ax.grid()

  for i in bound:
     ax.axhline(y=i, color='red', linestyle='--', label='Horizontal Line')
  return fig

fig = plot_result(df, 'x', bounds['x'])
plt.show()

