import tkinter as tk
from classes import *
from random import randint

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")

for i in range(2):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(0, weight=1)



canvas = tk.Canvas(root, background="red")
Interface = tk.Frame(root, background="blue")

canvas.grid(column=0, row=0, sticky="nsew")
Interface.grid(column=1, row=0, sticky="nsew")

HEIGHT_CANVAS = canvas.winfo_height()
WIDTH_CANVAS = canvas.winfo_width()



"""HERE GOES THE BUTTONS OF THE INTERFACE"""




"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""
main_list = [Histogram(randint(30, 500), canvas, width=20) for i in range(30)]
def canvas_mainloop():
    canvas.delete("all")    
    for index, histogram in enumerate(main_list):
        histogram.draw(canvas, position=index, spacing=5)
    root.after(10, canvas_mainloop)
    return
    


root.after(500, canvas_mainloop)
root.mainloop()