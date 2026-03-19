# import tkinter as tk
# from main import mainlist, root

# class tableau():
#     def __init__(self):
#         tab = [i.value for i in mainlist]

# canva_size = len(mainlist) * 2
# def user_window():
#     user_lists_window = tk.Toplevel().wm_resizable(width= canva_size, height= canva_size + 20).wm_resizable(canva_size, canva_size + 20)
#     mini_canvas = tk.Canvas(user_list_win, width= canva_size, height=canva_size)
#     submit_button = tk.Button(user_list_win, text='Submit', command=submit(), height= 20)

# def submit():



import tkinter as tk
from main import array_size, mainlist, canvas

def Mousecoords(event):
    if array_size < canvas.winfo_width():
        index = event.x % array_size
    elif array_size > canvas.winfo_width():
        ind_approx = array_size / canvas.winfo_width()
        ind_start = event.x * ind_approx
        index = [ind_start + i for i in range(ind_approx)]
    
    pointxy = (event.x, event.y) # get the mouse position from event
    print(pointxy)

    return index


root = tk.Tk()
can = tk.Canvas(root, bg='blue')
can.pack(fill="both", expand=True)


can.bind('<B1-Motion>', Mousecoords)

root.mainloop()