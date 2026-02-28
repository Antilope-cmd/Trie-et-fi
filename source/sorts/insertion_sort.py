from classes import Histogram
from queue import Queue


def insertionsort(hist_list:list[Histogram], moves_list:Queue[tuple]):
    copy = hist_list.copy()
    n = len(copy)
    for i in range(1, n):
        j = i

        while j > 0 and copy[j].value < copy[j-1].value:
            moves_list.put(("compare", j, j-1))
            moves_list.put(("swap", j, j-1))
            copy[j], copy[j-1] = copy[j-1], copy[j]
            j -= 1
    
    moves_list.put(("finished",))
    return