import numpy as np

def extractLowAndHighArousalTrials(framesStartSample, pupilSize, stimOnset, \
                timeWindowBeforeStimStart = 500,\
                timeWindowAfterStimStart = 500, frameRate = 30):

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

    return lowArousalStimTrials, highArousalStimTrials