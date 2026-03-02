from classes import Histogram
from queue import Queue


def optimized_selectionsort(hist_list:list[Histogram], moves_queue:Queue[tuple]):
    n = len(hist_list)
    
    for i in range(n//2):
        min_val = float("inf")
        min_index = i

        max_val = float("-inf") #Finding both min and max allows 2 times less iterations over the array
        max_index = i

        for j in range(i, n-i):
        

            moves_queue.put(("compare", j, min_index))
            

            if hist_list[j].value < min_val:
                min_val = hist_list[j].value
                min_index = j
            if hist_list[j].value > max_val:
                max_val = hist_list[j].value
                max_index = j



    

        moves_queue.put(("swap", i, min_index))
        hist_list[min_index], hist_list[i] = hist_list[i], hist_list[min_index]


        if max_index == i:
            max_index = min_index


        moves_queue.put(("swap", n-i-1, max_index))
        hist_list[max_index], hist_list[n-1-i] = hist_list[n-1-i], hist_list[max_index]


    moves_queue.put(("finished",))
    return