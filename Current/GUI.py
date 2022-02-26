from tkinter import *
import tkinter
from PIL import ImageTk, Image
import ray_trace
from sphere import sphere
import numpy as np
from texture import texture



def refresh_image():
    
    t.render()

    i = Image.open("Current\image.png")
    display = ImageTk.PhotoImage(i, master=root)
    rendered_shapes.configure(image = display)
    rendered_shapes.image = display

def add_sphere():
    s = sphere( np.array([float(ex.get()), float(ey.get()), float(ez.get())]), float(era.get()), texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) )
    t.objects.append(s)
    refresh_image()
            # objects = [
        #     sphere( np.array([0.1, -0.3, 0]), 0.1, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) ),
        #     sphere( np.array([-0.2, 0, -1]), 0.7, texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 )),
        #     sphere( np.array([-0.3, 0, 0]), 0.15, texture(np.array([0, 0.1, 0]), np.array([0, 0.6, 0]), np.array([1, 1, 1]), 100, 0.5 )),
        #     sphere( np.array([0, -9000, 0]), 9000 - 0.7, texture(np.array([0.1, 0.1, 0.1]), np.array([0.6, 0.6, 0.6]), np.array([1, 1, 1]), 100, 0.5 ))
        #     [triangle(np.array([-0.2, 0, -1]),np.array([0.2, 0, -1]),np.array([0, 1, -1]),texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 ))]
        #] 




t = ray_trace.tracer()
root = tkinter.Tk()  
i = Image.open("Current\image.png")
display = ImageTk.PhotoImage(i, master=root)
rendered_shapes = tkinter.Label(root, image=display)
rendered_shapes.grid(row=0)

btn_refresh = tkinter.Button(root, text='Refresh',width= 25, command=refresh_image)
btn_refresh.grid(row=5, column = 0)
#refresh.pack( side = BOTTOM)

btn_new_sphere = tkinter.Button(root, text= 'new sphere', width = 25, command=add_sphere)

btn_new_sphere.grid(row=5, column = 1)
#new_sphere.pack(side = BOTTOM)

Label(root, text = 'x coordinate.').grid(row=1)
Label(root, text = 'y coordinate.').grid(row=2)
Label(root, text = 'z coordinate.').grid(row=3)
Label(root, text = 'THE ERA.').grid(row=4)

ex = Entry(root)
ey = Entry(root)
ez = Entry(root)
era = Entry(root)

ex.grid(row = 1, column = 1)
ey.grid(row = 2, column = 1)
ez.grid(row = 3, column = 1)
era.grid(row = 4, column = 1)


root.mainloop()
