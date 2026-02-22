import sys
sys.dont_write_bytecode = True  #Prevents pycache; TODO:REMOVE THIS LINE BEFORE PROD

import tkinter as tk
from typing import Callable
from classes import Histogram
from random import randint, shuffle
from utils import get_dimensions, update_canvas_display
from sorts import bubble_sort as bs
#NOTE: Tkinter IS NOT threading safe, do NOT import threading

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
ARRAY_SIZE = 100
DELAY = 1

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")


root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)



canvas = tk.Canvas(root, background="red")
interface = tk.Frame(root, background="blue")

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

canvas_dimensions = get_dimensions(canvas)




"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""
main_list = [Histogram(i, canvas, width=20) for i in range(ARRAY_SIZE)]
ml = main_list
colored_dict:dict[str, list[int]] = {
    "red" : [],
    "blue" : []
}

#Initialising histograms
for index, histogram in enumerate(main_list):
    histogram.draw(position=index, hist_amount=len(ml))


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
    erase_colors()
    shuffle(main_list)
    update_canvas_display(ml)
    return

def erase_colors(*colors:str):
    global colored_dict, main_list

    if colors:
        for color in colors:
            for index in colored_dict[color]:
                main_list[index].change_color("white")
            colored_dict[color].clear()
        return

    for clr, indexes in colored_dict.items():
        for index in indexes:
            main_list[index].change_color("white")
        indexes.clear()


def animate(gen):
    global ml, colored_dict #TODO: REDO THE FUNCTION WITH MATCH AND CASE
    action = next(gen)

    if action[0] == "compare":
        _, i, j = action
        ml[i].change_color("red")
        ml[j].change_color("red")
        colored_dict["red"].append(i)
        colored_dict["red"].append(j)
    
    elif action[0] == "swap":
        _, i, j = action
        ml[i].change_color("blue")
        ml[j].change_color("blue")
        colored_dict["blue"].append(i)
        colored_dict["blue"].append(j)
        update_canvas_display(main_list=ml, force_update=True)
    
    elif action[0] == "delay":
        root.after(DELAY, lambda: animate(gen))
    
    elif action[0] == "clearcolors":
        erase_colors()

    elif action[0] == "clearcolor":
        color_to_clear = action[1]
        erase_colors(color_to_clear)
    
    elif action[0] == "finished":
        print("List sorted!")
        return
    
    root.after(1, lambda: animate(gen))


def launch_sort(func: Callable, *args):
    gen = func(*args)
    animate(gen)


erase_colors_button = tk.Button(interface, text="Effacer couleurs", command=erase_colors)
erase_colors_button.pack()
randomise_button = tk.Button(interface, text="Mélanger", command=shuffle_mainlist)
randomise_button.pack()
sort_button = tk.Button(interface, text="Sort", command=lambda: launch_sort(bs.bubblesort, ml))
sort_button.pack()
canvas.bind("<Configure>", resize_graph)
root.mainloop()