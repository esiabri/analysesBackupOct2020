import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from mainFunctions.normalizedBetween_0_and_1 import normalizedBetween_0_and_1
import math

def spikeTriggeredFR1(spikeTimesNeuron1,spikeTimesNeuron2,sessionStart,sessionEnd,\
                            preWindowLen = 100,postWindowLen = 100, figureShow =0):

    # the delay window that we want to examine the correlated spiking of the two neurons
    # preWindowLen = 100   #in ms    
    # postWindowLen = 100  #in ms   
    lenWindowCrossCorr = preWindowLen + postWindowLen

    # time vector of the cross correlogram
    crossCorrTimeVector = np.arange(-lenWindowCrossCorr/2,lenWindowCrossCorr/2)

    # extract the spike time of the two neurons
    # spikeTimesNeuron1 = spikeTime[np.where(spikeClusters==clusterNo1)].squeeze()*1e3
    # spikeTimesNeuron2 = spikeTime[np.where(spikeClusters==clusterNo2)].squeeze()*1e3

    # just keeping the spikes in the part of session specified by sessionStart and sessionEnd (spont activity?)
    spikeTimesNeuron1 = spikeTimesNeuron1[(spikeTimesNeuron1>sessionStart*1e3) & \
                                        (spikeTimesNeuron1<sessionEnd*1e3)]

    spikeTimesNeuron2 = spikeTimesNeuron2[(spikeTimesNeuron2>sessionStart*1e3) & \
                                        (spikeTimesNeuron2<sessionEnd*1e3)]

    # the array to keep all the triggered spike times
    allTriggeredSpikes = np.array([])

    # in each iteration of this loop, for each spike of the neuron 1, we extract all the spikes that happens
    # in the vicinity of that spike on the neuron 2
    for spikeTimeN1 in spikeTimesNeuron1:

        # the left termporal limit to look for spikes on neuron2 relative to this spike on neuron1
        LeftLim = spikeTimeN1 - preWindowLen
        if LeftLim < sessionStart*1e3:
            LeftLim = 0

        # the right termporal limit to look for spikes on neuron2 relative to this spike on neuron1
        RightLim = spikeTimeN1 + postWindowLen
        if RightLim > sessionEnd*1e3:
            RightLim = sessionEnd*1e3

        # extract the relative spike times on nuron 2 that are happening in the window around this spike
        # on neuron 1
        tempArray = spikeTimesNeuron2[(spikeTimesNeuron2<(RightLim))\
                                            & (spikeTimesNeuron2>(LeftLim))] - spikeTimeN1

        allTriggeredSpikes = np.concatenate((allTriggeredSpikes,tempArray))
            
    # window size for smoothing the histogram of the triggered times
    WindowSize = 5

    # k-s test to check if the correlated firing pattern is significantly different from the 
    # the uniform distribution (uniform at chance level in case of no related activity between two neurons)

    # stats.ktest function with 'uniform' distribution accept samples that are sampled between 0 and 1
    # so we move samples to 0-1 distance before doing the comparison

    
    if len(allTriggeredSpikes)>1:
        ks_Pval = stats.kstest(normalizedBetween_0_and_1(allTriggeredSpikes),'uniform')[1]
    else:
        ks_Pval = math.nan
    # smoothing the histogram of the triggered times
    smoothedCrossCorr = np.convolve(\
                            np.histogram(allTriggeredSpikes\
                            ,normed=1,bins=lenWindowCrossCorr)[0],np.ones(WindowSize)/sum(np.ones(WindowSize)))\
                            [int(WindowSize/2):int(lenWindowCrossCorr+WindowSize/2)]

    # height of the cross correlogram (smoothed histogram of the triggered spike times) is representativie
    # of the correlated activity, we measured it here relative to the chance level which is the flat distribution
    # with the 1/lenWindowCrossCorr:
    peakSmoothedCrossCorr = smoothedCrossCorr.max() - 1.0/lenWindowCrossCorr

    # the delay between two neurons (where the peak happens)
    spikingDelay = np.abs(crossCorrTimeVector[np.argmax(smoothedCrossCorr)])

    if figureShow:
        fig = plt.figure()
        ax = fig.add_axes([0.2,0.2,0.6,0.6])
        ax.hist(allTriggeredSpikes,normed=1,bins=lenWindowCrossCorr);
        ax.plot(crossCorrTimeVector,smoothedCrossCorr,'r')
        ax.set_xlabel('delay (ms)')
        ax.text(.75*postWindowLen,\
        ax.get_ylim()[1]*0.9,'p=%(number)0.1e'%{'number':ks_Pval},ha='center')

    return allTriggeredSpikes, smoothedCrossCorr, peakSmoothedCrossCorr, spikingDelay, ks_Pval
