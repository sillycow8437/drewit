import tkinter as tk


root = tk.Tk()
root.title("Mini Paint (Pencil + Eraser)")


tool = tk.IntVar(value=1) 


menu = tk.Menu(root)
root.config(menu=menu)

filemenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)


filemenu.add_command(label="New")
filemenu.add_command(label="Open...")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")


left_panel = tk.Frame(root)
left_panel.pack(side=tk.LEFT, fill=tk.Y)


canvas = tk.Canvas(root, width=900, height=600, bg="white", cursor="crosshair")
canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Radiobutton(left_panel, text="Pencil", variable=tool, value=1).pack(anchor=tk.W, padx=8, pady=4)
tk.Radiobutton(left_panel, text="Eraser", variable=tool, value=2).pack(anchor=tk.W, padx=8, pady=4)


PENCIL_COLOR = "black"
ERASER_COLOR = "white"  
PENCIL_SIZE = 2
ERASER_SIZE = 14

last_x = None
last_y = None


def current_style():

    if tool.get() == 2:  # Eraser
        return ERASER_COLOR, ERASER_SIZE
    else:               # Pencil (default)
        return PENCIL_COLOR, PENCIL_SIZE


def on_mouse_down(event):

    global last_x, last_y
    last_x, last_y = event.x, event.y

def on_mouse_drag(event):

    global last_x, last_y


    if last_x is None or last_y is None:
        last_x, last_y = event.x, event.y
        return

    color, size = current_style()


    canvas.create_line(
        last_x, last_y, event.x, event.y,
        fill=color,
        width=size,
        capstyle=tk.ROUND,
        smooth=True
    )


    last_x, last_y = event.x, event.y

def on_mouse_up(event):
    """
    Called when the user releases the left mouse button.
    We clear the last positions so the next stroke starts fresh.
    """
    global last_x, last_y
    last_x, last_y = None, None

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)


def new_file():
    """
    Clears everything drawn on the canvas.
    """
    canvas.delete("all")

filemenu.entryconfig("New", command=new_file)


root.mainloop()
