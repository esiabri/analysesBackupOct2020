import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def powerSpectrumSingleChannel(inputSignal, SamplingRate, maxFreqToShow = 120,\
                freqRes = 0.5,figToShow = True,\
                xAxisLog = 0, figTitle = '', Normalized = 1):

    

    freqSampleNo = int(SamplingRate/freqRes)


    f, welchEstimatedPowerSpectrum = \
                    signal.welch(inputSignal, \
                                SamplingRate, nperseg=freqSampleNo, scaling='density')

    df = freqRes
#     estimatedTotalPower = np.sum(welchEstimatedPowerSpectrum\
#                                  [:min(np.where(f>=maxFreqToShow)[0])])*df
    
    estimatedTotalPower = np.sum(welchEstimatedPowerSpectrum)*df
    # power estimation: total estimated power of the signal up to the frequency that is going to be shown:
    # estimated power based on the output of the welch output in 'density' mode (it is already doubled), the sum of all
    # values need to be mutipliated by df

    if Normalized:
        welchEstimatedPowerSpectrum = welchEstimatedPowerSpectrum/\
                                                      np.sum(welchEstimatedPowerSpectrum) 


    if figToShow:

        epochSpectrumFig = plt.figure(figsize=(4,4))
        epochSpectrumAx = epochSpectrumFig.add_axes([0.25,0.25,0.6,0.5])

        if xAxisLog:
            epochSpectrumAx.set_xscale('log')

        epochSpectrumAx.semilogy(f, welchEstimatedPowerSpectrum)

        epochSpectrumAx.set_xlim([0,maxFreqToShow])
        epochSpectrumAx.set_xlabel('frequency [Hz]')

        epochSpectrumAx.spines['right'].set_visible(False)
        epochSpectrumAx.spines['top'].set_visible(False)

        # 

        epochSpectrumAx.set_ylim([min((welchEstimatedPowerSpectrum)\
                                                [:min(np.where(f>=maxFreqToShow)[0])])\
                                            ,1.2*max(welchEstimatedPowerSpectrum)])
        
        epochSpectrumAx.set_title(figTitle)

    return f, welchEstimatedPowerSpectrum, estimatedTotalPower