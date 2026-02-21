import io
import tkinter as tk
from tkinter import colorchooser
from turtle import color
from PIL import Image, ImageGrab, ImageTk
canvas_image_ref = None
x = 0
y = 0
root = tk.Tk()
root.title("Mini Paint (Pencil + Eraser)")

def choose_pencil_color():
    pencil_color = colorchooser.askcolor(title="Choose Pencil Color")
    if pencil_color[1] is not None:
        PENCIL_COLOR_BUTTON.config(bg=pencil_color[1])

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
tk.Radiobutton(left_panel, text="Bucket", variable=tool, value=3).pack(anchor=tk.W, padx=8, pady=4)


PENCIL_COLOR_BUTTON = tk.Button(left_panel, text="Choose Color", command=choose_pencil_color)
PENCIL_COLOR_BUTTON.pack(padx=8, pady=4)

ERASER_COLOR = "white"
pencil_size_scale = tk.Scale(left_panel, from_=1, to=20, label="Pencil Size", orient=tk.HORIZONTAL)
pencil_size_scale.set(3)
pencil_size_scale.pack(padx=8, pady=4)

eraser_size_scale = tk.Scale(left_panel, from_=1, to=50, label="Eraser Size", orient=tk.HORIZONTAL)
eraser_size_scale.set(14)
eraser_size_scale.pack(padx=8, pady=4)


last_x = None
last_y = None


def current_style():
    if tool.get() == 2:  # eraser
        return canvas["bg"], eraser_size_scale.get()
    return PENCIL_COLOR_BUTTON.cget("bg"), pencil_size_scale.get()



def on_mouse_down(event):

    global last_x, last_y
    if tool.get() == 3:
        bucket_fill(event.x, event.y)
        return
    last_x, last_y = event.x, event.y
def on_mouse_drag(event):

    global last_x, last_y


    if last_x is None or last_y is None:
        last_x, last_y = event.x, event.y
        return

    color, size = current_style()

    print("DEBUG color=", repr(color), type(color), " size=", size, type(size))


    canvas.create_line(
        last_x, last_y, event.x, event.y,
        fill=color,
        width=size,
        capstyle=tk.ROUND,
        smooth=True
    )


    last_x, last_y = event.x, event.y


from PIL import Image, ImageDraw, ImageTk
import io

# Keep a reference so the image isn't garbage collected
canvas_image_ref = None

def get_canvas_image():
    canvas.update()
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    return ImageGrab.grab(bbox=(x, y, x + w, y + h)).convert("RGB")

def pil_flood_fill(image, x, y, replacement_color):
    """BFS flood fill on a PIL image."""
    width, height = image.size
    target_color = image.getpixel((x, y))
    
    # Convert hex color like "#ff0000" to RGB tuple
    if isinstance(replacement_color, str):
        replacement_color = tuple(int(replacement_color[i:i+2], 16) for i in (1, 3, 5))
    
    if target_color == replacement_color:
        return image

    pixels = image.load()
    queue = [(x, y)]
    visited = set()
    
    while queue:
        cx, cy = queue.pop()
        if (cx, cy) in visited:
            continue
        if cx < 0 or cy < 0 or cx >= width or cy >= height:
            continue
        if pixels[cx, cy] != target_color:
            continue
        
        visited.add((cx, cy))
        pixels[cx, cy] = replacement_color
        
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))
    
    return image

def bucket_fill(x, y):
    global canvas_image_ref
    
    color = PENCIL_COLOR_BUTTON.cget("bg")
    
    # Get current canvas as image
    img = get_canvas_image()
    
    # Clamp coords to image bounds (canvas coords should match but just in case)
    x = max(0, min(x, img.width - 1))
    y = max(0, min(y, img.height - 1))
    
    # Run flood fill
    filled = pil_flood_fill(img, x, y, color)
    
    # Convert back to PhotoImage and draw on canvas
    photo = ImageTk.PhotoImage(filled)
    canvas_image_ref = photo  # Prevent garbage collection
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)


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
