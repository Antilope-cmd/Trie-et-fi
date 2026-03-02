from classes import Histogram
from queue import Queue


def selectionsort(hist_list:list[Histogram], moves_queue:Queue[tuple]):
    n = len(hist_list)

    for i in range(n):
        min = float("inf")
        min_index = i

        for j in range(i, n):
        

            moves_queue.put(("compare", j, min_index))
            

            if hist_list[j].value < min:
                min = hist_list[j].value
                min_index = j



    
        moves_queue.put(("swap", i, min_index))
        hist_list[min_index], hist_list[i] = hist_list[i], hist_list[min_index]

    moves_queue.put(("finished",))
    return