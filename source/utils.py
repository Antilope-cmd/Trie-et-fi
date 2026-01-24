import tkinter as tk

def get_dimensions(canvas:tk.Canvas):
    """returns Height/width"""
    return  canvas.winfo_height(), canvas.winfo_width()


def fill_percentage(dimensions):
