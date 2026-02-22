import tkinter as tk

class Histogram():
    
    def __init__(self, value:float, canvas:tk.Canvas, width:int) -> None:
        self.value:float = value
        self.height:float = value
        self.width:float = width
        self.colour = "white"
        self.canvas:tk.Canvas = canvas  #Stroring the canvas reference to avoid asking for it later.

        #Setup rectangle id to allow modifications without redrawing.
        self.canvas_id:int
    
    def get_dimensions(self):
        return self.canvas.winfo_height(), self.canvas.winfo_width()

    def draw(self, position:int, hist_amount:int):
        """Draws the histogram on the canvas. Only to be used at initialisation."""
        self.previous_position = position
        
        canvas_height, canvas_width = self.get_dimensions()

        self.width = (canvas_width-10)/hist_amount

        self.x1 = position*(self.width) + 10
        self.y1 = canvas_height
        self.x2 = self.x1 + self.width
        self.y2 = canvas_height - self.height
        self.canvas_id = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.colour, outline='')
        return
    
    def update_coords(self, position:int, hist_amount:int, force_update=False):

        if position == self.previous_position and not force_update:
            return  #If position in the list didn't change no need to update the coordinates
        
        self.previous_position = position
        canvas_height, canvas_width = self.get_dimensions()
        self.width = (canvas_width-10)/hist_amount
        self.x1 = position*(self.width) + 10
        self.y1 = canvas_height
        self.x2 = self.x1 + self.width
        self.y2 = canvas_height - self.height
        self.canvas.coords(self.canvas_id, self.x1, self.y1, self.x2, self.y2)
        return

    def change_color(self, colour:str) -> None:
        self.colour = colour
        self.canvas.itemconfig(self.canvas_id, fill=colour)
        return