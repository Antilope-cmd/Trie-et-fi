import tkinter as tk
from classes import Histogram

def get_dimensions(canvas:tk.Canvas):
    """returns Height/width"""
    return  canvas.winfo_height(), canvas.winfo_width()


def fill_percentage(canvas:tk.Canvas, percentage_x, percentage_y):
    height, width = get_dimensions(canvas)

    height_final = height*percentage_x/100
    width_final = width*percentage_y/100

    return height_final, width_final

def swap_values(main_list, index1, index2):
    color = 'blue'
    main_list[index1].change_color(color)
    main_list[index2].change_color(color)
    main_list[index1], main_list[index2] = main_list[index2], main_list[index1]
    return color  #TODO: NOT HERE BUT MAKE A FUNTION TO TURN BACK EVERYTHING WHITE WHILE STILL KEEPING A DELAY
            #NOTE: Maybe add a list of indexes that have their color changed so that we can turn them back white with O(1) efficiency.

def update_canvas_display(main_list:list[Histogram], force_update=False):
    """Refreshes the coordinates of the histogram according to the window"""

    for index, histogram in enumerate(main_list):
        histogram.update_coords(spacing=5, position=index, force_update=force_update)
    return