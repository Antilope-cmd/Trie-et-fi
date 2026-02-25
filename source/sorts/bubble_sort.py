from classes import Histogram
from utils import update_canvas_display


def bubblesort(hist_list:list[Histogram]):
    n = len(hist_list)
    for i in range(n-1):
        for j in range(n-i-1):
            
            yield "compare", j, j+1
            yield 'clearcolor', 'red'
        

            if hist_list[j].value > hist_list[j+1].value:
                hist_list[j], hist_list[j+1] = hist_list[j+1], hist_list[j]

                yield "swap", j, j+1
                yield 'clearcolor', 'blue'

        yield "delay"

    yield "finished",