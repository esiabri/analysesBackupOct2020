import numpy as np
import matplotlib.pyplot as plt
from basicFunctions.filters import \
                        butter_lowpass_filter

# this function examines the frames of pupil area and extract the epochs of alertness (area > alertnessThreshols)
# and epochs of nonAlertness (pupilArea < alertnessThreshod), if alertnessThreshold=0 passed to the 
# function then the alertnessThreshold is set as the median of all values for the pupil area

def exctractAlertAndNonAlertPeriods(pupilSmoothArea,framesStartSample,\
                startTime,endTime,minimumConsistentStateDur = 10,\
                    frameRate = 30,fs=20e3, alertnessThreshold = 0):

    
    endSample = int(endTime*fs)
    startSample = int(startTime*fs)
    
    endFrameNo = np.where(framesStartSample>endSample)[0][0] - 1
    if startSample>framesStartSample[0]:
        startFrameNo = np.where(framesStartSample>startSample)[0][0] - 1
    else:
        startFrameNo = 0

    pupilSignl = butter_lowpass_filter(pupilSmoothArea[startFrameNo:endFrameNo]\
                                , 1, frameRate, order=5)
    digitizedPupilArea = np.zeros(pupilSignl.shape)

    if not(alertnessThreshold):
        alertnessThreshold = np.median(pupilSignl)
    # np.median(pupilSmoothArea[:endFrameNo])

    digitizedPupilArea[pupilSignl>alertnessThreshold] = 1

    downTransitionCrossing = np.where ((np.diff(digitizedPupilArea)==-1))[0]
    upTransitionCrossing = np.where ((np.diff(digitizedPupilArea)==1))[0]

    if digitizedPupilArea[0]:
        upTransitionCrossing = np.append(0, upTransitionCrossing)
    else:
        downTransitionCrossing = np.append(0, downTransitionCrossing)
        
    if digitizedPupilArea[-1]:
        downTransitionCrossing = np.append(downTransitionCrossing, len(digitizedPupilArea)-1)
    else:
        upTransitionCrossing = np.append(upTransitionCrossing, len(digitizedPupilArea)-1)
        

    if digitizedPupilArea[0]:
        if digitizedPupilArea[-1]:
            alertEpochEnd = downTransitionCrossing
            alertEpochStart = upTransitionCrossing
            nonAlertEpochEnd = upTransitionCrossing[1:]
            nonAlertEpochStart = downTransitionCrossing[:-1]
            
            alertDurs = downTransitionCrossing - upTransitionCrossing
            nonAlertDurs = upTransitionCrossing[1:] - downTransitionCrossing[:-1]
        else:
            alertEpochEnd = downTransitionCrossing
            alertEpochStart = upTransitionCrossing[:-1]
            nonAlertEpochEnd = upTransitionCrossing[1:]
            nonAlertEpochStart = downTransitionCrossing
            
            alertDurs = downTransitionCrossing - upTransitionCrossing[:-1]
            nonAlertDurs = upTransitionCrossing[1:] - downTransitionCrossing
            
    else:
        if digitizedPupilArea[-1]:
            alertEpochEnd = downTransitionCrossing[1:]
            alertEpochStart = upTransitionCrossing
            nonAlertEpochEnd = upTransitionCrossing
            nonAlertEpochStart = downTransitionCrossing[:-1]
            
            alertDurs = downTransitionCrossing[1:] - upTransitionCrossing
            nonAlertDurs = upTransitionCrossing - downTransitionCrossing[:-1]
        else:
            alertEpochEnd = downTransitionCrossing[1:]
            alertEpochStart = upTransitionCrossing[:-1]
            nonAlertEpochEnd = upTransitionCrossing
            nonAlertEpochStart = downTransitionCrossing
            
            alertDurs = downTransitionCrossing[1:] - upTransitionCrossing[:-1]
            nonAlertDurs = upTransitionCrossing - downTransitionCrossing

     # in s
    minimumConsistentStateDurSamples = minimumConsistentStateDur*frameRate

    alertChoosedEpochs = np.where(alertDurs>minimumConsistentStateDurSamples)[0]
    nonAlertChoosedEpochs = np.where(nonAlertDurs>minimumConsistentStateDurSamples)[0]

    alertChoosedEpochsStarts = alertEpochStart[alertChoosedEpochs]
    alertChoosedEpochsEnds = alertEpochEnd[alertChoosedEpochs]

    nonAlertChoosedEpochsStarts = nonAlertEpochStart[nonAlertChoosedEpochs]
    nonAlertChoosedEpochsEnds = nonAlertEpochEnd[nonAlertChoosedEpochs]
    
    return alertChoosedEpochsStarts + startFrameNo, alertChoosedEpochsEnds + startFrameNo, \
        nonAlertChoosedEpochsStarts + startFrameNo, nonAlertChoosedEpochsEnds + startFrameNo