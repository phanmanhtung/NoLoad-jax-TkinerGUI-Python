import tkinter as tk

class OptionSelector:
    def __init__(self, master):
        self.master = master
        master.title("Option Selector")
        
        # Define options for the columns
        self.options1 = ["Option 1a", "Option 1b", "Option 1c"]
        self.options2 = ["Option 2a", "Option 2b", "Option 2c"]
        
        # Create column labels
        tk.Label(master, text="Column 1").grid(row=0, column=0)
        tk.Label(master, text="Column 2").grid(row=0, column=1)
        
        # Create option lists
        self.listbox1 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=False)
        self.listbox2 = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=False)
        
        # Populate option lists
        for option in self.options1:
            self.listbox1.insert(tk.END, option)
        for option in self.options2:
            self.listbox2.insert(tk.END, option)
        
        # Position option lists
        self.listbox1.grid(row=1, column=0)
        self.listbox2.grid(row=1, column=1)
        
        # Bind selection events to listboxes
        self.listbox1.bind("<<ListboxSelect>>", self.on_select)
        self.listbox2.bind("<<ListboxSelect>>", self.on_select)
        
        # Create button
        self.show_button = tk.Button(master, text="Show", command=self.show_selection)
        self.show_button.grid(row=2, column=0, columnspan=2)
        
    def on_select(self, event):
        # Get the widget that triggered the event
        selected_widget = event.widget
        
        # Get the selected index in the widget
        selected_index = selected_widget.curselection()
        
        # Deselect other options in the widget
        for i in range(selected_widget.size()):
            if i != selected_index:
                selected_widget.itemconfig(i, bg='white')
                
        # Highlight the selected option
        if selected_index:
            selected_widget.itemconfig(selected_index, bg='lightblue')
        
        # Get the other widget
        other_widget = self.listbox2 if selected_widget == self.listbox1 else self.listbox1
        
        # Deselect other options in the other widget
        other_widget.selection_clear(0, tk.END)
        
        # Deselect other options in the other widget
        for i in range(other_widget.size()):
            other_widget.itemconfig(i, bg='white')
        
    def show_selection(self):
        # Get selected options
        selected1 = self.listbox1.get(self.listbox1.curselection())
        selected2 = self.listbox2.get(self.listbox2.curselection())
        
        if selected1 and selected2:
            # Print selected options
            print("Selected options:")
            print(selected1)
            print(selected2)
        else:
            # Display error message if one or both options are not selected
            tk.messagebox.showerror(title="Error", message="Please select one option from each column.")
        
root = tk.Tk()
app = OptionSelector(root)
root.mainloop()
