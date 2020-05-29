import os.path

import numpy as np
import matplotlib.pyplot as plt

from tkinter import Tk
from tkinter.filedialog import askopenfilename

# we first extract the sample numbers (according to the Intan) for each saved frame  
# please select the output of facemap (.npy) in the pop up window.
# we read the facemap data file and load the pupil area and facial movement

# inputs
# 1 - the Intan analog channel that is connected to the camera strobe
# 2 - the address to the data folder
# optional inputs:
# darMode: in case the output figure mode is preferred to be in dard theme
# histBinNumber: the number of bins used to generate the histogram of camera strobe values
# cameraStrobeValidMin: the earliest time that the camera strobe is valid, this is used to discard the invalid transitions
# detected in strobe signal

def facemapDataReading(cameraStrobe,dataFileBaseFolder,darkMode = False,\
            histBinNumber=4, cameraStrobeValidMin=0, firstStrobeValid=1):

    # option for the color of output plots in case of dark mode in jupyter notebook
    if darkMode:
        plt.style.use('dark_background')

    # the default direction for opening the pop up window
    defaultDataDir = dataFileBaseFolder

    # if the default is not valid go to C:
    if not os.path.isdir(defaultDataDir):
        defaultDataDir = "C:\\"
        
    root = Tk()
    root.withdraw()

    # open the pop-up window
    videoDataFileAdd =  askopenfilename(initialdir = defaultDataDir,title = "Select file",\
                                filetypes = (("facemap output file","*.npy"),("all files","*.*")))

    # loading the data file and put in a variable
    proc = np.load(videoDataFileAdd,allow_pickle=True).item()

    # pupilArea = proc['pupil'][0]['area']

    # total number of frames based on the facemap output
    totalNumberOfSavedFrames = proc['iframes'][0]#len(pupilSmoothArea)

    # pupil area variable from facemap
    if len(proc['pupil'])>0:
        pupilSmoothArea = proc['pupil'][0]['area_smooth']
    else:
        pupilSmoothArea = np.zeros(totalNumberOfSavedFrames)
    

    # motion variable from the facemap
    if len(proc['motion'])>1:
        motion = proc['motion'][1]
    else:
        motion = np.zeros(totalNumberOfSavedFrames)
    
    

    # plotting the histogram of values of analog channel that is connected to the camera strobe signal
    histOutput = plt.hist(cameraStrobe,bins=histBinNumber)
    plt.title('histogram of the cameraStrobe values')

    # identifing the two peaks on the distribution of camera strobe signal
    # we use these two values to set a decision boundry to detect the transition between two levels
    firstHistPeakEdge = np.argsort(histOutput[0])[-1]  # the position of the first peak on the histogram
    secondHistPeakEdge = np.argsort(histOutput[0])[-2] # the position of the second peak on the histogram

    # difining the cut level as the distance between the edges of the two peaks on the strobe histogram 
    cutLevel = (histOutput[1][firstHistPeakEdge] + histOutput[1][firstHistPeakEdge + 1] \
                + histOutput[1][secondHistPeakEdge] + histOutput[1][secondHistPeakEdge + 1]) / 4 

    # defining a degitized version for the strobe signal
    digitizedStrobe = np.zeros(cameraStrobe.shape)
    
    # set the digitized strobe to 1 wherever the strobe signal is more than the threshold value
    digitizedStrobe[cameraStrobe>cutLevel] = 1

    # detecting the down transitions in the digitized signal (down transitions are the begining of each frame)
    # upTransitionStrobe = np.where (np.diff(digitizedStrobe)==1)[0]
    downTransitionStrobe = np.where ((np.diff(digitizedStrobe)==-1))[0]

    
    # just keeping that are happening later than the earliest valid moment for the cameraStrobe
    downTransitionStrobe = downTransitionStrobe[downTransitionStrobe>cameraStrobeValidMin]
    # lastCapturedFrame_Sample = downTransitionStrobe[-1] #changed bc of the potential dropped frames 

    #first strobe is not valid (because of the way we are using the camera! probably)
    # keeping the down transition samples (except the first one) as the samples that frames were happening
    framesStartSample = downTransitionStrobe[1:] 
    # firstCapturedFrame_Sample = downTransitionStrobe[1]
    # lastCapturedFrame_Sample = framesStartSample[totalNumberOfSavedFrames-1]#framesStartSample[totalNumberOfSavedFrames]
    
    # the total number of frames based on the detected strobes with the above procedure
    totalNumberOfStrobeSignals = len(framesStartSample)

    # in some sessions the experimenter have missed the right order in the begining and we don't have
    # the correct starting sync, so we use here the last frame to get the frame sync
    if not(firstStrobeValid):
        framesStartSample = framesStartSample[-totalNumberOfSavedFrames:]
        print('Be careful: the first strobe could not be identified in the signal and dropped frames might be missed')


    else:
        # reporting the number of saved frames and the number of detected frames based on the strobe signal
        # these two numbers should be the same, otherwise the source of disrepancy should be detected    
        print(totalNumberOfStrobeSignals,':Number of strobe signals')
        print(totalNumberOfSavedFrames,':Number of saved frames')
        print('these two numbers should be the same')
    
    return framesStartSample, pupilSmoothArea, motion

