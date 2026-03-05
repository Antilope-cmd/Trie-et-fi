from classes import Histogram
import globals

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