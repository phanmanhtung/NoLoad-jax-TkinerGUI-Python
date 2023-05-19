import tkinter as tk

class App:
    def __init__(self, root, options):
        self.root = root
        self.options = options
        self.create_widgets()

    def create_widgets(self):
        self.option_frame = tk.Frame(self.root)
        self.option_frame.pack(padx=10, pady=10)

        for option in self.options:
            # Create a label for each option
            label = tk.Label(self.option_frame, text=option)
            label.pack()

            # Create a context menu for each option
            menu = tk.Menu(label, tearoff=False)
            menu.add_command(label="Additional Info", command=lambda opt=option: self.show_additional_info(opt))
            label.bind("<Button-3>", lambda event, m=menu: m.tk_popup(event.x_root, event.y_root))

    def show_additional_info(self, option):
        # This function will be called when the "Additional Info" menu item is clicked
        # You can implement your logic here to show the additional information for the selected option
        print(f"Additional info for {option}")

# Define your options list
options = ["Option 1", "Option 2", "Option 3"]

root = tk.Tk()
app = App(root, options)
root.mainloop()
