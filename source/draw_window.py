import tkinter as tk

values_to_make = 100

root = tk.Tk()
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

canvas = tk.Canvas(
    master=root,
    background="black",
    width=500,
    height=500
    )

height, width = 500, 500

coordinates:list[tuple] = [None for i in range(500)]

def on_click(event):
    if not (0 <= event.x < width and 0 <= event.y < height):
        return
    
    x, y  = event.x, event.y

    if coordinates[x] is not None:
        rect_id = coordinates[x][0]
        canvas.delete(rect_id)

    rect = canvas.create_rectangle(
        x-1, y-1,
        x+1, y+1,
        fill='white'
    )
    
    coordinates[x] = (rect, y/5)
    return
    
canvas.bind("<B1-Motion>", on_click)

canvas.grid(row=0, column=0)
root.mainloop()