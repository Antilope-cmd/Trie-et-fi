import sys
sys.dont_write_bytecode = True  #Prevents pycache; TODO:REMOVE THIS LINE BEFORE PROD

import tkinter as tk
from typing import Callable
from classes import Histogram, Colorstamp
from utils import *
from sorts import *
from time import sleep
from queue import Queue
import threading
import globals

WINDOW_COEFF = 0.5
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

array_size:int = 350
Colors = True

window_resize_schedule_id = ""

sorts = {
    "Tri à bulles" : bubblesort,
    "Tri par sélection" : selectionsort,
    "Tri par sélection optimisé" : optimized_selectionsort,
    "Tri par insertion" : insertionsort,
    "Tri par fusion" : merge_sort,
    "Tri rapide" : quick_sort
    }

"""Configuring window"""
root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")
root.title("Trie et fi")

root.grid_columnconfigure(0, weight=5)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)


canvas = tk.Canvas(root, background="black")
interface = tk.Frame(root, background="white", border=5)

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

canvas_dimensions = get_dimensions(canvas)



"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""

#NOTE:Important variables
main_list = [Histogram(i, canvas, width=20) for i in range(1, array_size+1)] #List that stores everything
ml = main_list  #alias for main_list


main_list_updates:list[int] = []    #List that stores pending GUI updates
mlu = main_list_updates #alias for main_list_updates

colored_dict:dict[str, list[Colorstamp]] = {    #Dictionary that stores the colors used by the program.
    "red" : [],
    "blue" : [],
    "green" : []
}

#Initialising histograms
for index, histogram in enumerate(main_list):
    histogram.draw(position=index, hist_amount=len(ml))

def on_resize(event):
    """Canvas redrawing scheduler"""
    global window_resize_schedule_id, canvas

    if window_resize_schedule_id:   #checking if update is already scheduled
        root.after_cancel(window_resize_schedule_id)    #prevent new scheduling

    #Hiding items when dragging/resizing to avoid jitter.
    canvas.itemconfig("all", state="hidden")
    window_resize_schedule_id = root.after(70, resize_graph)    #Scheduling update


def resize_graph():
    """Updates the Graph dimensions according to the window size"""
    global window_resize_schedule_id, ml, canvas_dimensions
    window_resize_schedule_id = None
    canvas_dimensions = get_dimensions(canvas)

    #Putting the items back.
    canvas.itemconfig("all", state="normal")
    root.after(1, lambda: update_canvas_display(ml, force_update=True))   #Recalculating
    
def change_len_mainlist(new_len):
    global main_list, array_size

    histogram_count_update.config(state="disabled")

    new_len = int(new_len)
    array_size = new_len
    new_list = [Histogram(i, canvas, width=20) for i in range(1, array_size+1)]

    main_list.clear()
    main_list.extend(new_list)
    
    canvas.delete("all")    #deleting all before redrawing

    for index, histogram in enumerate(main_list):
        histogram.draw(position=index, hist_amount=len(main_list))

    histogram_count_label.config(text=f"Choose the size of the array to sort (current: {array_size}):")

    update_canvas_display(main_list, force_update=True)

    histogram_count_update.config(state="active")
    return

sorting = False
expired_stamps:Queue[Colorstamp] = Queue()
def update_colors():
    global colored_dict, amount_stamps_deleted
    global expired_stamps

    while sorting:

        for color in colored_dict.keys():

            colorstamps = colored_dict[color]

            valid_stamps = []

            for stamp in colorstamps:

                if stamp.is_expired():
                    expired_stamps.put(stamp)
                
                else:
                    valid_stamps.append(stamp)
            
            colored_dict[color] = valid_stamps
        sleep(0.016)
    return

def delete_old_colors():
    global expired_stamps
    while not expired_stamps.empty():
        expired_stamps.get().reset_color()



scheduled_animation_id:str
def animate(moves_list:Queue):
    """Animation function for the GUI. Given a list of moves, this funtion will replicate them on the GUI."""
    global ml, mlu, t1
    global scheduled_animation_id
    global sorting
    
    if moves_list.empty():
        scheduled_animation_id = root.after(1, lambda: animate(moves_list))
        return
    
    action = moves_list.get()
    max_skips = 20
    skips = 0

    while Colors and action[0] == "compare" and skips < max_skips:
        _, i, j = action
        colorstamp1 = ml[i].change_color("red")
        colorstamp2 = ml[j].change_color("red")
        colored_dict["red"].extend((colorstamp1, colorstamp2))

        skips += 1

        action = moves_list.get()



    match action[0]:    #TODO: Comparisons outside the loop so we only animate the interesting things.
        
        case "swap":
            _, i, j = action
            ml[i].value, ml[j].value = ml[j].value, ml[i].value
            

            update_canvas_display(main_list=ml, pending_updates_list=[i, j])


            if Colors:
                colorstamp1 = ml[i].change_color("blue")
                colorstamp2 = ml[j].change_color("blue")
                colored_dict["blue"].extend((colorstamp1, colorstamp2))

        
        case "set":
            _, i, value = action
            ml[i].value = value

            update_canvas_display(main_list=ml, pending_updates_list=[i])

            if Colors:
                colorstamp1 = ml[i].change_color("green")
                colored_dict["green"].append(colorstamp1)

        case "finished":

            #Telling the threads to stop working.
            sorting = False
            globals.stop_sorting_flag.clear()

            root.after(10, lambda: erase_colors(colored_dict=colored_dict, hist_list=main_list))

            listbox.config(state="normal")
            sort_button.config(state="active")
            randomise_button.config(state="active")
            pause_sort_button.config(state="disabled")
            kill_sort_button.config(state="disabled")
            histogram_count_update.config(state="active")

            globals.moves_queue = Queue()

            return
    
    if Colors:
        delete_old_colors()
    
    scheduled_animation_id = root.after_idle(lambda: animate(moves_list))


