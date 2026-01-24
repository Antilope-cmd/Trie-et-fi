import tkinter as tk

def get_dimensions(canvas:tk.Canvas):
    """returns Height/width"""
    return  canvas.winfo_height(), canvas.winfo_width()


def fill_percentage(canvas:tk.Canvas, percentage_x, percentage_y):
    height, width = get_dimensions(canvas)
    height_final = height*percentage_x/100
    width_final = width*percentage_y/100
    return width_final, height_final