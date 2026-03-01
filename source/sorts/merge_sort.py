from classes import Histogram
from queue import Queue


#Launch function, only used in recursive functions to signal to the GUI when to finish the sort;
#as putting the finish inside the body of the funtion would call it everytime the function returns
#This is the function we pass to the program
def merge_sort(hist_list:list[Histogram], movesqueue:Queue[tuple]):
    mergesort(hist_list, movesqueue)
    movesqueue.put(("finished",))
    return


def merge(left:list[Histogram], right:list[Histogram], start_of_segment, movesqueue:Queue[tuple]):
    merged = []
    i = 0; j = 0
    k = start_of_segment #Tracks the original indecies in the main list.
    len_left, len_right = len(left), len(right)

    while i < len_left and j < len_right:

        #We COULD optimize these additions in the comparison by writing everything in function of k (since its initialised at start_of_sergment)
        #But it isn't worth losing in readability and doesn't even gain that much perf.
        movesqueue.put(("compare", start_of_segment + i, start_of_segment + len_left + j))

        if left[i].value < right[j].value:
            merged.append(left[i])
            #Because we tracked the start of the segment in the main list with k, we know where the overwrite needs to happen
            movesqueue.put(("set", k, left[i].value))

            i += 1

        else:
            merged.append(right[j])
            movesqueue.put(("set", k, right[j].value))

            j += 1

        k += 1 #Always increment k ko follow the merging in the Gui

    while i < len_left:
        merged.append(left[i])
        movesqueue.put(("set", k, left[i].value))

        i += 1
        k += 1

    while j < len_right:
        merged.append(right[j])
        movesqueue.put(("set", k, right[j].value))

        j += 1
        k += 1

    return merged

#Really, the algorithm is the same, only thing is we track the index of the changes while in sub arrays (to know where the changes are happening)
def mergesort(hist_list:list[Histogram], movesqueue:Queue[tuple], start_of_segment=0):

    n = len(hist_list)

    if n <= 1:
        return hist_list
    
    middle = n//2
    left = mergesort(
                    hist_list[:middle], movesqueue, 

                    #Need to keep original indexing, to tell the Gui where to change objects
                    start_of_segment=start_of_segment,
                    )
    right = mergesort(
                    hist_list[middle:], movesqueue,

                    #(middle + start) gives us the starting index of the right array in the main list
                    start_of_segment= middle + start_of_segment
                    )


    return merge(left, right, start_of_segment, movesqueue=movesqueue)


