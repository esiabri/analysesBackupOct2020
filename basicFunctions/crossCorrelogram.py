import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import correlate
from copy import deepcopy

def crossCorrelogram(signal1,signal2,samplingFreq,delaysToPlot,showShuffling=1,figTitle=''):

    xcorrLengthSamples = np.max([len(signal1),len(signal2)])

    xcorrDelays = np.arange(-(xcorrLengthSamples-1),(xcorrLengthSamples))/samplingFreq

    xcorr = correlate(signal1,signal2)

    plt.plot(xcorrDelays,xcorr)

    if showShuffling:

        sig1Shuffled = deepcopy(signal1)
        sig2Shuffled = deepcopy(signal2)

        np.random.shuffle(sig1Shuffled)
        np.random.shuffle(sig2Shuffled)

        xcorrShuffled = correlate(sig1Shuffled,sig2Shuffled)

        plt.plot(xcorrDelays,xcorrShuffled,'grey',alpha=0.4)

    plt.xlabel('delay (sedonds)')
    if delaysToPlot:
        plt.xlim(-delaysToPlot,delaysToPlot)

    plt.title('Cross Correlogram ' + figTitle)

    plt.legend(['xcorr','xcorr_shuffled'])
