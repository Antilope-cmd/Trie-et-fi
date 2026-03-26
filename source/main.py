import tkinter as tk
import os   #Used for the iconbitmap
from classes import Histogram, Colorstamp
from utils import *
from sorts import *
from time import sleep
from queue import Queue
from draw_window import draw_graph
import threading
import globals

#Configuring height/width of the window
WINDOW_COEFF = 0.7
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920

#Mutating variables
array_size:int = 350    #Used to control how big the array is
Colors = True   #Used to know wether to display colors or not
delay:int = 0   #Configues how much delay there is between moves

window_resize_schedule_id = ""  #Used to know wether a <Config> update is already scheduled


"""Configuring window"""
root = tk.Tk()
root.geometry(f"{int(WINDOW_COEFF*WINDOW_WIDTH)}x{int(WINDOW_COEFF*WINDOW_HEIGHT)}")
root.title("Trie et Fi")

try:    #Try to put logo on top left corner
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
except:
    print("failed to load iconbitmap")
    pass

#Only the canvas grows when window expanded.
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_rowconfigure(0, weight=1)

#Used to display the Histograms
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
    """Used to change the amount of histograms to sort"""
    global main_list, array_size, histogram_amount_entry
    
    histogram_amount_entry.config(validate="none")
    histogram_amount_entry.delete(0, 'end')
    histogram_amount_entry.config(validate="key")

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

    delay_entry.configure(validate="none")
    delay_entry.delete(0, tk.END)
    delay_entry.configure(validate="key")

    if new_delay == "":
        return

    delay = int(new_delay)

    delay_label.config(text=f"Choose the delay between each move (current: {delay}ms)")
    return


expired_stamps:Queue[Colorstamp] = Queue()
def update_colors():
    """Filters the colortamps and puts them into expired_stamps queue for processing"""
    global colored_dict, amount_stamps_deleted
    global expired_stamps

    while not globals.stop_sorting_flag.is_set():

        for color in colored_dict.keys():   #Filtering

            colorstamps = colored_dict[color]

            valid_stamps = []

            for stamp in colorstamps:

                if stamp.is_expired():
                    expired_stamps.put(stamp)
                
                else:
                    valid_stamps.append(stamp)
            
            colored_dict[color] = valid_stamps

        sleep(0.016)    #Only do it at 60fps to avoid hogging ressources
    return

def delete_old_colors():
    """Used by the main thread to reset all the colors in the expired_stamps queue"""
    global expired_stamps
    while not expired_stamps.empty():
        expired_stamps.get().reset_color()



scheduled_animation_id:str
def animate(moves_list:Queue):
    """Animation function for the GUI. Given a list of moves, this funtion will replicate them on the GUI."""
    global ml, scheduled_animation_id
    
    #This condition means that the thread hasn't finished computing the moves yet
    if moves_list.empty():
        scheduled_animation_id = root.after(1, lambda: animate(moves_list)) #waiting
        print("waiting for moves to load")
        return
    
    action = moves_list.get() #Getting the fist move in the queue(FIFO)

    #The greater the delay, the less skips happen to keep everything smooth
    #Max/min skips possible: 20/1
    max_skips = max( 1,
                min(
        20,
        int( 5 * (40/(delay*3+1) ) )
        
        ))
    skips = 0

    #I don't value compare action, they are boring
    #So I skip them
    while Colors and action[0] == "compare" and skips < max_skips:
        _, i, j = action
        colorstamp1 = ml[i].change_color("red")
        colorstamp2 = ml[j].change_color("red")
        colored_dict["red"].extend((colorstamp1, colorstamp2))

        skips += 1

        if moves_list.empty():
            break

        action = moves_list.get()
    
    #Catching last compare action
    if action[0] == "compare" and Colors:
        _, i, j = action
        colorstamp1 = ml[i].change_color("red")
        colorstamp2 = ml[j].change_color("red")
        colored_dict["red"].extend((colorstamp1, colorstamp2))



    match action[0]:
        
        case "swap":
            _, i, j = action #Retrieving indecies of swap
            ml[i].value, ml[j].value = ml[j].value, ml[i].value #Swap
            

            update_canvas_display(main_list=ml, pending_updates_list=[i, j])


            if Colors: #Coloring blue swaps
                colorstamp1 = ml[i].change_color("blue")
                colorstamp2 = ml[j].change_color("blue")
                colored_dict["blue"].extend((colorstamp1, colorstamp2))

        
        case "set":
            _, i, value = action #Retriving index and value
            ml[i].value = value #Setting value at index

            update_canvas_display(main_list=ml, pending_updates_list=[i])

            if Colors: #Coloring set action green
                colorstamp1 = ml[i].change_color("green")
                colored_dict["green"].append(colorstamp1)

        case "finished":

            #Telling the threads to stop working.
            globals.stop_sorting_flag.clear()

            #Erase remaining colors
            root.after(10, lambda: erase_colors(colored_dict=colored_dict, hist_list=main_list))

            #Reconfigure buttons
            listbox.config(state="normal")
            sort_button.config(state="active")
            randomise_button.config(state="active")
            pause_sort_button.config(state="disabled")
            kill_sort_button.config(state="disabled")
            histogram_count_submit.config(state="active")

            #Clearing moves_queue to avoid leaking into another sort
            globals.moves_queue = Queue()

            return
    
    if Colors:
        delete_old_colors()
    
    #Scheduling next move
    if delay:
        scheduled_animation_id = root.after(delay, lambda: animate(moves_list))
        return

    scheduled_animation_id = root.after_idle(lambda: animate(moves_list))
    
    return


