from classes import Histogram
from queue import Queue

def bubblesort(hist_list:list[Histogram], moves_queue:Queue):
    copy = hist_list.copy()
    n = len(copy)
    for i in range(n-1):
        for j in range(n-i-1):
        
            moves_queue.put(("compare", j, j+1))

            if copy[j].value > copy[j+1].value:
                copy[j], copy[j+1] = copy[j+1], copy[j]


                #yield "swap", j, j+1
                moves_queue.put(("swap", j, j+1))


    #yield "finished"
    moves_queue.put(("finished",))
    return