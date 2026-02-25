from classes import Histogram


def bubblesort(hist_list:list[Histogram], moves_queue:list):
    copy = hist_list.copy()
    n = len(copy)
    for i in range(n-1):
        for j in range(n-i-1):
        
            moves_queue.append(("compare", j, j+1))

            if copy[j].value > copy[j+1].value:
                copy[j], copy[j+1] = copy[j+1], copy[j]


                #yield "swap", j, j+1
                moves_queue.append(("swap", j, j+1))


    #yield "finished"
    moves_queue.append(("finished",))
    return