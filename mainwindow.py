from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
import pydicom

from tagdisplay import *
from imagedisplay import *
from buttonsave import *

class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.image = None
        self.photo = None
        self.canvas = None        

        self.tagdisplay = None
        self.imageDisplay = None                            
        self.buttonsave = None

        self.init_ui()

    def init_ui(self):
        self.parent.title("DICOM TAG EDITOR")
        self.init_toolbar()
        
        self.frameLeft = Frame(self.parent, width=512,height=700)
        self.frameLeft.pack(side=LEFT, expand=1)                
        self.frameRight = Frame(self.parent, width=550,height=700)
        self.frameRight.pack(side=LEFT, expand=1)     

        # DICOM TAG Panel       
        self.tagdisplay = TagDisplay(self.frameRight)        
        # IMAGE
        self.imageDisplay = ImageDisplay(self.frameLeft)       
        # Button Save
        self.buttonsave = ButtonSave(self.frameRight)

    def init_toolbar(self):
        # Top level menu
        menubar = Menu(self.parent, bd=0)
        self.parent.config(menu=menubar, bd=0)

        # "File" menu
        filemenu = Menu(menubar, tearoff=False, bd=0)  # tearoff False removes the dashed line
        menubar.add_cascade(label="File", menu=filemenu)        
        filemenu.add_command(label="Open...", command=self.on_open)                      

    def on_open(self):
        filename =  askopenfilename(title = "Select DICOM file",filetypes=(("All files", "*.*"),
                                                     ("DICOM files", "*.dcm")))                
        dataset = pydicom.dcmread(filename)

        self.tagdisplay.showDicomTag(dataset)
        self.imageDisplay.showImage(dataset)
        self.buttonsave.setDataset(dataset)
        self.buttonsave.setDcmFileNameToEdit(filename)
        self.buttonsave.setButSaveVisible()

    
