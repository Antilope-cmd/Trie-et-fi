import sys
sys.dont_write_bytecode = True  #Prevents pycache; TODO:REMOVE THIS LINE BEFORE PROD

import tkinter as tk
from classes import Histogram
from random import randint, shuffle
from utils import swap_values, get_dimensions


WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")

for i in range(2):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(0, weight=1)



canvas = tk.Canvas(root, background="red")
interface = tk.Frame(root, background="blue")

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

canvas_dimensions = get_dimensions(canvas)




"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""
main_list = [Histogram(randint(30, 500), canvas, width=20) for i in range(30)]
ml = main_list

#Initialising histograms
for index, histogram in enumerate(main_list):
    histogram.draw(position=index, spacing=5)

def swap(index1, index2):
    global ml
    swap_values(ml, index1, index2)
    update_canvas_display()
    return

def update_canvas_display(force_update=False):
    """Refreshes the coordinates of the histogram according to the window"""

    print("canvs dimensions: ", get_dimensions(canvas))   #TODO: DELETE THIS DEBBUGGING LINE
    for index, histogram in enumerate(main_list):
        histogram.update_coords(spacing=5, position=index, force_update=force_update)
    return

def resize_graph(*_event):
    """Updates the Canvas display only when the dimentions changes"""
    global main_list, canvas_dimensions
    new_dimensions = get_dimensions(canvas)

    if canvas_dimensions == new_dimensions:
        return
    
    canvas_dimensions = new_dimensions
    update_canvas_display(force_update=True)
    

"""HERE GO THE BUTTONS OF THE INTERFACE"""
def shuffle_mainlist() -> None:
    global main_list
    shuffle(main_list)
    update_canvas_display()
    return

randomise_button = tk.Button(interface, text="Mélanger", command=shuffle_mainlist)
randomise_button.pack()
switch_button = tk.Button(interface, text="Swap", command=lambda: swap(randint(0, 29), randint(0, 29)))
switch_button.pack()
canvas.bind("<Configure>", resize_graph)
root.mainloop()