def launch_sort(*args):
    global sorting
    
    sorting = True
    globals.stop_sorting_flag.clear()

    try:
        selection = listbox.curselection()
        selected_name = listbox.get(selection[0])

    except IndexError:
        return

    func: Callable = sorts[selected_name]

    listbox.config(state="disabled")
    sort_button.config(state="disabled")
    pause_sort_button.config(state="active")
    randomise_button.config(state="disabled")
    histogram_count_update.config(state="disabled")
    
    t1 = threading.Thread(target=func, args=args, daemon=True)
    t1.start()

    t2 = threading.Thread(target=update_colors, args=[], daemon=True)
    t2.start()

    root.after(1, lambda: animate(globals.moves_queue))

    return

def stop_animation():
    global scheduled_animation_id

    if scheduled_animation_id:
        root.after_cancel(scheduled_animation_id)
        
        pause_sort_button.config(text="Reprendre")
        kill_sort_button.config(state="active")
        
        scheduled_animation_id = ""
    else:
        scheduled_animation_id = root.after(1, lambda: animate(globals.moves_queue))

        pause_sort_button.config(text="Pause")
        kill_sort_button.config(state="disabled")
    return


def change_color_state():
    """Used to switch between black and white/colred (b&w makes performance improvements)"""
    global Colors, visual_colors
    Colors = not Colors
    if Colors:
        visual_colors.config(text='Couleurs')
    else:
        visual_colors.config(text='Noir et Blanc')
    erase_colors(colored_dict, ml)

def kill_sort():

    globals.stop_sorting_flag.set()

    globals.moves_queue = Queue()
    globals.moves_queue.put(("finished",))
    stop_animation()
    return

"""HERE GO THE BUTTONS OF THE INTERFACE"""
important_font_size = 18
secondary_font_size = 14

listbox = make_listbox(master=interface, sorts=sorts)   #Listbox to choose the algorithm
listbox.pack(fill="both", expand=True, padx=5, pady=1)

erase_colors_button = tk.Button(
    interface,
    text="Effacer couleurs",
    command=lambda: erase_colors(colored_dict=colored_dict, hist_list=main_list),
    width=15,
    font=("Arial", secondary_font_size)
    )

randomise_button = tk.Button(
    interface,
    text="Mélanger",
    command=lambda: shuffle_mainlist(main_list, colored_dict),
    width=15,
    font=("Arial", secondary_font_size)
    )

sort_button = tk.Button(
    interface,
    text="Trier",
    command=lambda: launch_sort(ml.copy()),    #use a copy of the list to avoid mutations while sorting
    width=15,
    font=("Arial", secondary_font_size)
    )

pause_sort_button = tk.Button(interface,
    text="Pause",
    command=stop_animation,
    width=15,
    state="disabled",
    font=("Arial", secondary_font_size)
    )

kill_sort_button = tk.Button(interface,
    text="Stop sorting",
    command=kill_sort,
    width=15,
    state="disabled",
    font=("Arial", secondary_font_size)
    )

visual_colors = tk.Button(
    interface,
    text="Couleurs",
    command=change_color_state,
    width=15,
    font=("Arial", secondary_font_size)
    )

histogram_count_label = tk.Label(
    interface,
    text=f"Choose the size of the array to sort (current: {array_size}):",
    font=("Arial", secondary_font_size)
)

vcmd = root.register(validate_input)
histogram_amount_entry = tk.Entry(
    interface,
    width=15,
    validate="key",
    validatecommand= (vcmd, "%P"),
    font=("Arial", secondary_font_size)
)

histogram_count_update = tk.Button(
    interface,
    text="Submit",
    command=lambda: change_len_mainlist(histogram_amount_entry.get()),
    width=15,
    font=("Arial", important_font_size)
)

erase_colors_button.pack(fill="both", expand=True, padx=5, pady=1)
randomise_button.pack(fill="both", expand=True, padx=5, pady=1)
sort_button.pack(fill="both", expand=True, padx=5, pady=1)
pause_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
kill_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
visual_colors.pack(fill="both", expand=True, padx=5, pady=1)
histogram_count_label.pack(fill="both", expand=True, padx=5, pady=1)
histogram_amount_entry.pack(fill="both", expand=True, padx=5, pady=1)
histogram_count_update.pack(fill="both", expand=True, padx=5, pady=1)


root.bind("<Configure>", on_resize)

root.mainloop()