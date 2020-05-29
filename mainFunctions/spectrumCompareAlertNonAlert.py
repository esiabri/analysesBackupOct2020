import numpy as np
import matplotlib.pyplot as plt
from mainFunctions.powerSpectrumSingleChannel \
    import powerSpectrumSingleChannel

import scipy.stats as stats


def spectrumCompareAlertNonAlert(inputSignalToFreqAnalysis,\
        alertChoosedEpochsStarts, alertChoosedEpochsEnds,\
     nonAlertChoosedEpochsStarts, nonAlertChoosedEpochsEnds, framesStartSample,\
     figTitle = 'Spectrum L5',timeToExclude = 2, df = 2, \
         reducedSamplingRate = 2e3, fs=20e3, maxFreqToShow = 120, avgPowerCompare=1):


    alertSpectrumAbs = []
    alertSpectrumNormed = []
    alertTotalPower = []
    alertEpochDur = []


    for epochCounter in range(len(alertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[alertChoosedEpochsStarts[epochCounter]]\
                            *reducedSamplingRate/fs)\
                                    + int(timeToExclude*reducedSamplingRate)
        epochEndSample = int(framesStartSample[alertChoosedEpochsEnds[epochCounter]]\
                            *reducedSamplingRate/fs)\
                                    - int(timeToExclude*reducedSamplingRate)
        
        # print(epochEndSample-epochStartSample)

        f, welchEstimatedPowerSpectrum, estimatedTotalPower = \
                    powerSpectrumSingleChannel(\
                        inputSignalToFreqAnalysis[epochStartSample:epochEndSample],\
                        reducedSamplingRate,figToShow = False,\
                            maxFreqToShow = 120, freqRes = df, Normalized = 0 )
        
        alertSpectrumAbs.append(welchEstimatedPowerSpectrum)
        alertSpectrumNormed.append(welchEstimatedPowerSpectrum/estimatedTotalPower)
        alertTotalPower.append(estimatedTotalPower)
        # alertEpochDur.append((epochEndSample - epochStartSample)/reducedSamplingRate)


    nonAlertSpectrumAbs = []
    nonAlertSpectrumNormed = []
    nonAlertTotalPower = []
    nonAlertEpochDur = []

    for epochCounter in range(len(nonAlertChoosedEpochsStarts)):
        
        epochStartSample = int(framesStartSample[nonAlertChoosedEpochsStarts[epochCounter]]\
                            *reducedSamplingRate/fs)\
                                    + int(timeToExclude*reducedSamplingRate)
        epochEndSample = int(framesStartSample[nonAlertChoosedEpochsEnds[epochCounter]]\
                            *reducedSamplingRate/fs)\
                                    - int(timeToExclude*reducedSamplingRate)
        
        
        # print(epochEndSample-epochStartSample)

        f, welchEstimatedPowerSpectrum, estimatedTotalPower = \
                    powerSpectrumSingleChannel(\
                        inputSignalToFreqAnalysis[epochStartSample:epochEndSample],\
                            reducedSamplingRate, figToShow = False,\
                                        maxFreqToShow = 120, freqRes = df, Normalized = 0 )
        
        nonAlertSpectrumAbs.append(welchEstimatedPowerSpectrum)
        nonAlertSpectrumNormed.append(welchEstimatedPowerSpectrum/estimatedTotalPower)
        nonAlertTotalPower.append(estimatedTotalPower)
        # nonAlertEpochDur.append((epochEndSample - epochStartSample)/reducedSamplingRate)

    if avgPowerCompare:
        pvalAvgPowerCompare = stats.ttest_ind(alertTotalPower,nonAlertTotalPower)[1]

        figAvgPowerCompare = plt.figure(figsize=(4,6))
        axAvgPowerCompare = figAvgPowerCompare.add_axes([0.2,0.2,0.6,0.6])

        axAvgPowerCompare.bar([1,3],\
                                        [np.mean(alertTotalPower), np.mean(nonAlertTotalPower)])#, width=0.8)


        axAvgPowerCompare.spines['right'].set_visible(False)
        axAvgPowerCompare.spines['top'].set_visible(False)
        axAvgPowerCompare.spines['left'].set_position(('axes', -0.02))
        axAvgPowerCompare.spines['bottom'].set_position(('axes', -0.02))


        axAvgPowerCompare.set_xticks([1,3])
        axAvgPowerCompare.set_xticklabels(['Motion','Stillness'],fontsize=13)

        axAvgPowerCompare.set_ylabel('Power [$\mu$$V^2$]',fontsize=14,labelpad=10)

        axAvgPowerCompare.text(2,np.max((np.mean(alertTotalPower), np.mean(nonAlertTotalPower)))*1.1,\
                                    'p=%(number).1E'%{'number':pvalAvgPowerCompare},\
                                    ha='center',va='bottom',fontsize=12) 
    
    
    epochSpectrumFig = plt.figure(figsize=(10,4))
    epochSpectrumAbsAx = epochSpectrumFig.add_axes([0.25,0.25,0.2,0.5])
    epochSpectrumNormedAx = epochSpectrumFig.add_axes([0.6,0.25,0.2,0.5])

    # if xAxisLog:
    #     epochSpectrumAbsAx.set_xscale('log')

    epochSpectrumAbsAx.semilogy(f, np.mean(alertSpectrumAbs,0))
    epochSpectrumAbsAx.semilogy(f, np.mean(nonAlertSpectrumAbs,0))

    alertSpectrumNormed = alertSpectrumAbs / (np.sum(np.mean(alertSpectrumAbs,0))*df)
    nonAlertSpectrumNormed = nonAlertSpectrumAbs / (np.sum(np.mean(nonAlertSpectrumAbs,0))*df)

    epochSpectrumNormedAx.semilogy(f, np.mean(alertSpectrumNormed,0))
    epochSpectrumNormedAx.semilogy(f, np.mean(nonAlertSpectrumNormed,0))

    epochSpectrumAbsAx.set_xlim([0,maxFreqToShow])
    epochSpectrumAbsAx.set_xlabel('frequency [Hz]')

    epochSpectrumNormedAx.set_xlim([0,maxFreqToShow])
    epochSpectrumNormedAx.set_xlabel('frequency [Hz]')

    epochSpectrumAbsAx.spines['right'].set_visible(False)
    epochSpectrumAbsAx.spines['top'].set_visible(False)

    epochSpectrumNormedAx.spines['right'].set_visible(False)
    epochSpectrumNormedAx.spines['top'].set_visible(False)

    ylimMax = 1.2*np.max([np.max(np.mean(alertSpectrumAbs,0)),np.max(np.mean(nonAlertSpectrumAbs,0))])
    ylimMin = min(np.mean(alertSpectrumAbs,0)[int(maxFreqToShow/df)],\
                        np.mean(nonAlertSpectrumAbs,0)[int(maxFreqToShow/df)])

    epochSpectrumAbsAx.set_ylim([ylimMin,ylimMax])

    ylimMax = 1.2*np.max([np.max(np.mean(alertSpectrumNormed,0)),np.max(np.mean(nonAlertSpectrumNormed,0))])
    ylimMin = min(np.mean(alertSpectrumNormed,0)[int(maxFreqToShow/df)],\
                        np.mean(nonAlertSpectrumNormed,0)[int(maxFreqToShow/df)])

    epochSpectrumNormedAx.set_ylim([ylimMin,ylimMax])

    epochSpectrumAbsAx.set_title(figTitle + ' (Non-Normalized)');
    epochSpectrumAbsAx.legend(['Motion','Stillness'])

    epochSpectrumNormedAx.set_title(figTitle + ' (Normalized)');
    epochSpectrumNormedAx.legend(['Motion','Stillness'])

    # the estimation of total power for alert and non alert periods
    # print(' ')
    # print('alert Average Power:',np.mean(alertTotalPower))#\
    #     # np.sum(np.array(alertTotalPower)*np.array(alertEpochDur))/np.sum(alertEpochDur))
    # # print('average alert Power Per Sec:',\
    # #     np.mean(np.array(alertTotalPower)/np.array(alertEpochDur)))
    # print('non-alert Total Power:',np.mean(nonAlertTotalPower))#\
    #     # np.sum(np.array(nonAlertTotalPower)*np.array(nonAlertEpochDur))/np.sum(nonAlertEpochDur))
    # # print('average non-alert Power Per Sec:',\
    # #     np.mean(np.array(nonAlertTotalPower)/np.array(nonAlertEpochDur)))

   


    return f, alertSpectrumAbs, nonAlertSpectrumAbs, alertTotalPower,\
       nonAlertTotalPower

    
# if __name__ == '__main__':
#    main()