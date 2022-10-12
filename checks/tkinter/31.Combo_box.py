from tkinter import messagebox, ttk
import tkinter as tk

# https://pythonassets.com/posts/drop-down-list-combobox-in-tk-tkinter/
def selection_changed(event):
    selection = combo.get()
    messagebox.showinfo(
        title="New Selection",
        message=f"Selected option: {selection}"
    )

def dropdown_opened():
    print("The drop-down has been opened!")
    print(combo.get())

main_window = tk.Tk()
main_window.config(width=300, height=200)
main_window.title("Combobox")
combo = ttk.Combobox(
    # state="readonly",
    values=["Python", "C", "C++", "Java"],
    postcommand = dropdown_opened
)
combo.bind("<<ComboboxSelected>>", selection_changed)
combo.place(x=50, y=50)
combo.set('gurusuruz')
print(combo.get())
# button = ttk.Button(text="Display selection", command=display_selection)
# button.place(x=50, y=100)
main_window.mainloop()