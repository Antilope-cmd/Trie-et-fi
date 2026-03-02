from classes import Histogram
from queue import Queue

""" optimized selection sort is sorting an array by cycling throw it and finding the smallest + biggest histogram,
    then reducing the size of the array by ignoring what suposed to be already sorted
        average complexity O(n²) | best case  O(n²) | worst case O(n²)"""


def optimized_selectionsort(hist_list:list[Histogram], moves_queue:Queue[tuple]):
    n = len(hist_list)
    
    for i in range(n//2):
        min_val = float("inf")
        min_index = i

        max_val = float("-inf") #Finding both min and max allows 2 times less iterations over the array
        max_index = i

        for j in range(i, n-i):
        

            moves_queue.put(("compare", j, min_index))  # mark object n°j and min_index as compared
            

            if hist_list[j].value < min_val:            # compare value of object n°j and min_val
                min_val = hist_list[j].value                # change value of min_val
                min_index = j                               # change min_index for the index of the new min_val
            if hist_list[j].value > max_val:            # compare value of object n°j and man_val
                max_val = hist_list[j].value                # change value of man_val
                max_index = j                               # change min_index for the index of the new man_val



    

        moves_queue.put(("swap", i, min_index))         # marking object n°i and min_index as swaped
        hist_list[min_index], hist_list[i] = hist_list[i], hist_list[min_index]         # swaping object n°i and min_index


        if max_index == i:          # to avoid swaping object on the last cycle
            max_index = min_index


        moves_queue.put(("swap", n-i-1, max_index))     # marking object n°n-i-1 and max_index as swaped
        hist_list[max_index], hist_list[n-1-i] = hist_list[n-1-i], hist_list[max_index] # swaping object n°i and min_index


    moves_queue.put(("finished",))                      # marking sorting as finished
    return