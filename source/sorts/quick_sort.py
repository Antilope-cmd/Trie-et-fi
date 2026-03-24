from classes import Histogram
import globals
from random import randint

"""
Time complexity : O(n*log(n)) | Space complexity : O(n)

Quicksort picks a pivot and put all elements lower than the pivot on its left,
and all the bigger ones on its right, before doing that recursively on the left and right.
"""




"""Quicksort stays nice and simple because it already works on the main array"""

def quick_sort(array):
    quicksort(hist_list=array, start=0, end=(len(array)-1) )
    globals.moves_queue.put(("finished", ))



def partition(hist_list:list[Histogram], start:int, end:int):
    
    #Choosing random pivot to avoid worse-case scenarios
    random_pivot_index = randint(start, end)
    
    hist_list[random_pivot_index], hist_list[end] = hist_list[end], hist_list[random_pivot_index]
    globals.moves_queue.put(("swap", random_pivot_index, end))

    pivot = hist_list[end]
    i = start
    
    for j in range(start, end):

        globals.moves_queue.put(("compare", j, end))

        if hist_list[j].value < pivot.value:

            hist_list[i], hist_list[j] = hist_list[j], hist_list[i]
            globals.moves_queue.put(("swap", i, j))

            i += 1
    
    globals.moves_queue.put(("swap", i, end))
    hist_list[i], hist_list[end] = hist_list[end], hist_list[i]

    return i

def quicksort(hist_list:list[Histogram], start, end):
    
    if globals.stop_sorting_flag.is_set():
        return

    if end <= start:
        return

    pivot = partition(hist_list=hist_list, start=start, end=end)

    quicksort(hist_list=hist_list, start=start, end=pivot-1)
    quicksort(hist_list=hist_list, start=pivot+1, end=end)

    return