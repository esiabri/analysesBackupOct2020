import numpy as np

def firingRateExtract(clusterNo,clusterSpikeTime,recordingDurInMS,\
                firingRateWindow = 50,firingRateStep = 10):

    # clusterNo = spikeClustersToPlot[0]

    # clusterSpikeTime = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()*1e3/fs #spike times in ms

    # firingRateWindow = 50 # in ms
    # firingRateStep = 10 # in ms

    NoAllStepsInFR_Vector = int(recordingDurInMS/firingRateStep)
    firingRateVec = np.zeros(NoAllStepsInFR_Vector)


    for runningStep in range(int(firingRateWindow/firingRateStep),NoAllStepsInFR_Vector):
        
        windowEnd = runningStep*firingRateStep
        windowStart = windowEnd - firingRateWindow
        firingRateVec[runningStep] = len(clusterSpikeTime[(clusterSpikeTime>windowStart)&\
                                                                (clusterSpikeTime<windowEnd)])

    return firingRateVec