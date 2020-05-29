import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def spikeTriggeredAvgPupilSize(framesStartSample,pupilSmoothArea,spikeClustersToPlot,spikeTime,\
                spikeClusters, spontFRs,\
                    frameNoBeforeSpike = 200,frameNoAfterSpike = 200, fs=20e3, darkMode = False):

    if darkMode:
        plt.style.use('dark_background')

    framesStartTimeInMS = framesStartSample*1e3/fs

    triggeredPupilSize = np.zeros(frameNoAfterSpike+frameNoBeforeSpike)

    cameraFrameRate = 30
    estimatedTime_triggeredWindow = np.arange(-frameNoBeforeSpike,frameNoAfterSpike)/cameraFrameRate
    normalizedPupilSize = pupilSmoothArea/max(pupilSmoothArea)

    labelFontSize = 14

    firstCapturedFrame_Sample = framesStartSample[0]
    if len(pupilSmoothArea) < len(framesStartSample): #if there is missing frames the time of 
    # the last captured frame is different
        lastCapturedFrame_Sample = framesStartSample[len(pupilSmoothArea)-1] 
    else:
        lastCapturedFrame_Sample = framesStartSample[-1]

    allSpikeTriggeredPupil = []
    clusterCounter = 0
    for clusterNo in spikeClustersToPlot:
        
        
    #     print(clusterNoensor to determine the stimOnset timeensor to determine the stimOnset time)

        clusterSpikeTime = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()*1e3 #spike times in ms

    
        # keeping the only spikes that can be used to compute the triggered average
        clusterSpikeTime = clusterSpikeTime[(clusterSpikeTime>\
                            ((firstCapturedFrame_Sample*1e3/fs)+(frameNoBeforeSpike+1)*1e3/30))\
                                    & (clusterSpikeTime<\
                            ((lastCapturedFrame_Sample*1e3/fs)-(frameNoBeforeSpike+1)*1e3/30))]

        

        # frameWindows = np.array([np.arange((np.where(framesStartTimeInMS>spikeTimeLoop)[0][0] - 1)\
        #                                    - frameNoBeforeSpike, \
        #                                    (np.where(framesStartTimeInMS>spikeTimeLoop)[0][0] - 1)\
        #                                    + frameNoAfterSpike) for spikeTimeLoop in clusterSpikeTime])

        triggeredPupilSize = np.zeros(frameNoAfterSpike+frameNoBeforeSpike)
        # frameWindows = []
        # for spikeTimeLoop in clusterSpikeTime[:]:
        #     frameCorrespondingToTheSpike = np.where(framesStartTimeInMS>spikeTimeLoop)[0][0] - 1
        #     frameWindows.append(np.arange(frameCorrespondingToTheSpike\
        #                                    - frameNoBeforeSpike, \
        #                                    frameCorrespondingToTheSpike\
        #                                    + frameNoAfterSpike) )

        # triggeredPupilSize = np.mean(normalizedPupilSize[np.array(frameWindows)],0)

        for spikeTimeLoop in clusterSpikeTime[:]:

            frameCorrespondingToTheSpike = np.where(framesStartTimeInMS>spikeTimeLoop)[0][0] - 1

            triggeredPupilSize = triggeredPupilSize + \
                                    normalizedPupilSize[frameCorrespondingToTheSpike-frameNoBeforeSpike:\
                                                frameCorrespondingToTheSpike+frameNoAfterSpike]

        triggeredPupilSize = triggeredPupilSize/len(clusterSpikeTime)
        
        allSpikeTriggeredPupil.append(triggeredPupilSize)
        
        figSpikeTriggeredPupil = plt.figure(figsize=(6,4))
        axSpikeTriggeredPupil = figSpikeTriggeredPupil.add_axes([0.2,0.2,0.6,0.6])
        
        axSpikeTriggeredPupil.plot(estimatedTime_triggeredWindow,triggeredPupilSize)
        
        axSpikeTriggeredPupil.set_xlabel('second')
        axSpikeTriggeredPupil.set_title('spike-triggered pupil size, cluster: %(number1)d, FR: %(number2)0.2f' %{'number1': clusterNo, 'number2': spontFRs[clusterCounter]}, fontsize=labelFontSize)
    
        clusterCounter = clusterCounter + 1
    return  allSpikeTriggeredPupil