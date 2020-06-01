import numpy as np

# Here we generate firing rate vector for a vector of spike times that are passed to the function
# inputs:
# 1 - spikeTimes: the vector of spike times, the times should be in seconds
# 2 - startTime: the start of the signal (if not provided, then the smallest spike time is considered as the signal start)
# 3 - endTime: the end of the signal (if not provided, then the largest spike time is consdiered as the sinal end)

# optional inputs:
# dt: the temporal resolution of the firing rate vector to be generated, the default value is 1 ms
# windowSize: the window size for counting the spikes, the default value is 50 ms
# slidingWindow: (default True) using sliding windows for calculating the firing rate, if slideingWindow is set
# to false then the dt (temporal resolution) is set to be equall to the windowsize regardless of the value that
# is passed to the function

# outputs:
# 1- timePoints: the vector of time points regarding the output firing rate vector
# 2- FR: the vector of firing rate

def firingRate(spikeTimes,startTime=None,endTime=None,dt=1e-3,windowSize=50e-3,slidingWindow=True):

    # sort the spike times ascendingly 
    spikeTimes = np.sort(spikeTimes)

    # if stratTime of the output vector is not determined then the start time is set to the time of the first spike
    if startTime is None:
        startTime = np.min(spikeTimes)

    # if endTime of the output vector is not determined then the end time is set to the time of the last spike
    if endTime is None:
        endTime = np.max(spikeTimes)
    
    # if sliding window is set to false then the temporal resolution is set to the window size
    if slidingWindow is False:
        dt = windowSize

    # the vector of time points that are used to calculate firing rate
    timePoints = np.arange(startTime+windowSize,endTime,dt)

    # the firing rate vector
    FR = np.zeros(timePoints.shape)

    # in each iteration of this loop we count the spikes in one window and estimate the firing rate in that window
    for windowCounter in range(len(timePoints)):

        # finding the index of the first spike in the window (index: the spike number)
        indsStart = np.searchsorted(spikeTimes, startTime + ((windowCounter)*dt))

        #finding the index of the last spike in the window
        indsEnd = np.searchsorted(spikeTimes, startTime + ((windowCounter)*dt)+windowSize)
                 
        # estimated firing rate in the window: (number of spikes in the window)/(window duration)
        FR[windowCounter] = (indsEnd - indsStart)/windowSize

        
    return timePoints, FR
