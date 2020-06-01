import numpy as np
import matplotlib.pyplot as plt

def extractLowAndHighArousalTrials(framesStartSample, pupilSize, stimOnset, \
                timeWindowBeforeStimStart = 500,\
                timeWindowAfterStimStart = 500, frameRate = 30, distFig=1, figxLabel='movement quantity'):

    # framesStartTimeInMS = framesStartSample*1e3/fs

    # timeWindowBeforeStimStart = 500 #in ms
    

    frameNoBeforeStimStart = int(timeWindowBeforeStimStart*1e-3*frameRate)
    frameNoAfterStimStart = int(timeWindowAfterStimStart*1e-3*frameRate)

    pupilSizeAtStimOnset = []

    for stimOnsetSample in stimOnset[:]:

        frameCorrespondingToStimOnset = np.where(framesStartSample>stimOnsetSample)[0][0] - 1
        
        pupilSizeAtStimOnset.append(np.nanmean(pupilSize[\
                    frameCorrespondingToStimOnset-frameNoBeforeStimStart:\
                    frameCorrespondingToStimOnset+frameNoAfterStimStart]))
        
    pupilSizeAtStimOnset = np.array(pupilSizeAtStimOnset)
        
    lowArousalStimTrials = np.where(pupilSizeAtStimOnset<(np.median(pupilSizeAtStimOnset)))[0]
    highArousalStimTrials = np.where(pupilSizeAtStimOnset>(np.median(pupilSizeAtStimOnset)))[0]

    if distFig:

        plt.figure()
        plt.hist(pupilSizeAtStimOnset,bins=50)#int(len(framesStartSample)/1000))
        plt.xlabel(figxLabel)
        plt.ylabel('trial No')
        plt.axvline(np.median(pupilSizeAtStimOnset))

    return lowArousalStimTrials, highArousalStimTrials