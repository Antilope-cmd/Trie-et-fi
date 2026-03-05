from classes import Histogram
import globals

def bubblesort(hist_list:list[Histogram]):
    global moves_queue, stop_sorting_flag

    n = len(hist_list)
    for i in range(n-1):
        for j in range(n-i-1):
        
            if globals.stop_sorting_flag.is_set():
                print("stopping")
                return


            globals.moves_queue.put(("compare", j, j+1))

            if hist_list[j].value > hist_list[j+1].value:
                hist_list[j], hist_list[j+1] = hist_list[j+1], hist_list[j]


                globals.moves_queue.put(("swap", j, j+1))


    globals.moves_queue.put(("finished",))
    return