from tkinter import *
from mainwindow import MainWindow

def main():
    root = Tk()
    root.minsize(600, 550)
    root.geometry("1062x800")
    MainWindow(root)
    
    root.mainloop()    
    
if __name__ == '__main__':
    main()