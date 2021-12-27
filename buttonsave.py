from tkinter import *
from tkinter import messagebox
from io import BytesIO
from pydicom import dcmwrite
from pydicom.filebase import DicomFileLike

class ButtonSave(Frame):
    def __init__(self, parent):
        self.dcmFileNameToEdit = None
        self.dataset = None
        self.butSave = Button(parent, text ="Modify&Save", command = self.modifyAndSave)
        
    def modifyAndSave(self):        
        dcmFileNameToEditMod = self.dcmFileNameToEdit + "._mod"

        f = open(dcmFileNameToEditMod, "wb")
        byteToWrite = self.__write_dataset_to_bytes(self.dataset)
        f.write(byteToWrite)
        f.close()

        messagebox.showinfo("Success", "Create modify DICOM at " + dcmFileNameToEditMod)
  
    def setButSaveVisible(self):        
        self.butSave.pack()

    def setDataset(self, dataset):
        self.dataset = dataset

    def setDcmFileNameToEdit(self, dcmFileNameToEdit):
        self.dcmFileNameToEdit = dcmFileNameToEdit        

    #---private method---#
    def __write_dataset_to_bytes(self, dataset):
        # create a buffer
        with BytesIO() as buffer:
            # create a DicomFileLike object that has some properties of DataSet
            memory_dataset = DicomFileLike(buffer)
            # write the dataset to the DicomFileLike object
            dcmwrite(memory_dataset, dataset)
            # to read from the object, you have to rewind it
            memory_dataset.seek(0)
            # read the contents as bytes
            return memory_dataset.read()