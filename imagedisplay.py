from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ImageDisplay(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent        
        
        self.init_ui()        

    def init_ui(self):        
        print("init_ui")

    def showImage(self, dataset):
        fig = plt.figure(figsize=(5,5))
        plt.axis('off')
        plt.imshow(dataset.pixel_array, cmap= plt.cm.bone)
        
        canvas = FigureCanvasTkAgg(fig, self.parent)                
        
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)        
