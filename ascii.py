from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import PIL
from PIL import Image, ImageDraw, ImageGrab
import os 
from colorutils import Color
import time

name = ''
savename = ''
convert_bool = False

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

class Paint(object):

    DEFAULT_COLOR = '#000000'
    DEFAULT_CHOOSE_SIZE= 5
    DEFAULT_OPACITY = 1
    OPACITY_OBJECT_COUNTER = 0
    CURRENT_MODE = 1
    CURRENT_OBJECT = []

    def __init__(self):
        self.root = Tk()

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=2, columnspan=5)

        self.color_button = Button(self.root, text='Brush Color', command=self.choose_color).grid(row=0, column=0)

        self.canvas_button = Button(self.root, text='Background Color', command=self.background).grid(row=1, column=0)

        self.opacity_label = Label(self.root, text='Opacity').grid(row=1, column=1)
        self.opacity_button = Scale(self.root, from_= 0.00, to=1.00, orient=HORIZONTAL, resolution = .01)
        self.opacity_button.grid(row=0, column=1)
        self.opacity_button.set(self.DEFAULT_OPACITY)

        self.choose_size_label = Label(self.root, text='Thickness').grid(row=1, column=2)
        self.choose_size_button = Scale(self.root, from_=1, to=30, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=2)
        self.choose_size_button.set(self.DEFAULT_CHOOSE_SIZE)

        self.save_as_button = Button(self.root, text='Save As', command=self.save_as).grid(row=0, column=3)

        self.undo_button = Button(self.root, text='Undo', command = self.undo).grid(row=1, column=3)

        self.save_quit_button = Button(self.root, text='Convert to ASCII As', command=self.convert).grid(row=0, column=4)

        self.quit_button = Button(self.root, text='My Own Image', command=self.own_image).grid(row=1, column=4)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.back_color = "ffffff"
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    def background(self):
        self.back_color = askcolor(color=self.color)[1]
        self.c.create_rectangle((-10, -10, 1000, 1000),fill=self.back_color)
        self.CURRENT_OBJECT.append(max(self.c.find_all())-1)

    def paint(self, event):
        if self.CURRENT_MODE:
            if len(self.c.find_all()):
                self.CURRENT_OBJECT.append(max(self.c.find_all()))
            else:
                self.CURRENT_OBJECT = [0]
        self.CURRENT_MODE = 0
        ids = self.c.find_overlapping(event.x,event.y,event.x,event.y)
        if len(ids)>0:
            index = 0
            for i in ids:
                if i<self.OPACITY_OBJECT_COUNTER:
                    index = i
            if index:
                color = self.c.itemcget(index, "fill")
            else:
                color = "#ffffff"
        else:
            color = "#ffffff"
        bg_color = hex_to_rgb(str(color))
        paint_color = hex_to_rgb(self.color)
        combined_color =   (int(paint_color[0]*self.opacity_button.get()+bg_color[0]*(1-self.opacity_button.get())),
                            int(paint_color[1]*self.opacity_button.get()+bg_color[1]*(1-self.opacity_button.get())),
                            int(paint_color[2]*self.opacity_button.get()+bg_color[2]*(1-self.opacity_button.get())))
        final_color = rgb_to_hex(combined_color)

        self.line_width = self.choose_size_button.get()
        if self.old_x and self.old_y:
            self.c.create_line((self.old_x, self.old_y, event.x, event.y),
                               width=self.line_width, fill=final_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        if len(self.c.find_all()):
            self.OPACITY_OBJECT_COUNTER = max(self.c.find_all())
        self.CURRENT_MODE = 1

    def undo(self):
        if self.CURRENT_OBJECT != []:
            for i in range(self.CURRENT_OBJECT[-1]+1,max(self.c.find_all())+1):
                self.c.delete(i)
            self.CURRENT_OBJECT = self.CURRENT_OBJECT[:-1]

    def convert(self):
        global savename, convert_bool
        convert_bool = True
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        height = self.root.winfo_height() + y
        width = self.root.winfo_width() + x
        ImageGrab.grab().crop((x+3, y+70, width-3, height-64)).save(str(os.getcwd())+"/Masterpiece_Unga_bunga_don't_use_this_name.png")
        savename = filedialog.asksaveasfile(defaultextension = ".txt", filetypes = [("TXT file", "*.txt")])
        if savename:
            self.root.destroy()
    
    def save_as(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        height = self.root.winfo_height() + y
        width = self.root.winfo_width() + x
        name = filedialog.asksaveasfile(defaultextension = ".png", filetypes = [("PNG file", "*.png")])
        self.root.update()
        ImageGrab.grab().crop((x+3, y+70, width-3, height-64)).save(name.name)

    def own_image(self):
        global name, convert_bool, savename
        name = filedialog.askopenfilename()
        if name:
            convert_bool = True
            savename = filedialog.asksaveasfile(defaultextension = ".txt", filetypes = [("TXT file", "*.txt")])
            self.root.destroy()


Paint()

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)

def grayscale(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)

def main(new_width=100):
    if name:
        path = name
    else:
        path = str(os.getcwd())+"/Masterpiece_Unga_bunga_don't_use_this_name.png"
    try:
        image = Image.open(path)
    except:
        print(path, "is not a valid pathname to an image.")
    new_image_data = pixels_to_ascii(grayscale(resize_image(image,new_width = new_width)))

    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    print(ascii_image)

    with open(savename.name, "w") as fp:
        fp.write(ascii_image)

if convert_bool:
    main(200)
    if os.path.exists(str(os.getcwd())+"/Masterpiece_Unga_bunga_don't_use_this_name.png"):
        os.remove(str(os.getcwd())+"/Masterpiece_Unga_bunga_don't_use_this_name.png")
