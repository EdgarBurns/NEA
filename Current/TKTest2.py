import tkinter as tk
from PIL import ImageTk, Image

import ray_trace
import numpy as np
import time

from sphere import sphere
from texture import texture

class MainWindow:

    def __init__(self, master):

        self.tracer = ray_trace.tracer()

        self.master = master
        self.frame = tk.Frame(self.master, width=400, height=300,highlightcolor="black")

        self.buttonAddCircle = tk.Button(self.frame, text = "Add Sphere", width = 10, command = lambda: self.addShape("Sphere",'200x150'))
        self.buttonAddCircle.place(x=0,y=40)

        self.buttonAddCircle = tk.Button(self.frame, text = "Add Triangle", width = 10, command = lambda: self.addShape("Triangle",'450x150'))
        self.buttonAddCircle.place(x=100,y=40)

        self.buttonAddCircle = tk.Button(self.frame, text = "Add Plane", width = 10, command = lambda: self.addShape("Plane",'350x150'))
        self.buttonAddCircle.place(x=200,y=40)

        self.ButtonExit= tk.Button(self.frame, text = "Exit", width = 10, command = lambda: self.close_windows())
        self.ButtonExit.place(x=300,y=40)
  
        display = ImageTk.PhotoImage(Image.open("Current\image.png"), master)

        self.rendered_image = tk.Label(master, image=display)
        self.rendered_image.place(x=0, y=70)

        self.frame.pack()

    def addShape(self,shapeType, geometry):

        self.addShapeWindow = tk.Toplevel(self.master)
        self.addShapeWindow.title = shapeType
        self.addShapeWindow.geometry(geometry)

        if shapeType == "Sphere":
            self.app = ShapeSphere(self.addShapeWindow)
        elif shapeType == "Triangle":
            self.app = ShapeTriangle(self.addShapeWindow)
        elif shapeType == "Plane":
            self.app = ShapePlane(self.addShapeWindow)

        self.addShapeWindow.transient(self.master)
        self.addShapeWindow.grab_set()

        self.master.wait_window(self.addShapeWindow)

        if self.app.addShape == True:
            self.tracer.objects.append(self.app.shape)
            self.tracer.render(0)
            #time.sleep(10)
            display = ImageTk.PhotoImage(Image.open("Current\image.png"), master=self.master)
            self.rendered_image.configure(image = display)


    def close_windows(self):
        self.master.destroy()


class Point:

    def __init__(self, master, x, y, width, height, title):

        self.width = width
        self.height = height
        self.x = x
        self.y = y
        
        self.master = master
        self.frame = tk.LabelFrame(self.master,width=self.width, height=self.height, text=title)
        self.frame.place(x = self.x,y = self.y)

        self.labels = []

        self.labels.append(tk.Label(self.frame, text = 'x:'))
        self.labels.append(tk.Label(self.frame, text = 'y:'))
        self.labels.append(tk.Label(self.frame, text = 'z:'))

        self.entrys = []

        self.entrys.append(tk.Entry(self.frame, width= 10))
        self.entrys.append(tk.Entry(self.frame, width= 10))
        self.entrys.append(tk.Entry(self.frame, width= 10))

        for i in range(len(self.labels)):
            self.labels[i].place(x = 2, y = i*20)
            self.entrys[i].place(x = 50, y = i*20)

class ShapeSphere:

    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master,width=300, height=200)
        self.frame.pack()

        self.xOffset = 10

        self.labels = []

        self.labels.append(tk.Label(self.frame, text = 'x:'))
        self.labels.append(tk.Label(self.frame, text = 'y:'))
        self.labels.append(tk.Label(self.frame, text = 'z:'))
        self.labels.append(tk.Label(self.frame, text = 'Ratio'))

        self.entrys = []

        self.entrys.append(tk.Entry(self.frame, width= 10))
        self.entrys.append(tk.Entry(self.frame, width= 10))
        self.entrys.append(tk.Entry(self.frame, width= 10))
        self.entrys.append(tk.Entry(self.frame, width= 10))
    
        self.entrys[0].insert(tk.END,'-0.3')
        self.entrys[1].insert(tk.END,'0.0')
        self.entrys[2].insert(tk.END,'0.0')
        self.entrys[3].insert(tk.END,'0.1')

        for i in range(len(self.labels)):
            self.labels[i].place(x = self.xOffset, y = i*20)
            self.entrys[i].place(x = 50, y = i*20)

        self.buttonAdd = tk.Button(self.frame, text = "Add Shape", width = 10, command = lambda: self.close_windows(True))
        self.buttonAdd.place(x=self.xOffset,y=(len(self.labels) + 1)*20)

        self.ButtonCancel = tk.Button(self.frame, text = "Cancel", width = 10, command = lambda: self.close_windows(False))
        self.ButtonCancel.place(x=100,y=(len(self.labels) + 1)*20)



    def close_windows(self,addShape):

        self.addShape = addShape

        if addShape == True:
            self.a = float(self.entrys[0].get())
            self.shape = sphere(np.array([float(self.entrys[0].get()), float(self.entrys[1].get()), float(self.entrys[2].get())]), float(self.entrys[3].get()), \
                texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) )
            

        self.master.destroy()

class ShapeTriangle:

    def __init__(self, master):

        self.master = master

        self.frame = tk.Frame(self.master,width=350, height=250)
        self.frame.place(x = 1,y = 1)

        self.corners = []

        for i in range(3):
            self.corners.append(Point(self.frame, 5 + (140 * i), 2, 140, 90, "Corner " + str(i+1)))

        self.buttonAdd = tk.Button(self.frame, text = "Add Shape", width = 10, command = lambda: self.close_windows(True))
        self.buttonAdd.place(x=0,y=110)

        self.ButtonCancel = tk.Button(self.frame, text = "Cancel", width = 10, command = lambda: self.close_windows(False))
        self.ButtonCancel.place(x=100,y=110)

    def close_windows(self,addShape):

        self.addShape = addShape

        if addShape == True:
            self.shape = sphere(np.array([float(self.app.entrys[0].get()), float(self.app.entrys[1].get()), float(self.app.entrys[2].get())]), float(self.app.entrys[3].get()), \
                texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) )
        
        self.master.destroy()

class ShapePlane:

    def __init__(self, master):

        self.master = master

        self.frame = tk.Frame(self.master,width=350, height=250)
        self.frame.place(x = 1,y = 1)

        self.pointOnPlane = Point(self.frame, 2, 2, 140, 90, "Point")
        self.normal = Point(self.frame, self.pointOnPlane.width + 10, 2, 140, 90, "Normal")

        self.buttonAdd = tk.Button(self.frame, text = "Add Shape", width = 10, command = lambda: self.close_windows(True))
        self.buttonAdd.place(x=0,y=self.pointOnPlane.height + 20)

        self.ButtonCancel = tk.Button(self.frame, text = "Cancel", width = 10, command = lambda: self.close_windows(False))
        self.ButtonCancel.place(x=100,y=self.pointOnPlane.height + 20)

    def close_windows(self,addShape):

        self.addShape = addShape

        if addShape == True:
            self.shape = sphere(np.array([float(self.app.entrys[0].get()), float(self.app.entrys[1].get()), float(self.app.entrys[2].get())]), float(self.app.entrys[3].get()), \
                texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) )
        
        self.master.destroy()

def main(): 
    root = tk.Tk()
    root.title("NEA")
    root.geometry('400x500')
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()