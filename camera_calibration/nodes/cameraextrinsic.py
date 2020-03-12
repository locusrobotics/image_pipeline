from Tkinter import *
import PIL.Image, PIL.ImageTk
import threading
import time


class KeySelectThread(threading.Thread):
    """
    Thread that displays the current images
    And provide the UI for key point selection
    """
    def __init__(self, queue, opencv_calibration_node):
        threading.Thread.__init__(self)
        self.queue = queue
        self.opencv_calibration_node = opencv_calibration_node
        self.foundImage = False
    def run(self):
             
        # wait for an image (could happen at the very beginning when the queue is still empty)
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)
        self.updateDisplay()
        self.but1 = Button(self.root, text="press me", command=lambda: self.changeImg())
        self.but1.pack()

        self.root.mainloop()
    def configure(self,event):
        w, h = event.width, event.height
        #print("congiure event (w={}, h={})".format(w, h))
        self.image = self.image.resize((w, h), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(image=self.image)
        self.canvas.itemconfig(self.imgArea, image = self.photo )
        
    def updateDisplay(self):
        while len(self.queue) == 0:
            time.sleep(0.1)

        if self.foundImage == False:            
            height, width, _ = self.queue[0].shape
            self.canvas = Canvas(self.frame, width = width, height = height, bd=0, highlightthickness=0)            
            self.canvas.pack(fill=BOTH, expand=YES)
            #self.canvas.addtag_all("all")
            self.image  = PIL.Image.fromarray(self.queue[0])
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.imgArea = self.canvas.create_image(0, 0, anchor = NW, image = self.photo)
            self.canvas.bind("<Configure>", self.configure)
            self.foundImage = True
        else:
            self.image  = PIL.Image.fromarray(self.queue[0])
            width = self.frame.winfo_width()
            height = self.frame.winfo_height()
            self.image = self.image.resize((width, height), PIL.Image.ANTIALIAS)
            self.photo = PIL.ImageTk.PhotoImage(image = self.image)
            self.canvas.itemconfig(self.imgArea, image = self.photo )
            
        self.canvas.after(100, self.updateDisplay) # call itself to implement the timer function
        
    def changeImg(self):
        pass
