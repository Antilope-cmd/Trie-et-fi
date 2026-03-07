from classes import Histogram
from utils import shuffle_mainlist, update_canvas_display
from main import colored_dict
import globals

""" boggo sort is a sorting algorithm who shuffle the array util it's sorted.
        average complexity O(n*n!) | best case  O(n) | worst case O(∞)"""


def bogosort(hist_list:list[Histogram]):
    is_sorted = False
    while is_sorted == False:
        for i in range(len(hist_list)):                         # look inside of hist_list to see if it is sorted
            
            if i > 0 and hist_list[i] < hist_list[i-1]:
                is_sorted = False
                break
            else:
                is_sorted = True

        if not is_sorted:                                       # hist_list is not sorted, so we shuffle it again anc resart the function
            shuffle_mainlist(hist_list, colored_dict)               # shuffle list to "sort" it
            
            update_canvas_display(hist_list,force_update=True)      # update the canvas


    globals.moves_queue.put(("finished",))       # hist_list is sorted, so we exit the function
    return