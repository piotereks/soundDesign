import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        <create the rest of your GUI here>

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
"""
If your app has additional toplevel windows, I recommend making 
each of those a separate class, inheriting from tk.Toplevel. 
This gives you all of the same advantages mentioned above -- the windows are atomic,
they have their own namespace, and the code is well organized. 
Plus, it makes it easy to put each into its own module once the code starts to get large.

Finally, you might want to consider using classes for every major portion of your interface.
For example, if you're creating an app with a toolbar, a navigation pane, 
a statusbar, and a main area, you could make each one of those classes. 
This makes your main code quite small and easy to understand:
"""
class Navbar(tk.Frame): ...
class Toolbar(tk.Frame): ...
class Statusbar(tk.Frame): ...
class Main(tk.Frame): ...

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.statusbar = Statusbar(self, ...)
        self.toolbar = Toolbar(self, ...)
        self.navbar = Navbar(self, ...)
        self.main = Main(self, ...)

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)
"""
Since all of those instances share a common parent, the parent effectively 
becomes the "controller" part of a model-view-controller architecture. 
So, for example, the main window could place something on the statusbar by 
calling self.parent.statusbar.set("Hello, world"). This allows you to define 
a simple interface between the components, helping to keep coupling to a minimun.
"""