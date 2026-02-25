from classes import Histogram

def insertion_sort(hist_list:list[Histogram], moves_list:list[tuple]):
    copy = hist_list.copy()
    n = len(copy)
    for i in range(1, n):
        j = i

        while j > 0 and copy[j].value < copy[j-1].value:
            moves_list.append(("compare", j, j-1))
            moves_list.append(("swap", j, j-1))
            copy[j], copy[j-1] = copy[j-1], copy[j]
            j -= 1
    
    moves_list.append(("finished",))
    return