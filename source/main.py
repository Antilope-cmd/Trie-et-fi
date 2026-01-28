import tkinter as tk
from classes import *
from random import randint, shuffle

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")

for i in range(2):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(0, weight=1)



canvas = tk.Canvas(root, background="red")
interface = tk.Frame(root, background="blue")

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

HEIGHT_CANVAS = canvas.winfo_height()
WIDTH_CANVAS = canvas.winfo_width()

main_list = [Histogram(randint(30, 500), canvas, width=20) for i in range(30)]


"""HERE GOES THE BUTTONS OF THE INTERFACE"""
def shuffle_mainlist() -> None:
    global main_list
    main_list = shuffle(main_list)
    return
randomise_button = tk.Button(interface, text="Mélanger", command=shuffle_mainlist)

randomise_button.pack()



"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""
def canvas_mainloop():
    canvas.delete("all")    
    for index, histogram in enumerate(main_list):
        histogram.draw(canvas, position=index, spacing=5)
    root.after(10, canvas_mainloop)
    return
    


root.after(500, canvas_mainloop)
root.mainloop()