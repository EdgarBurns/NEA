from tkinter import *
from PIL import ImageTk, Image
from numpy.lib.polynomial import roots
import ray_trace
from sphere import sphere
import numpy as np
from texture import texture
from triangle import triangle


def refresh_image():
    
    t.render()

    i = Image.open("Current\image.png")
    display = ImageTk.PhotoImage(i, master=root)
    rendered_shapes.configure(image = display)
    rendered_shapes.image = display

def add_sphere():
    s = sphere( np.array([float(esx.get()), float(esy.get()), float(esz.get())]), float(esra.get()), texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) )
    t.objects.append(s)
    refresh_image()
            # objects = [
        #     sphere( np.array([0.1, -0.3, 0]), 0.1, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) ),
        #     sphere( np.array([-0.2, 0, -1]), 0.7, texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 )),
        #     sphere( np.array([-0.3, 0, 0]), 0.15, texture(np.array([0, 0.1, 0]), np.array([0, 0.6, 0]), np.array([1, 1, 1]), 100, 0.5 )),
        #     sphere( np.array([0, -9000, 0]), 9000 - 0.7, texture(np.array([0.1, 0.1, 0.1]), np.array([0.6, 0.6, 0.6]), np.array([1, 1, 1]), 100, 0.5 ))
            
        #]
def add_triangle():
    point1 = np.array([float(etv01.get()), float(etv02.get()), float(etv03.get())]) 
    point2 = np.array([float(etv11.get()), float(etv12.get()), float(etv13.get())])
    point3 = np.array([float(etv21.get()), float(etv22.get()), float(etv23.get())])
    
    tri = triangle( point1, point2, point3, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1,1,1]), 100, 0.5 ) )

    t.objects.append(tri)
    refresh_image()

t = ray_trace.tracer()
root = Tk()  
i = Image.open("Current\image.png")
display = ImageTk.PhotoImage(i, master=root)
rendered_shapes = Label(root, image=display)
rendered_shapes.grid(row=0)

btn_refresh = Button(root, text='Refresh',width= 25, command=refresh_image)
btn_refresh.grid(row=14, column = 0)
#refresh.pack( side = BOTTOM)

btn_new_sphere = Button(root, text= 'new sphere', width = 25, command=add_sphere)

btn_new_sphere.grid(row=14, column = 1)
#new_sphere.pack(side = BOTTOM)
btn_new_triangle = Button(root, text= 'new triangle', width = 25, command=add_triangle)

btn_new_triangle.grid(row=14, column = 2)

Label(root, text = 'x coordinate.').grid(row=1)
Label(root, text = 'y coordinate.').grid(row=2)
Label(root, text = 'z coordinate.').grid(row=3)
Label(root, text = 'The radius.').grid(row=4)
Label(root, text = 'Verticie 1 x').grid(row=5)
Label(root, text = 'Verticie 1 y ').grid(row=6)
Label(root, text = 'Verticie 1 z').grid(row=7)
Label(root, text = 'Verticie 2 x').grid(row=8)
Label(root, text = 'Verticie 2 y').grid(row=9)
Label(root, text = 'Verticie 2 z').grid(row=10)
Label(root, text = 'Verticie 3 x').grid(row=11)
Label(root, text = 'Verticie 3 y').grid(row=12)
Label(root, text = 'Verticie 3 x').grid(row=13)

esx = Entry(root)
esy = Entry(root)
esz = Entry(root)
esra = Entry(root)
etv01 = Entry(root)
etv02 = Entry(root)
etv03 = Entry(root)
etv11 = Entry(root)
etv12 = Entry(root)
etv13 = Entry(root)
etv21 = Entry(root)
etv22 = Entry(root)
etv23 = Entry(root)

esx.grid(row = 1, column = 1)
esy.grid(row = 2, column = 1)
esz.grid(row = 3, column = 1)
esra.grid(row = 4, column = 1)
etv01.grid(row = 5, column = 1)
etv02.grid(row = 6, column = 1)
etv03.grid(row = 7, column = 1)
etv11.grid(row = 8, column = 1)
etv12.grid(row = 9, column = 1)
etv13.grid(row = 10, column = 1)
etv21.grid(row = 11, column = 1)
etv22.grid(row = 12, column = 1)
etv23.grid(row = 13, column = 1)

root.mainloop()
