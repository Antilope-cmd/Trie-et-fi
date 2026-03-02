from classes import Histogram
from queue import Queue

""" insertion sort is sorting an array byinserting the value selected at its place
    in the part that is already sorted.
        average complexity O(n²) | best case  O(n) | worst case O(n²)"""


def insertionsort(hist_list:list[Histogram], moves_list:Queue[tuple]):
    n = len(hist_list)
    for i in range(1, n):
        j = i

        while j > 0 and hist_list[j].value < hist_list[j-1].value:
            moves_list.put(("compare", j, j-1))
            moves_list.put(("swap", j, j-1))
            hist_list[j], hist_list[j-1] = hist_list[j-1], hist_list[j]
            j -= 1
    
    moves_list.put(("finished",))
    return