from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

dark_blue = '#374956'
white = "#f4f4f5"
window_width = 500
window_height = 300
algorithm_names = ["CathmulClark", "DooSabin", "Loop", "PetersReif", "Mixed"]

app = Tk()
app.configure(bg=dark_blue)
font_size = int(window_height / 25)
normal_font = Font(family="Open Sans", size=font_size)
bigger_font = Font(family="Open Sans", size=int(font_size * 3 / 2))

def set_width(scale):
    return int(window_width * scale)

def set_height(scale):
    return int(window_height * scale)

def set_font(scale):
    return int(font_size * scale)

def validate_int(string):
    try:
        return int(string)
    except ValueError:
        messagebox.showinfo("Iterations Count", "Insert valid integer!")
        return None

def validate_filename(string):
    file_extension = string.split(".")[-1]
    if len(string) < 5:
        messagebox.showinfo("Output filename", "Filename is to short!")
        return None
    if file_extension != "off":
        messagebox.showinfo("Output filename", "Bad extension - we support only .off meshes!")
        return None
    return string
