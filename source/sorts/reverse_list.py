from classes import Histogram
import globals

"""
This is simply a funciton to turn the list upside down.
"""


def reverselist(list_hist:list[Histogram]):
    n = len(list_hist)

    for i in range(n//2):

        if globals.stop_sorting_flag.is_set():
            return


        list_hist[i], list_hist[n-i-1] = list_hist[n-i-1], list_hist[i]
        globals.moves_queue.put(("swap", i, n-i-1))
    
    globals.moves_queue.put(("finished",))
    return