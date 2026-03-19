import sys
sys.dont_write_bytecode = True


import tkinter as tk
import os
from classes import Histogram, Colorstamp
from utils import *
from sorts import *
from time import sleep
from queue import Queue
import threading
import globals

WINDOW_COEFF = 0.7
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920


Colors = True
array_size:int = 350
delay:int = 0

window_resize_schedule_id = ""


"""Configuring window"""
root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")
root.title("Trie et fi")
root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))

root.grid_columnconfigure(0, weight=5)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)


canvas = tk.Canvas(root, background="black")

interface = tk.Frame(root, background="white", border=5)
array_size_menu = tk.Frame(interface, background="white", width=25)
delay_menu = tk.Frame(interface, background="white", width=25)

canvas.grid(column=0, row=0, sticky="nsew")
interface.grid(column=1, row=0, sticky="nsew")

canvas_dimensions = get_dimensions(canvas)



"""HERE GOES THE LOGIC TO REPRESENT A LIST OF NUMBERS"""

#NOTE:Important variables
main_list = [Histogram(i, canvas, width=20) for i in range(1, array_size+1)] #List that stores everything
ml = main_list  #alias for main_list


main_list_updates:list[int] = []    #List that stores pending GUI updates
mlu = main_list_updates #alias for main_list_updates

colored_dict:dict[str, list[Colorstamp]] = {    #Dictionary that stores the active colors on the GUI.
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
        root.after_cancel(window_resize_schedule_id)    #prevent mass scheduling

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

    if new_len == "":
        return

    histogram_count_submit.config(state="disabled")

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

    histogram_count_submit.config(state="active")
    return

def change_delay(new_delay):
    global delay

    if new_delay == "":
        return

    delay = int(new_delay)

    delay_label.config(text=f"Choose the delay between each move (current: {delay}ms)")
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
        print("waiting for moves to load")
        return
    
    action = moves_list.get()
    #The greater the delay, the less skips happen to keep everything smooth
    #Max/min skips possible: 20/1
    max_skips = max( 1,
                min(
        20,
        int( 20 * (40/(delay+1) ) )
        
        ))
    skips = 0

    while Colors and action[0] == "compare" and skips < max_skips:
        _, i, j = action
        colorstamp1 = ml[i].change_color("red")
        colorstamp2 = ml[j].change_color("red")
        colored_dict["red"].extend((colorstamp1, colorstamp2))

        skips += 1

        if moves_list.empty():
            break

        action = moves_list.get()
        
    if action[0] == "compare" and Colors:
        _, i, j = action
        colorstamp1 = ml[i].change_color("red")
        colorstamp2 = ml[j].change_color("red")
        colored_dict["red"].extend((colorstamp1, colorstamp2))



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
            histogram_count_submit.config(state="active")

            globals.moves_queue = Queue()

            return
    
    if Colors:
        delete_old_colors()
    
    if not delay:
        scheduled_animation_id = root.after_idle(lambda: animate(moves_list))
    
    else:
        scheduled_animation_id = root.after(delay, lambda: animate(moves_list))
    
    return


def launch_sort(*args):
    global sorting
    
    sorting = True
    globals.stop_sorting_flag.clear()

    try:
        selection = listbox.curselection()
        selected_name = listbox.get(selection[0])

    except IndexError:
        return

    func = sorts_dict[selected_name]

    listbox.config(state="disabled")
    sort_button.config(state="disabled")
    pause_sort_button.config(state="active")
    randomise_button.config(state="disabled")
    histogram_count_submit.config(state="disabled")
    
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
        
        pause_sort_button.config(text="Resume")
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
        visual_colors.config(text='Colors: enabled')
    else:
        visual_colors.config(text='Colors: disabled')
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

listbox = make_listbox(master=interface, sorts=sorts_dict)   #Listbox to choose the algorithm
listbox.pack(fill="both", expand=True, padx=5, pady=1)

randomise_button = tk.Button(
    interface,
    text="Randomise",
    command=lambda: shuffle_mainlist(main_list, colored_dict),
    width=15,
    font=("Arial", secondary_font_size)
    )

sort_button = tk.Button(
    interface,
    text="► Launch sort",
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
    text="■ Stop sorting",
    command=kill_sort,
    width=15,
    state="disabled",
    font=("Arial", secondary_font_size)
    )

visual_colors = tk.Button(
    interface,
    text="Colors: enabled",
    command=change_color_state,
    width=15,
    font=("Arial", secondary_font_size)
    )

menu_separator = tk.Label(interface, text="_________________________________", font=("Arial", important_font_size))

histogram_count_label = tk.Label(
    interface,
    text=f"Choose the size of the array to sort (current: {array_size})",
    font=("Arial", secondary_font_size)
)

vcmd = root.register(validate_input)
histogram_amount_entry = tk.Entry(
    array_size_menu,
    width=15,
    highlightbackground="red",
    validate="key",
    validatecommand= (vcmd, "%P"),
    font=("Arial", secondary_font_size),
    relief="solid",
    borderwidth=1,
)

histogram_count_submit = tk.Button(
    array_size_menu,
    text="Submit",
    command=lambda: change_len_mainlist(histogram_amount_entry.get()),
    width=10,
    font=("Arial", important_font_size),
)

delay_label = tk.Label(
    interface,
    text=f"Choose the delay between each move (current: {delay}ms)",
    font=("Arial", secondary_font_size)
)

delay_entry = tk.Entry(
    delay_menu,
    width=15,
    validate="key",
    validatecommand= (vcmd, "%P"),
    font=("Arial", secondary_font_size),
    relief="solid",
    borderwidth=1,
)

delay_submit_button = tk.Button(
    delay_menu,
    text="Submit",
    command=lambda: change_delay(delay_entry.get()),
    width=10,
    font=("Arial", important_font_size),
)

randomise_button.pack(fill="both", expand=True, padx=5, pady=1)
sort_button.pack(fill="both", expand=True, padx=5, pady=1)
pause_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
kill_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
visual_colors.pack(fill="both", expand=True, padx=5, pady=1)

menu_separator.pack(fill="both", expand=False, padx=5)


array_size_menu.columnconfigure(0, weight=1)
array_size_menu.columnconfigure(1, weight=1)

delay_menu.columnconfigure(0, weight=1)
delay_menu.columnconfigure(1, weight=1)

histogram_count_label.pack(fill="both", expand=True, padx=5, pady=0)

histogram_amount_entry.grid(column=0, row=0, sticky="nwse")
histogram_count_submit.grid(column=1, row=0, sticky="nwse")
array_size_menu.pack(fill="both", expand=True, padx=5, pady=0)

delay_label.pack(fill="both", expand=True, padx=5, pady=0)

delay_entry.grid(column=0, row=0, sticky="nwse")
delay_submit_button.grid(column=1, row=0, sticky="nwse")
delay_menu.pack(fill="both", expand=True, padx=5, pady=0)

root.bind("<Configure>", on_resize)

root.mainloop()