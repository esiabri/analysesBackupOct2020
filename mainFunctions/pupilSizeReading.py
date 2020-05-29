import os.path

import numpy as np
import matplotlib.pyplot as plt


from tkinter import Tk
from tkinter.filedialog import askopenfilename

def pupilSizeReading(cameraStrobe,dataFileBaseFolder,darkMode = False,\
            histBinNumber=4, cameraStrobeValidMin=0):

    if darkMode:
        plt.style.use('dark_background')

    defaultDataDir = dataFileBaseFolder

    if not os.path.isdir(defaultDataDir):
        defaultDataDir = "C:\\"
        
    root = Tk()
    root.withdraw()

    videoDataFileAdd =  askopenfilename(initialdir = defaultDataDir,title = "Select file",\
                                filetypes = (("facemap output file","*.npy"),("all files","*.*")))

    proc = np.load(videoDataFileAdd,allow_pickle=True).item()

    if len(proc['pupil']):
        pupilArea = proc['pupil'][0]['area']
        pupilSmoothArea = proc['pupil'][0]['area_smooth']
    else:
        pupilArea = []
        pupilSmoothArea = []
    
    
    totalNumberOfSavedFrames = proc['iframes']#len(pupilSmoothArea)

    histOutput = plt.hist(cameraStrobe,bins=histBinNumber)
    plt.title('histogram of the cameraStrobe values')

    firstHistPeakEdge = np.argsort(histOutput[0])[-1]  # the position of the first peak on the histogram
    secondHistPeakEdge = np.argsort(histOutput[0])[-2] # the position of the second peak on the histogram

    # difining the cut level as the distance between the edges of the two peaks on the strobe histogram 
    cutLevel = (histOutput[1][firstHistPeakEdge] + histOutput[1][firstHistPeakEdge + 1] \
                + histOutput[1][secondHistPeakEdge] + histOutput[1][secondHistPeakEdge + 1]) / 4 

    digitizedStrobe = np.zeros(cameraStrobe.shape)
    
    # cameraStrobe[cameraStrobe<cutLevel] = 0
    digitizedStrobe[cameraStrobe>cutLevel] = 1

    # upTransitionStrobe = np.where (np.diff(digitizedStrobe)==1)[0]
    downTransitionStrobe = np.where ((np.diff(digitizedStrobe)==-1))[0]

    downTransitionStrobe = downTransitionStrobe[downTransitionStrobe>cameraStrobeValidMin]
    # lastCapturedFrame_Sample = downTransitionStrobe[-1] #changed bc of the potential dropped frames 
    framesStartSample = downTransitionStrobe[1:] #first strobe is not valid (because of the way we are using the camera! probably)
    firstCapturedFrame_Sample = downTransitionStrobe[1]
    lastCapturedFrame_Sample = framesStartSample[totalNumberOfSavedFrames-1]#framesStartSample[totalNumberOfSavedFrames]
    totalNumberOfStrobeSignals = len(framesStartSample)
    
    print(totalNumberOfStrobeSignals,':Number of strobe signals')
    print(totalNumberOfSavedFrames,':Number of saved frames')
    print('these two numbers should be the same')
    
    return framesStartSample, pupilSmoothArea, pupilArea, firstCapturedFrame_Sample, lastCapturedFrame_Sample