def launch_sort(*args):
    """Function used to start a program. Will setup and call animate()"""
    
    globals.stop_sorting_flag.clear() #Clearing flag to sort again

    try:
        selection = listbox.curselection()
        selected_name = listbox.get(selection[0])

    except IndexError: #If no selection -> return
        return

    # Retrieving the sorting algorithm
    func = sorts_dict[selected_name]

    listbox.config(state="disabled")
    sort_button.config(state="disabled")
    pause_sort_button.config(state="active")
    randomise_button.config(state="disabled")
    histogram_count_submit.config(state="disabled")
    
    #Calling the sorting algorithm on a separate thread
    t1 = threading.Thread(target=func, args=args, daemon=True)
    t1.start()

    #Starting to filter colors
    t2 = threading.Thread(target=update_colors, args=[], daemon=True)
    t2.start()

    #Launching the animation
    root.after(1, lambda: animate(globals.moves_queue))

    return

def stop_animation():
    global scheduled_animation_id

    if scheduled_animation_id:
        root.after_cancel(scheduled_animation_id) #Cancels next frame
        
        pause_sort_button.config(text="Resume")
        kill_sort_button.config(state="active")
        
        scheduled_animation_id = "" #Resets scheduling
    else:
        scheduled_animation_id = root.after(1, lambda: animate(globals.moves_queue)) #Resume by scheduling next frame

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
    """Used to stop sorting."""
    #Signalings threads to stop
    globals.stop_sorting_flag.set()

    #Resetting moves queue
    globals.moves_queue = Queue()
    #Telling UI to stop animation
    globals.moves_queue.put(("finished",))
    stop_animation()
    return

def apply_graph():
    global main_list, ml

    root.winfo_toplevel().attributes("-disabled", True)

    def draw_and_update():
        global main_list, ml

        histogram_input = draw_graph(array_size)

        main_list.clear()
        main_list.extend([Histogram(i*array_size, canvas, width=20) for i in histogram_input])
        ml = main_list

        canvas.delete("all")

        for index, histogram in enumerate(main_list):
            histogram.draw(position=index, hist_amount=len(main_list))

        update_canvas_display(main_list, force_update=True)
        root.winfo_toplevel().attributes("-disabled", False)

    threading.Thread(target=draw_and_update, daemon=True).start()


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

draw_graph_button = tk.Button(
    interface,
    text="Draw my graph",
    command=apply_graph,
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


"""Packing up the interface"""

randomise_button.pack(fill="both", expand=True, padx=5, pady=1)
sort_button.pack(fill="both", expand=True, padx=5, pady=1)
pause_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
kill_sort_button.pack(fill="both", expand=True, padx=5, pady=1)
visual_colors.pack(fill="both", expand=True, padx=5, pady=1)
draw_graph_button.pack(fill="both", expand=True, padx=5, pady=1)

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