from classes import Histogram
from queue import Queue

def bubblesort(hist_list:list[Histogram], moves_queue:Queue, stop_flag):
    n = len(hist_list)
    for i in range(n-1):
        for j in range(n-i-1):
        
            if stop_flag.is_set():
                return


            moves_queue.put(("compare", j, j+1))

            if hist_list[j].value > hist_list[j+1].value:
                hist_list[j], hist_list[j+1] = hist_list[j+1], hist_list[j]


                moves_queue.put(("swap", j, j+1))


    moves_queue.put(("finished",))
    return