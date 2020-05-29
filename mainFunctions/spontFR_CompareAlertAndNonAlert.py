import numpy as np
import matplotlib.pyplot as plt

def spontFR_CompareAlertAndNonAlert(spikeTime, spikeClusters, spikeClustersToPlot,\
     alertChoosedEpochsStarts, alertChoosedEpochsEnds,\
     nonAlertChoosedEpochsStarts, nonAlertChoosedEpochsEnds, framesStartSample,\
     timeToExclude = 0, fs=20e3):

    alertSpontFR = np.zeros(len(spikeClustersToPlot))
    nonAlertSpontFR = np.zeros(len(spikeClustersToPlot))

    alertSpontDur = 0
    nonAlertSpontDur = 0


    for epochCounter in range(len(alertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[alertChoosedEpochsStarts[epochCounter]])\
                                    + int(timeToExclude*fs)
        epochEndSample = int(framesStartSample[alertChoosedEpochsEnds[epochCounter]])\
                                    - int(timeToExclude*fs)
        
        
        alertSpontDur = alertSpontDur + (epochEndSample - epochStartSample)/fs
        
        clusterLoopCounter = 0
        for clusterNo in spikeClustersToPlot:

            clusterSpikeSample = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()

            alertSpontFR[clusterLoopCounter] = alertSpontFR[clusterLoopCounter] + \
                len(clusterSpikeSample[(clusterSpikeSample > epochStartSample) &
                                       (clusterSpikeSample < epochEndSample)])

            clusterLoopCounter = clusterLoopCounter + 1

    alertSpontFR = alertSpontFR/alertSpontDur

    for epochCounter in range(len(nonAlertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[nonAlertChoosedEpochsStarts[epochCounter]])\
                                    + int(timeToExclude*fs)
        epochEndSample = int(framesStartSample[nonAlertChoosedEpochsEnds[epochCounter]])\
                                    - int(timeToExclude*fs)
        
        
        nonAlertSpontDur = nonAlertSpontDur + (epochEndSample - epochStartSample)/fs
        
        clusterLoopCounter = 0
        for clusterNo in spikeClustersToPlot:

            clusterSpikeSample = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()

            nonAlertSpontFR[clusterLoopCounter] = nonAlertSpontFR[clusterLoopCounter] + \
                len(clusterSpikeSample[(clusterSpikeSample > epochStartSample) &
                                       (clusterSpikeSample < epochEndSample)])

            clusterLoopCounter = clusterLoopCounter + 1

    nonAlertSpontFR = nonAlertSpontFR/nonAlertSpontDur

    return alertSpontFR, nonAlertSpontFR, alertSpontDur, nonAlertSpontDur