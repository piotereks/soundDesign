import tkinter as tk

class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

def main():
    root = tk.Tk()
    root.geometry('200x200')
    win = WrappingLabel(root, text="As in, you have a line of text in a Tkinter window, a Label. As the user drags the window narrower, the text remains unchanged until the window width means that the text gets cut off, at which point the text should wrap.")
    win.pack(expand=True, fill=tk.X)
    root.mainloop()

if __name__ == '__main__':
    main()