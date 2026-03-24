from classes import Histogram
import globals
"""
Time complexity : O(n²) | Space complexity : O(1)

Selection sort scans the array, finds the minimum, and puts it at the end of the sorted part of the array.
It is the most intuitive one to understand as it is exaclty how a human would sort.
"""
def selectionsort(hist_list:list[Histogram]):
    n = len(hist_list)

    for i in range(n):
        min = float("inf")
        min_index = i

        for j in range(i, n):
        
            if globals.stop_sorting_flag.is_set():
                return

            globals.moves_queue.put(("compare", j, min_index))
            

            if hist_list[j].value < min:
                min = hist_list[j].value
                min_index = j



    
        globals.moves_queue.put(("swap", i, min_index))
        hist_list[min_index], hist_list[i] = hist_list[i], hist_list[min_index]

    globals.moves_queue.put(("finished",))
    return