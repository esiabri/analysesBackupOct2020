import numpy as np
import matplotlib.pyplot as plt
from basicFunctions.filters import \
        butter_lowpass_filter
from copy import deepcopy

def stimOffsetExtraction(photoDiodeSignal,firstBeforeStimTagSampleNo, lastStimTagSampleNo,\
                            stimOnset_DigitalTag_afterStimOnFlip,\
                            fs,darkMode = False,\
                                lowPassfilterBand = 500):



    filteredPhotoDiodeSig = butter_lowpass_filter(photoDiodeSignal, lowPassfilterBand, fs, order=5)

    # check the histogram of photodiode signal values (it should be double peak distribution) 
    # and determine the cut value to transform the analog signal to a two valued digital signal
    histOutput = plt.hist(filteredPhotoDiodeSig,bins=4)
    plt.title('photoDiodeSignal Histogram')

    firstHistPeakEdge = np.argsort(histOutput[0])[-1]  # the position of the first peak on the histogram
    secondHistPeakEdge = np.argsort(histOutput[0])[-2] # the position of the second peak on the histogram

    # difining the cut level as the distance between the edges of the two peaks on the photoDiode histogram 
    cutLevel = (histOutput[1][firstHistPeakEdge] + histOutput[1][firstHistPeakEdge + 1] \
                + histOutput[1][secondHistPeakEdge] + histOutput[1][secondHistPeakEdge + 1]) / 4 

    lowLevelDigiVal = 0
    highLevelDigiVal = 1

    digitizedFilteredSig = deepcopy(filteredPhotoDiodeSig)
    digitizedFilteredSig[digitizedFilteredSig<cutLevel] = lowLevelDigiVal
    digitizedFilteredSig[digitizedFilteredSig>cutLevel] = highLevelDigiVal


    # if white is under the sensor during the stimulus
    # stimOnset = np.where (np.diff(digitizedFilteredSig)>0)[0]

    # if black is under the sensor during the stimulus
    stimOffset = np.where (np.diff(digitizedFilteredSig)>0)[0] #the samples in which the stim offset happens

    # stimOnset = stimOnset[stimOnset>startSample]

    # ignoring all the transitions that has happend before the first digital flag related to the visual stimulation

    stimOffset = stimOffset[stimOffset>firstBeforeStimTagSampleNo]
    stimOffset = stimOffset[stimOffset<(lastStimTagSampleNo+3*fs)]


    totalStimNo = len(stimOffset)

    print(totalStimNo,': detected stim offsets from the photodiode sensor')



    if totalStimNo == len(stimOnset_DigitalTag_afterStimOnFlip):
        # checking all the stimuli presentation to make sure that everything make sense!
        plt.figure()
        plt.title('all photoDiodeSignals triggered by detected stimOnset')
        transWindowToLook = 2500
        plt.xlabel('ms')
        for stimTime in stimOffset[:]: #[digitizedFilteredSig[(stimOnset+1.2*fs).astype('int')]==lowLevelAvg]:
        #     plt.figure()
            plt.plot(np.arange(-transWindowToLook,transWindowToLook,1e3/fs),\
                    filteredPhotoDiodeSig[int(stimTime-transWindowToLook*fs/1e3):\
                            int(stimTime+transWindowToLook*fs/1e3)],'gray')


        plt.figure()
        plt.title('5 sample trials zoomed-in')
        transWindowToLook = 25
        plt.xlabel('ms')
        for stimTime in stimOffset[:5]: #[digitizedFilteredSig[(stimOnset+1.2*fs).astype('int')]==lowLevelAvg]:
        #     plt.figure()
            plt.plot(np.arange(-transWindowToLook,transWindowToLook,1e3/fs),\
                    filteredPhotoDiodeSig[int(stimTime-transWindowToLook*fs/1e3):\
                            int(stimTime+transWindowToLook*fs/1e3)],'gray')

        plt.plot(np.arange(-transWindowToLook,transWindowToLook,1e3/fs),\
                digitizedFilteredSig[int(stimTime-transWindowToLook*fs/1e3):\
                        int(stimTime+transWindowToLook*fs/1e3)]*((histOutput[1][firstHistPeakEdge] + histOutput[1][firstHistPeakEdge + 1] \
                - histOutput[1][secondHistPeakEdge] - histOutput[1][secondHistPeakEdge + 1]) / 2) + \
                ((histOutput[1][secondHistPeakEdge] + histOutput[1][secondHistPeakEdge + 1]) / 2)
                ,'w')
    else:
        print('\nBE CAREFULL: Non Matched Stim No, stimonset estimated based on the digital tags (being around 10 ms ahead with 1ms jitter)')
        stimOffset = digitalTagStimOnsetEstimation
        print(len(stimOffset),': number of the stimuli based on the digital tags')


    del digitizedFilteredSig, filteredPhotoDiodeSig
    return stimOffset