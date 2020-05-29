import numpy as np
import matplotlib.pyplot as plt
from mainFunctions.spikeTriggeredFR import spikeTriggeredFR
import scipy.stats as stats
from mainFunctions.normalizedBetween_0_and_1 import normalizedBetween_0_and_1
import math

def spikeTriggeredFR_alertNonAlert(spikeTimesNeuron1,spikeTimesNeuron2,\
                            alertChoosedEpochsStarts, alertChoosedEpochsEnds,\
                            nonAlertChoosedEpochsStarts, nonAlertChoosedEpochsEnds, framesStartSample,\
                            preWindowLen = 100,postWindowLen = 100, timeToExclude = 0, fs = 20e3,\
                                figureShow =0):


    alertTriggeredSpikes = np.array([]) #array to keep triggered spike times during alert periods
    nonAlertTriggeredSpikes = np.array([]) #array to keep triggered spike times during non-alert periods


    lenWindowCrossCorr = preWindowLen + postWindowLen

    crossCorrTimeVector = np.arange(-lenWindowCrossCorr/2,lenWindowCrossCorr/2)


    for epochCounter in range(len(alertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[alertChoosedEpochsStarts[epochCounter]])\
                                    + int(timeToExclude*fs)
        epochEndSample = int(framesStartSample[alertChoosedEpochsEnds[epochCounter]])\
                                    - int(timeToExclude*fs)
        
        epochStartTime = epochStartSample/fs
        epochEndTime = epochEndSample/fs

        triggeredSpikes = spikeTriggeredFR(spikeTimesNeuron1,spikeTimesNeuron2,epochStartTime,epochEndTime,\
                            preWindowLen = preWindowLen, postWindowLen = postWindowLen, figureShow=0)
        
        alertTriggeredSpikes = np.concatenate((triggeredSpikes[0],alertTriggeredSpikes))
        
    for epochCounter in range(len(nonAlertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[nonAlertChoosedEpochsStarts[epochCounter]])\
                                    + int(timeToExclude*fs)
        epochEndSample = int(framesStartSample[nonAlertChoosedEpochsEnds[epochCounter]])\
                                    - int(timeToExclude*fs)
        
        epochStartTime = epochStartSample/fs
        epochEndTime = epochEndSample/fs
        
        triggeredSpikes = spikeTriggeredFR(spikeTimesNeuron1,spikeTimesNeuron2,epochStartTime,epochEndTime,\
                            preWindowLen = preWindowLen, postWindowLen = postWindowLen, figureShow=0)
        
        nonAlertTriggeredSpikes = np.concatenate((triggeredSpikes[0],nonAlertTriggeredSpikes))


    # window size for smoothing the histogram of the triggered times
    WindowSize = 5

    # smoothing the histogram of the triggered times
    smoothedCrossCorrAlert = np.convolve(\
                            np.histogram(alertTriggeredSpikes\
                            ,normed=1,bins=lenWindowCrossCorr)[0],np.ones(WindowSize)/sum(np.ones(WindowSize)))\
                            [int(WindowSize/2):int(lenWindowCrossCorr+WindowSize/2)]

    smoothedCrossCorrNonAlert = np.convolve(\
                            np.histogram(nonAlertTriggeredSpikes\
                            ,normed=1,bins=lenWindowCrossCorr)[0],np.ones(WindowSize)/sum(np.ones(WindowSize)))\
                            [int(WindowSize/2):int(lenWindowCrossCorr+WindowSize/2)]

    if len(alertTriggeredSpikes)>1:
        ks_Pval_Alert = stats.kstest(normalizedBetween_0_and_1(alertTriggeredSpikes),'uniform')[1]
    else:
        ks_Pval_Alert = math.nan

    if len(nonAlertTriggeredSpikes)>1:
        ks_Pval_NonAlert = stats.kstest(normalizedBetween_0_and_1(nonAlertTriggeredSpikes),'uniform')[1]
    else:
        ks_Pval_NonAlert = math.nan

    # height of the cross correlogram (smoothed histogram of the triggered spike times) is representativie
    # of the correlated activity, we measured it here relative to the chance level which is the flat distribution
    # with the 1/lenWindowCrossCorr:
    peakSmoothedCrossCorrAlert = smoothedCrossCorrAlert.max() - 1.0/lenWindowCrossCorr
    peakSmoothedCrossCorrNonAlert = smoothedCrossCorrNonAlert.max() - 1.0/lenWindowCrossCorr

    # the delay between two neurons (where the peak happens)
    spikingDelayAlert = np.abs(crossCorrTimeVector[np.argmax(smoothedCrossCorrAlert)])
    spikingDelayNonAlert = np.abs(crossCorrTimeVector[np.argmax(smoothedCrossCorrNonAlert)])


    fig = plt.figure()
    ax = fig.add_axes([0.2,0.2,0.6,0.6])
    ax.plot(crossCorrTimeVector,smoothedCrossCorrAlert,'w')
    ax.plot(crossCorrTimeVector,smoothedCrossCorrNonAlert,'grey')
    ax.legend(['movement','stillness'],loc='upper left')
    ax.set_xlabel('delay (ms)')
    ax.text(.75*postWindowLen,\
        ax.get_ylim()[1]*0.9,'p=%(number)0.1e'%{'number':ks_Pval_Alert},ha='center',color='w')
    ax.text(.75*postWindowLen,\
        ax.get_ylim()[1]*0.8,'p=%(number)0.1e'%{'number':ks_Pval_NonAlert},ha='center',color='grey')

    return alertTriggeredSpikes, nonAlertTriggeredSpikes, \
        smoothedCrossCorrAlert, smoothedCrossCorrNonAlert, \
        peakSmoothedCrossCorrAlert, peakSmoothedCrossCorrNonAlert, \
            spikingDelayAlert, spikingDelayNonAlert, ks_Pval_Alert, ks_Pval_NonAlert
