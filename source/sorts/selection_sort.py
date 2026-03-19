from classes import Histogram
import globals

""" selection sort is sorting an array by cycling throw it and finding the smallest histogram,
    then reducing the size of the array by ignoring what suposed to be already sorted
        average complexity O(n²) | best case  O(n²) | worst case O(n²)"""

def selectionsort(hist_list:list[Histogram]):
    n = len(hist_list)

    for i in range(n):
        min = float("inf")
        min_index = i

        for j in range(i, n):
        
            if globals.stop_sorting_flag.is_set():
                return

            globals.moves_queue.put(("compare", j, min_index))  # mark object n°j and min_index as compared
            

            if hist_list[j].value < min:                # compare value of object n°j and min
                min = hist_list[j].value                    # change value of min
                min_index = j                               # change min_index for the index of the new min



    
        globals.moves_queue.put(("swap", i, min_index))         # marking object n°i and min_index as swaped
        hist_list[min_index], hist_list[i] = hist_list[i], hist_list[min_index] # swaping object n°i and min_index

    globals.moves_queue.put(("finished",))                      # marking sorting as finished
    return