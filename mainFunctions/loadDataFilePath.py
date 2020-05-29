import os.path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def loadDataFilePath(defaultDataDir):
    if not os.path.isdir(defaultDataDir):
        defaultDataDir = "C:\\"
    
    root = Tk()
    root.attributes("-topmost", True)
    root.lift()
    
    root.withdraw()

    dataFileAdd =  askopenfilename(initialdir = defaultDataDir,title = "Select file",\
                                filetypes = (("Intan raw files","*.dat"),("all files","*.*")),parent=root)

    # dataFileName = os.path.basename(dataFileAdd)[:-4]
    dataFileBaseFolder = os.path.dirname(dataFileAdd)

    infoFileAdd = dataFileBaseFolder + '/info.rhd'
    
    return dataFileAdd, dataFileBaseFolder, infoFileAdd