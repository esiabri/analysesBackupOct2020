import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# This is to look at the average of motion signal, extracted in facemap, locked to the firing of each neuron

def spikeTriggeredAvgFacialMovement(framesStartSample,motion,spikeClustersToPlot,spikeTime,\
                spikeClusters,spontFRs,\
                    frameNoBeforeSpike = 200,frameNoAfterSpike = 200, fs=20e3, darkMode = False, cameraFrameRate = 30):

    if darkMode:
        plt.style.use('dark_background')

    # time of start of each frame relative to e-phys signal start
    framesStartTimeInMS = framesStartSample*1e3/fs

    # the window size to calculate the average
    triggeredMotion = np.zeros(frameNoAfterSpike+frameNoBeforeSpike)

    # the triggering window in seconds
    estimatedTime_triggeredWindow = np.arange(-frameNoBeforeSpike,frameNoAfterSpike)/cameraFrameRate

    # normalizing the motion signal between 0 and 1
    normalizedMotion = motion/max(motion)

    labelFontSize = 14

    # the starting samples of the first and last frames
    firstCapturedFrame_Sample = framesStartSample[0]
    # lastCapturedFrame_Sample = framesStartSample[-1]
    if len(motion) < len(framesStartSample): #if there is missing frames the time of 
    # the last captured frame is different
        lastCapturedFrame_Sample = framesStartSample[len(motion)-1] 
    else:
        lastCapturedFrame_Sample = framesStartSample[-1]
    # lastCapturedFrame_Sample = framesStartSample[-1]

    # the set to keep all the calculated triggered patterns
    allSpikeTriggeredMotion = []
    clusterCounter = 0

    # each iteration of the loop is run to calculate the triggered pattern for one neuron
    for clusterNo in spikeClustersToPlot:
        
        
    #     print(clusterNoensor to determine the stimOnset timeensor to determine the stimOnset time)

        # the spike times of the neuron
        clusterSpikeTime = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()*1e3 #spike times in ms

    
        # keeping the only spikes that can be used to compute the triggered average; meaning that they should be 
        # far enough from the begining and the end of the recording so the triggering window can be defined 
        clusterSpikeTime = clusterSpikeTime[(clusterSpikeTime>\
                            ((firstCapturedFrame_Sample*1e3/fs)+(frameNoBeforeSpike+1)*1e3/30))\
                                    & (clusterSpikeTime<\
                            ((lastCapturedFrame_Sample*1e3/fs)-(frameNoBeforeSpike+1)*1e3/30))]


        triggeredMotion = np.zeros(frameNoAfterSpike+frameNoBeforeSpike)
        
        # in each iteration of this loop, we extract the frames around each spike in the neuron
        # and summing the motion around the 
        # detected frames time-locked to the spikes and then devide the summation to the number of spikes
        # to calculate the average of motion 
        for spikeTimeLoop in clusterSpikeTime[:]:

            # detecting the corresponding frame to the spike
            frameCorrespondingToTheSpike = np.where(framesStartTimeInMS>spikeTimeLoop)[0][0] - 1

            # adding the motion during the triggering window for each spike
            triggeredMotion = triggeredMotion + \
                                    normalizedMotion[frameCorrespondingToTheSpike-frameNoBeforeSpike:\
                                                frameCorrespondingToTheSpike+frameNoAfterSpike]

        # the average motion around the spike of the neurons
        triggeredMotion = triggeredMotion/len(clusterSpikeTime)
        
        # adding the detected motion pattern for the neuron to the set of paatern we are keeping for all the neurons
        allSpikeTriggeredMotion.append(triggeredMotion)
        
        # the output figure that illustrates the motion pattern around the firing for the neuron
        figSpikeTriggeredMotion = plt.figure(figsize=(6,4))
        axSpikeTriggeredMotion = figSpikeTriggeredMotion.add_axes([0.2,0.2,0.6,0.6])
        
        axSpikeTriggeredMotion.plot(estimatedTime_triggeredWindow,triggeredMotion)
        
        axSpikeTriggeredMotion.set_xlabel('second')
        axSpikeTriggeredMotion.set_title('spike-triggered Motion size, cluster: %(number1)d, FR: %(number2)0.2f' %{'number1': clusterNo, 'number2': spontFRs[clusterCounter]}, fontsize=labelFontSize)
    
        clusterCounter = clusterCounter + 1
    return  allSpikeTriggeredMotion