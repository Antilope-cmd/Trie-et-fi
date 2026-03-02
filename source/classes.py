import tkinter as tk
from time import time

class Colorstamp():
    """Class used to store the current color and validity of a color from a Histogram"""
    def __init__(self, color:str, duration:int, canvas:tk.Canvas, canvas_id:int) -> None:
        self.hist_id = canvas_id
        self.color = color
        self.timestamp = time()
        self.validity = duration
        self.canvas:tk.Canvas = canvas
    
    def is_expired(self):
        if time() - self.timestamp >= self.validity:
            return True
        return False
    
    def reset_color(self) -> None:
        self.canvas.itemconfig(self.hist_id, fill="white")
        return


class Histogram():
    '''Class used to representthe value of the main array'''
    def __init__(self, value:int, canvas:tk.Canvas, width:int) -> None:
        self.value:int = value
        self.height:float = value
        self.width:float = width
        self.colour = "white"
        self.canvas:tk.Canvas = canvas  #Storing the canvas reference to avoid asking for it later.

        self.previous_position:int
        self.previous_value:int

        #Setup rectangle id to allow modifications without redrawing.
        self.canvas_id:int
    
    def get_dimensions(self):
        return self.canvas.winfo_height(), self.canvas.winfo_width()

    def draw(self, position:int, hist_amount:int):
        """Draws the histogram on the canvas. Only to be used at initialisation."""
        self.previous_value = self.value

        canvas_height, canvas_width = self.get_dimensions()

        self.width = (canvas_width-20)/hist_amount

        self.x1 = position*(self.width) + 10
        self.y1 = canvas_height
        self.x2 = self.x1 + self.width
        self.y2 = canvas_height - self.height
        self.canvas_id = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.colour, outline='')
        return
    
    def update_coords(self, position:int, hist_amount:int, force_update=False):
        ''' position        is the position of the histogram in the array
            hist_amound     is the maximum size posible for an istogram in this array
            force_update    allow to force the update event if the position in the array didn't change'''

        if (self.previous_value == self.value) and (not force_update):
            return  #If position and value in the list didn't change no need to update the coordinates

        canvas_height, canvas_width = self.get_dimensions()
        self.previous_value = self.value
        
        
        self.window_height_percentage = self.value/hist_amount
        self.height = int(self.window_height_percentage * canvas_height)
        self.width = (canvas_width-20)/hist_amount

        self.x1 = position*(self.width) + 10
        self.y1 = canvas_height
        self.x2 = self.x1 + self.width
        self.y2 = canvas_height - self.height
        self.canvas.coords(self.canvas_id, self.x1, self.y1, self.x2, self.y2)
        return

    def change_color(self, color:str, duration=1) -> Colorstamp:
        self.colour = color
        self.canvas.itemconfig(self.canvas_id, fill=color)
        return Colorstamp(color=color, duration=duration, canvas=self.canvas, canvas_id=self.canvas_id)

