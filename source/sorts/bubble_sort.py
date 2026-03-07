from classes import Histogram
import globals

""" bubble sort is sorting an array by comparing each object inside the array to the next,
    putting the biggest behind and so on.
        average complexity O(n²) | best case  O(n) | worst case O(n²)"""

def bubblesort(hist_list:list[Histogram]):
    global moves_queue, stop_sorting_flag

    n = len(hist_list)
    for i in range(n-1):
        for j in range(n-i-1):
        
            if globals.stop_sorting_flag.is_set():
                print("stopping")
                return


            globals.moves_queue.put(("compare", j, j+1))        # marking object n°j and j+1 as compared

            if hist_list[j].value > hist_list[j+1].value:                   # comparing object n°j and j+1
                hist_list[j], hist_list[j+1] = hist_list[j+1], hist_list[j] # swaping object n°j and j+1


                globals.moves_queue.put(("swap", j, j+1))       # marking object n°j and j+1 as swaped


    globals.moves_queue.put(("finished",))                      # marking sorting as finished
    return