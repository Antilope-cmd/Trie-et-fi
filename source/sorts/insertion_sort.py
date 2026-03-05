from classes import Histogram
import globals

def insertionsort(hist_list:list[Histogram]):
    n = len(hist_list)
    for i in range(1, n):
        j = i

        while j > 0 and hist_list[j].value < hist_list[j-1].value:

            if globals.stop_sorting_flag.is_set():
                return


            globals.moves_queue.put(("compare", j, j-1))
            globals.moves_queue.put(("swap", j, j-1))
            hist_list[j], hist_list[j-1] = hist_list[j-1], hist_list[j]
            j -= 1
    
    globals.moves_queue.put(("finished",))
    return