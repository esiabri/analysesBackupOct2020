import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def motionStillnessPowerCompareGammaAndLowFreq(motionSpectrumVectors, \
                    stillnessSpectrumVectors,df, \
            lowBand1=0, highBand1=10, lowBand2=30, highBand2=70 ,figTitle='',figNo=0,\
                    movementColor='#1CB0AC',stillnessColor='#EA8D3A'):


    power_Motion_LowFreq = np.array([np.average(motionSpectrumVectors[motionEpochCounter]\
                                    [int(lowBand1/df):int(highBand1/df)]) for \
                        motionEpochCounter in range(len(motionSpectrumVectors))])

    power_Motion_highFreq = np.array([np.average(motionSpectrumVectors[motionEpochCounter]\
                                    [int(lowBand2/df):int(highBand2/df)]) for \
                        motionEpochCounter in range(len(motionSpectrumVectors))])

    power_Stillness_LowFreq = np.array([np.average(stillnessSpectrumVectors[EpochCounter]\
                                    [int(lowBand1/df):int(highBand1/df)]) for \
                        EpochCounter in range(len(stillnessSpectrumVectors))])

    power_Stillness_highFreq = np.array([np.average(stillnessSpectrumVectors[EpochCounter]\
                                    [int(lowBand2/df):int(highBand2/df)]) for \
                        EpochCounter in range(len(stillnessSpectrumVectors))])

    relativePowerMotion = power_Motion_highFreq/power_Motion_LowFreq
    relativePowerStillness = power_Stillness_highFreq/power_Stillness_LowFreq

    pvalAvgPowerCompare = stats.ttest_ind(relativePowerMotion,relativePowerStillness)[1]

    figAvgPowerCompare = plt.figure(num=figNo,figsize=(4,6))
    axAvgPowerCompare = figAvgPowerCompare.add_axes([0.2,0.2,0.6,0.6])

    axAvgPowerCompare.bar([1,3],[np.mean(relativePowerMotion), np.mean(relativePowerStillness)],\
            color=[movementColor,stillnessColor],\
                    yerr=[stats.sem(relativePowerMotion), stats.sem(relativePowerStillness)])#, width=0.8)


    axAvgPowerCompare.spines['right'].set_visible(False)
    axAvgPowerCompare.spines['top'].set_visible(False)
    axAvgPowerCompare.spines['left'].set_position(('axes', -0.02))
    axAvgPowerCompare.spines['bottom'].set_position(('axes', -0.02))


    axAvgPowerCompare.set_xticks([1,3])
    axAvgPowerCompare.set_xticklabels(['Movement','Stillness'],fontsize=13)


    axAvgPowerCompare.set_ylabel('Relative Power',fontsize=14,labelpad=10)

    axAvgPowerCompare.text(2,np.max((np.mean(relativePowerMotion), np.mean(relativePowerStillness))),\
                                'p=%(number).1E'%{'number':pvalAvgPowerCompare},\
                                ha='center',va='bottom',fontsize=10)

    axAvgPowerCompare.set_title(figTitle)