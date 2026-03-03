from classes import Histogram
from queue import Queue

"""Quicksort stays nice and simple because it already works on the main array"""

def quick_sort(array, movequeue:Queue[tuple], stopflag):
    quicksort(hist_list=array, movequeue=movequeue, stop_flag=stopflag, start=0, end=(len(array)-1) )
    movequeue.put(("finished", ))



def partition(hist_list:list[Histogram], movequeue:Queue[tuple], start:int, end:int):
    pivot = hist_list[end]
    i = start
    
    for j in range(start, end):

        movequeue.put(("compare", j, end))

        if hist_list[j].value < pivot.value:

            hist_list[i], hist_list[j] = hist_list[j], hist_list[i]
            movequeue.put(("swap", i, j))

            i += 1
    
    movequeue.put(("swap", i, end))
    hist_list[i], hist_list[end] = hist_list[end], hist_list[i]

    return i

def quicksort(hist_list:list[Histogram], movequeue:Queue[tuple], start, end, stop_flag):
    
    if stop_flag.is_set():
        return

    if end <= start:
        return

    pivot = partition(hist_list=hist_list, movequeue=movequeue, start=start, end=end)

    quicksort(hist_list=hist_list, movequeue=movequeue, stop_flag=stop_flag, start=start, end=pivot-1)
    quicksort(hist_list=hist_list, movequeue=movequeue, stop_flag=stop_flag, start=pivot+1, end=end)

    return