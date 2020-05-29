import numpy as np
import matplotlib.pyplot as plt
from mainFunctions.powerSpectrumSingleChannel import powerSpectrumSingleChannel

#reading the data from the start of the data
def estimatedL5chnnael(dataFileAdd,firstBeforeStimTagSampleNo,channelsNo = 64, fs=20e3,\
                        highFreqLowerBand = 500, highFreqHigherBand = 5000,figToShow = True,\
                            highestValidChannel = 0):

    noItemsToRead = firstBeforeStimTagSampleNo*channelsNo
    dataFile = open(dataFileAdd , 'rb')
    dataArray = np.fromfile(dataFileAdd,dtype='int16',count=noItemsToRead)
    dataFile.close()

    del dataFile

    dataMatrixReorderSpont = np.reshape(dataArray, (int(dataArray.shape[0]/channelsNo), channelsNo)).T

    del dataArray

    allChannelsNormHighFreqPower = []
    allChannelsHighFreqPower = []
    for channelNoToLFP_PowerStim in range(channelsNo):# 20
        df = 0.5
        inputSignalToFreqAnalysis = dataMatrixReorderSpont[channelNoToLFP_PowerStim]*0.195
        
        f, welchEstimatedPowerSpectrum, estimatedTotalPower = \
                powerSpectrumSingleChannel(inputSignalToFreqAnalysis,fs,figToShow = False,\
                                    maxFreqToShow = fs/2, freqRes = df, Normalized = 0)

        
        normHighFreqPower = np.sum(welchEstimatedPowerSpectrum[int(highFreqLowerBand/df):
                                                int(highFreqHigherBand/df)])*df/estimatedTotalPower
        
        highFreqPower = np.sum(welchEstimatedPowerSpectrum[int(highFreqLowerBand/df):
                                                int(highFreqHigherBand/df)])*df
        
        allChannelsNormHighFreqPower.append(normHighFreqPower)
        allChannelsHighFreqPower.append(highFreqPower)

    if figToShow:
        plt.figure()
        plt.plot(allChannelsHighFreqPower)
        plt.title('High Freq Power')
        plt.xlabel('channelNo')

        plt.figure()
        plt.plot(allChannelsNormHighFreqPower)
        plt.title('High Freq Normalized Power')
        plt.xlabel('channelNo')

    if highestValidChannel:
        return np.argmax(allChannelsNormHighFreqPower[:highestValidChannel]), allChannelsNormHighFreqPower,\
            allChannelsHighFreqPower
    else:
        return np.argmax(allChannelsNormHighFreqPower), allChannelsNormHighFreqPower,\
            allChannelsHighFreqPower