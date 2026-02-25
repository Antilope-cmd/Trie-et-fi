import sys
sys.dont_write_bytecode = True  #Prevents pycache; TODO:REMOVE THIS LINE BEFORE PROD

import tkinter as tk
from typing import Callable
from classes import Histogram, Colorstamp
from random import randint, shuffle
from utils import *
from sorts import bubble_sort as bs, selection_sort as ss, optimized_selection_sort as oss, insertion_sort as ins
import threading

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

ARRAY_SIZE = 500
Colors = True

root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")


root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)



canvas = tk.Canvas(root, background="black")
interface = tk.Frame(root, background="white", border=5)

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

canvas_dimensions = get_dimensions(canvas)




"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""
main_list = [Histogram(i, canvas, width=20) for i in range(ARRAY_SIZE)]
ml = main_list
moves_queue = []

main_list_updates:list[int] = []
mlu = main_list_updates

colored_dict:dict[str, list[Colorstamp]] = {
    "red" : [],
    "blue" : []
}

#Initialising histograms
for index, histogram in enumerate(main_list):
    histogram.draw(position=index, hist_amount=len(ml))

window_resize_schedule_id = None
def on_resize(event):
    """Canvas redrawing scheduler"""
    global window_resize_schedule_id

    if window_resize_schedule_id:   #checking if update is already scheduled
        root.after_cancel(window_resize_schedule_id)    #prevent new scheduling
    
    window_resize_schedule_id = root.after(70, resize_graph)    #Scheduling update



def resize_graph():
    """Updates the Graph dimensions according to the window size"""
    global window_resize_schedule_id, main_list, canvas_dimensions

    window_resize_schedule_id = None
    canvas_dimensions = get_dimensions(canvas)

    root.after_idle(lambda: update_canvas_display(ml, force_update=True))
    resizing = False
    

"""HERE GO THE BUTTONS OF THE INTERFACE"""



    
def update_colors():
    global colored_dict
    
    for color, colorstamps in colored_dict.items():

        while colorstamps and colorstamps[0].is_expired():
            colorstamps[0].reset_color()
            colorstamps.pop(0)


scheduled_animation_id = None
def animate(moves_list:list):
    global ml, mlu, t1
    global scheduled_animation_id
    
    if not moves_list:
        print("waiting for moves to load!")
        scheduled_animation_id = root.after(1, lambda: animate(moves_list))
        return
    
    action = moves_list.pop(0)

    match action[0]:
        
        case "swap":
            _, i, j = action
            ml[i], ml[j] = ml[j], ml[i]
            
            mlu.extend((i, j))
            update_canvas_display(main_list=ml, pending_updates_list=mlu)
            mlu.clear()

            if Colors:
                colorstamp1 = ml[i].change_color("blue")
                colorstamp2 = ml[j].change_color("blue")
                colored_dict["blue"].extend((colorstamp1, colorstamp2))

        
        case "compare":
            if Colors:
                _, i, j = action
                colorstamp1 = ml[i].change_color("red")
                colorstamp2 = ml[j].change_color("red")
                colored_dict["red"].extend((colorstamp1, colorstamp2))

        case "finished":
            print("list sorted!")
            root.after(10, lambda: erase_colors(colored_dict=colored_dict, hist_list=main_list))
            return
    
    if Colors:
        update_colors()
    
    if not animation:
        
        return
    
    scheduled_animation_id = root.after_idle(lambda: animate(moves_list))

animation = True
def stop_animation():
    global animation
    animation = False

def launch_sort(*args):
    global moves_queue, listbox
    global sort_button, randomise_button
    global stop_sort_button, erase_colors_button
    
    try:
        selection = listbox.curselection()
        selected_name = listbox.get(selection[0])
    except IndexError:
        print("Choisissez un mode de tri!")
        return

    func: Callable = sorts[selected_name]
    
    t1 = threading.Thread(target=func, args=args, daemon=True)
    t1.start()
    root.after(1, lambda: animate(moves_queue))

def change_color_state():
    global Colors, visual_colors
    Colors = not Colors
    if Colors:
        visual_colors.config(text='Remove Colors')
    else:
        visual_colors.config(text='Add Colors')
    erase_colors(colored_dict, ml)


sorts = {
    "Tri à bulles" : bs.bubblesort,
    "Tri par sélection" : ss.selectionsort,
    "Tri par sélection optimisé" : oss.optimized_selectionsort,
    "Tri par insertion" : ins.insertion_sort
    }

listbox = make_listbox(master=interface, sorts=sorts)
listbox.pack()

erase_colors_button = tk.Button(interface, text="Effacer couleurs", command=lambda: erase_colors(colored_dict=colored_dict, hist_list=main_list))

randomise_button = tk.Button(interface, text="Mélanger", command=lambda: shuffle_mainlist(main_list, colored_dict))

sort_button = tk.Button(interface, text="Sort", command=lambda: launch_sort(ml, moves_queue))

stop_sort_button = tk.Button(interface, text="Stop Sorting", command=stop_animation)

visual_colors = tk.Button(interface, text="Remove Colors", command=change_color_state)



erase_colors_button.pack()
randomise_button.pack()
sort_button.pack()
stop_sort_button.pack()
visual_colors.pack()


canvas.bind("<Configure>", on_resize)

root.mainloop()