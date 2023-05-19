import tkinter as tk
from tkinter import ttk

class Notebook(ttk.Notebook):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.enable_bindings()
        
    def enable_bindings(self):
        self.bind("<ButtonPress-1>", self.on_tab_click, True)
        self.bind("<ButtonRelease-1>", self.on_tab_release)
        self.bind("<B1-Motion>", self.on_tab_motion, True)
    
    def on_tab_click(self, event):
        element = event.widget.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))
        self._dragged_tab = index
        self._dragged_over = None
    
    def on_tab_release(self, event):
        if self._dragged_tab is not None and self._dragged_over is not None:
            current_tab = self._dragged_tab
            new_tab = self._dragged_over
            tabs = list(self.tabs())
            tabs[current_tab], tabs[new_tab] = tabs[new_tab], tabs[current_tab]
            self._nametowidget('!frame%s' % current_tab).grid_forget()
            self._nametowidget('!frame%s' % new_tab).grid_forget()
            for i, tab in enumerate(tabs):
                self.tab(tab, text="Tab %d" % i)
                self._nametowidget('!frame%s' % i).grid(row=0, column=0)
            self.select(new_tab)
        self._dragged_tab = None
        self._dragged_over = None
    
    def on_tab_motion(self, event):
        element = event.widget.identify(event.x, event.y)
        if element == "label":
            index = self.index("@%d,%d" % (event.x, event.y))
            if index != self._dragged_tab and index is not None:
                self._dragged_over = index
                self.lift(self._dragged_tab)
                self.move(self._dragged_tab, self.bbox(self._dragged_over))
                self.lift(self._dragged_tab)
    
root = tk.Tk()
root.geometry("400x300")

notebook = Notebook(root)

for i in range(5):
    frame = ttk.Frame(notebook, name='frame%s' % i)
    frame.grid(row=0, column=0)
    label = ttk.Label(frame, text="This is Tab %d" % i)
    label.pack()
    notebook.add(frame, text="Tab %d" % i)

notebook.pack(fill=tk.BOTH, expand=True)

root.mainloop()