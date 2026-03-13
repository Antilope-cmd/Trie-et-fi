"""
Custom library which allows for compatible sorting algorithms
"""
from .bubble_sort import bubblesort
from .cocktail_shaker_sort import cocktailshaker_sort
from .selection_sort import selectionsort
from .insertion_sort import insertionsort
from .optimized_selection_sort import optimized_selectionsort
from .merge_sort import merge_sort
from .quick_sort import quick_sort
from .reverse_list import reverselist


sorts_dict = {
    "Bubble sort" : bubblesort,
    "Coktail shaker sort" : cocktailshaker_sort,
    "Selection sort" : selectionsort,
    "Optimized selection sort" : optimized_selectionsort,
    "Insertion sort" : insertionsort,
    "Merge sort" : merge_sort,
    "Quick sort" : quick_sort,
    "Reverse list" : reverselist
    }