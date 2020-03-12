import rospy
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
        #NoDefaultRoot()
        # this is the main root for feature selection
        self.root = Tk()
        
        self.root.bind("<Key>", self.handle_key_event)
        self.root.title("Extrinsic Calibration")
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)
        self.updateDisplay()
        
        # this is the editor for key selection and display
        self.editor=KeySelectEditor(self.root)
        # main tkinter loop, there is no need to run two main loop, because main loop won't return
        self.root.mainloop()
        
    def handle_key_event(self, event):
        if event.char == 'q':
            rospy.signal_shutdown('Quit')
        
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
            self.canvas.bind("<Button-1>", self.on_mouse_click)           
            self.canvas.pack(fill=BOTH, expand=YES)
            
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
    def on_mouse_click(self, event):
        print("clicked at (x={}, y={})".format(event.x, event.y) )
        self.editor.insertItem(','.join([str(event.x), str(event.y)]) )
        
        
    def changeImg(self):
        pass
    
class KeySelectEditor:
    def __init__(self, master):
        self.root = Toplevel(master)
        self.root.title("Keypoint List")
        self.frame=Frame(self.root)
        self.keylistbox = Listbox(self.frame, selectmode=EXTENDED)
        self.keylistbox.pack(fill=BOTH, expand=1)
        self.keys=[]
        self.fill_listbox(self.keys)
        self.excalib_but = Button(self.frame, text="Start Calibration", command=lambda: self.calib_extrinsic())
        self.excalib_but.pack()
        self.frame.pack()
        
    def fill_listbox(self, keys):
        for key in keys:
            self.keylistbox.insert(END, key)        

    def insertItem(self, keypoint):
        self.keys.append(keypoint)
        self.keylistbox.insert(END, keypoint)
        
    def calib_extrinsic(self):
        pass
    