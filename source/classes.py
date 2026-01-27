import tkinter as tk
from utils import *

class Histogram():
    
    def __init__(self, value:float, canvas:tk.Canvas, width) -> None:
        canvas_height, _ = get_dimensions(canvas)
        self.value = value
        self.height = value
        self.width = width

    def draw(self, canvas:tk.Canvas, position:int, spacing:int):
        canvas_height, canvas_width = get_dimensions(canvas)
        x1 = position*(spacing+self.width) + 10
        y1 = canvas_height
        x2 = x1+self.width
        y2 = canvas_height - self.height
        canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        return