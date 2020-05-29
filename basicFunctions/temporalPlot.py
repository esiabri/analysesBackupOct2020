import numpy as np
import matplotlib.pyplot as plt

def temporalPlot(signal,startTime,stopTime,fs,figuresize=(6,4),figNo=0,linewidth=1,ax=None,\
                    lineColor='w'):

    startSample = int(startTime*fs)
    stopSample = int(stopTime*fs)

    x = np.linspace(startTime,stopTime - 1/fs,stopSample-startSample)

    # if newFig:
    #     plt.figure(num=figNo,figsize=figuresize)
    # else:
        
    if ax:
        ax.plot(x,signal[startSample:stopSample],linewidth=linewidth,color=lineColor)

        ax.set_xlabel('time from the signal start (seconds)')

    else:
        plt.figure(num=figNo,figsize=figuresize)
        
        plt.plot(x,signal[startSample:stopSample],linewidth=linewidth,color=lineColor)

        plt.xlabel('time from the signal start (seconds)')


    