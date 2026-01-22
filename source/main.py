import tkinter as tk

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")

for i in range(2):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(0, weight=1)

canvas = tk.Canvas(root, background="red")
Interface = tk.Frame(root, background="blue")

"""HERE GOES THE BUTTONS OF THE INTERFACE"""

"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""

canvas.grid(column=0, row=0, sticky="nsew")
Interface.grid(column=1, row=0, sticky="nsew")
root.mainloop()