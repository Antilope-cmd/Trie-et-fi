import tkinter as tk
from classes import Histogram
from random import shuffle

def get_dimensions(canvas:tk.Canvas):
    """returns Height/width"""
    return  canvas.winfo_height(), canvas.winfo_width()

def update_canvas_display(main_list:list[Histogram], pending_updates_list:list[int]=[], force_update=False):
    """Refreshes the coordinates of the histogram according to the window"""

    n = len(main_list)

    if pending_updates_list:    #If the pending upates list is provided, we only iterate through it.
        for index in pending_updates_list:
            main_list[index].update_coords(position=index, hist_amount=n, force_update=False)
        return


    for index, histogram in enumerate(main_list): #If no pending updates, go though the whole array
        histogram.update_coords(hist_amount=n, position=index, force_update=force_update)
    return

def erase_colors(colored_dict, hist_list):
    """Erases all colors from the canvas"""
    for hist in hist_list:
        hist.change_color("white")

    for color in colored_dict:
        colored_dict[color].clear()

def make_listbox(master, sorts:dict):
    """Uses the keys of a dict to build a tk.listbox."""

    listbox = tk.Listbox(master, width=50, font=("Arial", 18))
    for sort_name in sorts.keys(): #Take all the keys to make titles.
        listbox.insert(0, sort_name)
    return listbox


def shuffle_mainlist(mainlist, colored_dict) -> None:
    """Shuffles a list[Histogram]"""
    erase_colors(colored_dict=colored_dict, hist_list=mainlist)
    shuffle(mainlist)
    update_canvas_display(main_list=mainlist, force_update=True)
    return

def validate_input(P):
    """Only allows numerical characters."""
    try:
        P = int(P)  
        return True
    
    except:
        pass
    return False