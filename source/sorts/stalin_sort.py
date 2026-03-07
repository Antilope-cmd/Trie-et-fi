from classes import Histogram
from utils import update_canvas_display

""" staline sort is sorting an array by onli keeping what is already sorted in the list
        best, average and worst case O(n)"""


def stalinsort(hist_list:list[Histogram], moves_queue:Queue):
    i = 1
    while i < len(hist_list):                           # as long as we don't have reach the last histogram of the array
        
        moves_list.put(("compare", i, i-1))                 # mark the histogram as compared
        
        if hist_list[i].value < hist_list[i-1].value:           # compare the current and the previous histogram
            hist_list.pop(i)                                    # get rid of hist_list[i] if < to hist_list[i-1]
            update_canvas_display(hist_list,force_update=True)  # update the canvas
        
        else:
            i += 1                      # increment i to mark object n°i as sorted
    
    
    moves_queue.append(("finished",))   # marking sorting as finished
    return 