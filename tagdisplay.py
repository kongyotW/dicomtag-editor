from tkinter import *
from  tkinter import ttk
class TagDisplay(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.tagTree = ttk.Treeview(parent, height = 35) # record height
        
        # scrollbars        
        self.vsb = Scrollbar(self.parent, orient="vertical", command=self.tagTree.yview)        
        self.vsb.pack(side='right', fill='y')
        
        self.hsb = Scrollbar(self.parent, orient="horizontal", command=self.tagTree.xview)
        self.hsb.pack(side='bottom', fill='x')        
        self.tagTree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.dataset = None
        self.init_ui()        

    def init_ui(self):        
        # tv = ttk.Treeview(parent)
        self.tagTree['columns']=('TAG', 'Name', 'Value')
        self.tagTree.column('#0', width=0, stretch=NO)
        self.tagTree.column('TAG', width=100)
        self.tagTree.column('Name',  width=200)
        self.tagTree.column('Value',  width=250) # sum = 550

        self.tagTree.heading('#0', text='', anchor=CENTER)
        self.tagTree.heading('TAG', text='TAG', anchor=CENTER)
        self.tagTree.heading('Name', text='Name', anchor=CENTER)
        self.tagTree.heading('Value', text='Value', anchor=CENTER)
        self.tagTree.bind('<Double-1>', self.onDoubleClick)

        self.tagTree.pack()
    
    def onDoubleClick(self, event):
        # print(self.dataset)
        ''' Executed, when a row is double-clicked. Opens 
        read-only EntryPopup above the item's column, so it is possible
        to select text '''

        # close previous popups
        # self.destroyPopups()

        # what row and column was clicked on
        rowid = self.tagTree.identify_row(event.y)
        column = self.tagTree.identify_column(event.x)

        # get column position info
        x,y,width,height = self.tagTree.bbox(rowid, column)

        # y-axis offset
        # pady = height // 2
        pady = 0

        # place Entry popup properly         
        text = self.tagTree.item(rowid, 'text')
        self.entryPopup = EntryPopup(self.tagTree, self.dataset, rowid, text)
        self.entryPopup.place( x=300, y=y+pady, anchor=W, relwidth=1) # 300 = width col1+ width col2

    def showDicomTag(self, dataset):
        self.dataset = dataset                        
        dont_show_tag = ['Pixel Data', 'File Meta Information Version']                      

        table_index = 0

        #file meta read-only
        for data_element in dataset.file_meta:
            self.tagTree.insert(parent='', index=table_index, \
                        iid=table_index, values=(data_element.tag,data_element.name,data_element.value))
            table_index += 1

        for data_element in dataset:
            if data_element.VR == "SQ":   # a sequence
                print("how to deal with sequence...")
                # for sequence_item in data_element.value:
                #     myprint(sequence_item, indent + 1)
                #     print(next_indent_string + "---------")
            else:
                if data_element.name in dont_show_tag:
                    print("""<item not printed -- in the "don't print" list>""")
                else:
                    # repr_value = repr(data_element.value)
                    # if len(repr_value) > 50:
                    #     repr_value = repr_value[:50] + "..."                    
                    # self.tagTree.insert(parent='', index=table_index, \
                    #     iid=table_index, text='', values=(data_element.tag,data_element.name,repr_value))
                    self.tagTree.insert(parent='', index=table_index, \
                        iid=table_index, values=(data_element.tag,data_element.name,data_element.value))
                    table_index += 1            

class EntryPopup(Entry):
    def __init__(self, parent, dataset, iid, text, **kw):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.dataset = dataset
        self.insert(0, text) 
        # self['state'] = 'readonly'
        # self['readonlybackground'] = 'white'
        # self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())        

    def on_return(self, event):        
        self.tv.item(self.iid, text=self.get())        
        focused = self.tv.focus()
        
        tag_original = self.tv.item(focused)["values"][0]
        name_original = self.tv.item(focused)["values"][1] 
        value_new = self.get()    
        self.tv.item(focused, values=(tag_original, name_original, value_new))

        self.updateTagDataset(tag_original, value_new)
        self.destroy()

    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')
        print("select_all...")
        # returns 'break' to interrupt default key-bindings
        return 'break'

    def updateTagDataset(self, tag_original, value_new):
        print("tag_original : " + tag_original)
        tag_replace = tag_original.replace("(", "")
        tag_replace = tag_replace.replace(")", "")

        tag_string_tuple = tag_replace.split(", ")
        print(tag_string_tuple)
        # hex_string = "0xAA"
        # "0x" also required

        tag_pre = int(tag_string_tuple[0], 16)
        tag_post = int(tag_string_tuple[1], 16)
        # an_integer is a decimal value

        hex_tag_pre = hex(tag_pre)
        hex_tag_post = hex(tag_post)
        print(hex_tag_pre)
        print(hex_tag_post)
        self.dataset[hex_tag_pre, hex_tag_post].value = value_new        
        
        print(self.dataset)