from classes import Histogram


def optimized_selectionsort(hist_list:list[Histogram], moves_queue:list):
    copy = hist_list.copy()
    n = len(copy)
    
    for i in range(n//2):
        min_val = float("inf")
        min_index = i

        max_val = float("-inf")
        max_index = i

        for j in range(i, n-i):
        

            moves_queue.append(("compare", j, min_index))
            

            if copy[j].value < min_val:
                min_val = copy[j].value
                min_index = j
            if copy[j].value > max_val:
                max_val = copy[j].value
                max_index = j



    

        moves_queue.append(("swap", i, min_index))
        copy[min_index], copy[i] = copy[i], copy[min_index]


        if max_index == i:
            max_index = min_index


        moves_queue.append(("swap", n-i-1, max_index))
        copy[max_index], copy[n-1-i] = copy[n-1-i], copy[max_index]


    moves_queue.append(("finished",))
    return