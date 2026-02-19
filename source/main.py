import sys
sys.dont_write_bytecode = True  #Prevents pycache; TODO:REMOVE THIS LINE BEFORE PROD

import tkinter as tk
from classes import Histogram
from random import randint, shuffle
from utils import swap_values, get_dimensions, update_canvas_display


WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
ARRAY_SIZE = 30

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
main_list = [Histogram(randint(30, 500), canvas, width=20) for i in range(ARRAY_SIZE)]
ml = main_list
colored_dict:dict[str, list[int]] = {
    "red" : [],
    "blue" : []
}

#Initialising histograms
for index, histogram in enumerate(main_list):
    histogram.draw(position=index, spacing=5)

def swap(index1, index2):
    global ml
    color = swap_values(ml, index1, index2) #Both saving the color of the histogram and swapping the Hist.
    update_canvas_display(ml)
    colored_dict[color] += [index1, index2]
    return

def resize_graph(*_event):
    """Updates the Canvas display only when the dimentions changes"""
    global main_list, canvas_dimensions
    new_dimensions = get_dimensions(canvas)

    if canvas_dimensions == new_dimensions:
        return
    
    canvas_dimensions = new_dimensions
    update_canvas_display(ml, force_update=True)
    

"""HERE GO THE BUTTONS OF THE INTERFACE"""
def shuffle_mainlist() -> None:
    global main_list
    shuffle(main_list)
    update_canvas_display(ml)
    return

def erase_colors(*colors):
    global colored_dict, main_list

    if colors:
        # TODO: handle specific colors
        return

    for clr, indexes in colored_dict.items():
        for index in indexes:
            main_list[index].change_color("white")
        indexes.clear()



erase_colors_button = tk.Button(interface, text="Effacer couleurs", command=erase_colors)
erase_colors_button.pack()
randomise_button = tk.Button(interface, text="Mélanger", command=shuffle_mainlist)
randomise_button.pack()
switch_button = tk.Button(interface, text="Swap", command=lambda: swap(randint(0, ARRAY_SIZE-1), randint(0, ARRAY_SIZE-1)))
switch_button.pack()
canvas.bind("<Configure>", resize_graph)
root.mainloop()