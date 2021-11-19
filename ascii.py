from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import PIL
from PIL import Image, ImageDraw, ImageGrab
import os 
from colorutils import Color

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

    def __init__(self):
        self.root = Tk()

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=2, columnspan=5)

        self.image1 = PIL.Image.new('RGB', (640, 480), 'white')
        self.draw = ImageDraw.Draw(self.image1)

        self.color_button = Button(self.root, text='Color', command=self.choose_color).grid(row=0, column=0)

        self.opacity_label = Label(self.root, text='Opacity').grid(row=1, column=1)
        self.opacity_button = Scale(self.root, from_= 0.00, to=1.00, orient=HORIZONTAL, resolution = .01)
        self.opacity_button.grid(row=0, column=1)
        self.opacity_button.set(self.DEFAULT_OPACITY)

        self.choose_size_label = Label(self.root, text='Thickness').grid(row=1, column=2)
        self.choose_size_button = Scale(self.root, from_=1, to=20, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=2)
        self.choose_size_button.set(self.DEFAULT_CHOOSE_SIZE)

        self.color_button = Button(self.root, text='Save and Quit', command=self.save).grid(row=0, column=3)

        self.color_button = Button(self.root, text='Quit', command=self.quit).grid(row=0, column=4)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]



    def paint(self, event):
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

    def save(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        height = self.root.winfo_height() + y
        width = self.root.winfo_width() + x
        ImageGrab.grab().crop((x, y+64, width, height-64)).save(str(os.getcwd())+"/Masterpiece.png")
        self.root.destroy()
    
    def quit(self):
        self.root.destroy()

if __name__ == '__main__':
    Paint()
