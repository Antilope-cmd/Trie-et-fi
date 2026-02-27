from classes import Histogram
from queue import Queue


def selectionsort(hist_list:list[Histogram], moves_queue:Queue[tuple]):
    copy = hist_list.copy()
    n = len(copy)

    for i in range(n):
        min = float("inf")
        min_index = i

        for j in range(i, n):
        

            moves_queue.put(("compare", j, min_index))
            

            if copy[j].value < min:
                min = copy[j].value
                min_index = j



    
        moves_queue.put(("swap", i, min_index))
        copy[min_index], copy[i] = copy[i], copy[min_index]

    moves_queue.put(("finished",))
    return