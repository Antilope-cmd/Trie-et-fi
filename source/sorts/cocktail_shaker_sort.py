from classes import Histogram
import globals

def cocktailshaker_sort(hist_list:list[Histogram]):
    n = len(hist_list)

    for i in range(n//2):
        swapped = False

        #First pass
        for j in range(i, n-i-1):
            
            globals.moves_queue.put(("compare", j, j+1))
            if hist_list[j].value > hist_list[j+1].value:

                globals.moves_queue.put(("swap", j, j+1))
                hist_list[j+1], hist_list[j] = hist_list[j], hist_list[j+1]
                swapped = True
        
        if not swapped:
            break
        #Reverse pass
        for j in range(n-i-2, i, -1):

            globals.moves_queue.put(("compare", j, j-1))
            if hist_list[j].value < hist_list[j-1].value:

                globals.moves_queue.put(("swap", j, j-1))
                hist_list[j-1], hist_list[j] = hist_list[j], hist_list[j-1]
    
    globals.moves_queue.put(("finished",))

    return