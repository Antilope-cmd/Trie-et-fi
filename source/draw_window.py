import tkinter as tk
def draw_graph(values_to_make: int):
    """Opens an input window where the user can draw his own graph"""

    #List that will be returned
    results_list: list = [None]

    #Initializing window
    root = tk.Tk()
    root.title("Draw a graph")

    root.columnconfigure(0, weight=3)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    canvas = tk.Canvas(master=root, background="black", width=600, height=600)
    height, width = 600, 600

    #Dictionaries that store the coordinates at each x-value
    registered_coords: dict = {}
    lines_coords: dict = {} #This is just aesthetic to connect points

    def draw_line(x1, y1, x2, y2):
        """Connect two points"""
        return canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

    def on_click(event):
        """Detects click, draws square, update values"""

        #Checking if inbounds
        if not (0 <= event.x < width and 0 <= event.y < height):
            return

        #We use a grid on the x-axis of step 6 to snap the points to.
        x = 6 * round(event.x / 6) #Snapping the point on a multiple of 6
        y = event.y #Value inputted

        #If there was already a point on the input, we delete it.
        if x in registered_coords:

            canvas.delete(registered_coords[x][0]) #Delete square

            if x - 6 in lines_coords:
                canvas.delete(lines_coords[x - 6]) #Delete line before
            if x + 6 in lines_coords:
                canvas.delete(lines_coords[x + 6]) #Delete line after

        #Drawing the rectangle
        rect = canvas.create_rectangle(x + 3, y + 3, x - 3, y - 3, fill="white")
        registered_coords[x] = (rect, y) #registering its id on canvas and value

        #Drawing line left and right
        if x - 6 in registered_coords:
            lines_coords[x - 6] = draw_line(x - 6, registered_coords[x - 6][1], x, y)
        if x + 6 in registered_coords:
            lines_coords[x + 6] = draw_line(x + 6, registered_coords[x + 6][1], x, y)

    def combine(values: list, interpolation: list[list]):
        result = []
        for i in range(len(values)):
            result.append(values[i])
            if i < len(interpolation):
                result.extend(interpolation[i])
        return result

    def get_values():
        """Retrieves and adapts the values to fit the number of values_to_make"""
        values = []
        #Sort the registered coords by the x-axis
        sorted_dict = dict(sorted(registered_coords.items()))

        #Calculate relative height
        for x in sorted_dict:
            values.append(1 - sorted_dict[x][1] / height)

        values_amount = len(values)
        if values_amount == 0:
            return [i / values_to_make for i in range(1, values_to_make + 1)]  # fallback

        #This varable tells us if we need to interpolate (make more values)
        interpolation_amount = values_to_make // values_amount
        all_interpolated_values = []

        if interpolation_amount > 1:
            #Interpolation
            for i in range(values_amount - 1):

                base_value = values[i]
                next_value = values[i + 1]
                #Steps
                dy = (next_value - base_value) / interpolation_amount
                
                #All values between x and x+1
                interpolated_values = []
                
                for j in range(1, interpolation_amount):
                    interpolated_values.append(base_value + dy * j)
                
                #Add those values back
                all_interpolated_values.append(interpolated_values)

        elif interpolation_amount <= 1:
            #Skipping values
            step = max(1, values_amount // values_to_make)

            return values[::step][:values_to_make]

        final_values = combine(values, all_interpolated_values)
        return final_values[:values_to_make]

    def end_graph():
        """Closes the graph and returns values"""
        results_list[0] = get_values()
        root.after(10, lambda: root.destroy())

    submit_button = tk.Button(
        master=root,
        command=end_graph,
        text="Submit",
        width=35,
        height=2,
        font= ("Arial", 20)
        )
    
    #Detect clicks and drag
    canvas.bind("<B1-Motion>", on_click)#Drag
    canvas.bind("<Button-1>", on_click)#Click
    
    canvas.grid(row=0, column=0)
    submit_button.grid(row=1, column=0)
    root.resizable(False, False)
    root.mainloop()

    return results_list[0] if results_list[0] is not None else [i / values_to_make for i in range(1, values_to_make + 1)] #Failsafe

if __name__ == "__main__":
    draw_graph(100)