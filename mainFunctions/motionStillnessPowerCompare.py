import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def motionStillnessPowerCompare(motionSpectrumVectors, stillnessSpectrumVectors, lowBand, highBand,\
                                df, figTitle='',relPower=0):


    power_Motion = [np.average(motionSpectrumVectors[motionEpochCounter]\
                                    [int(lowBand/df):int(highBand/df)]) for \
                        motionEpochCounter in range(len(motionSpectrumVectors))]

    power_Stillness = [np.average(stillnessSpectrumVectors[EpochCounter]\
                                    [int(lowBand/df):int(highBand/df)]) for \
                        EpochCounter in range(len(stillnessSpectrumVectors))]

    pvalAvgPowerCompare = stats.ttest_ind(power_Motion,power_Stillness)[1]

    figAvgPowerCompare = plt.figure(figsize=(4,6))
    axAvgPowerCompare = figAvgPowerCompare.add_axes([0.2,0.2,0.6,0.6])

    axAvgPowerCompare.bar([1,3],[np.mean(power_Motion), np.mean(power_Stillness)])#, width=0.8)


    axAvgPowerCompare.spines['right'].set_visible(False)
    axAvgPowerCompare.spines['top'].set_visible(False)
    axAvgPowerCompare.spines['left'].set_position(('axes', -0.02))
    axAvgPowerCompare.spines['bottom'].set_position(('axes', -0.02))


    axAvgPowerCompare.set_xticks([1,3])
    axAvgPowerCompare.set_xticklabels(['Motion','Stillness'],fontsize=13)

    if relPower:
        axAvgPowerCompare.set_ylabel('relative power',fontsize=14,labelpad=10)
    else:
        axAvgPowerCompare.set_ylabel('Power [$\mu$$V^2$]',fontsize=14,labelpad=10)

    axAvgPowerCompare.text(2,np.max((np.mean(power_Motion), np.mean(power_Stillness)))*0.9,\
                                'p=%(number).1E'%{'number':pvalAvgPowerCompare},\
                                ha='center',va='bottom',fontsize=12)

    axAvgPowerCompare.set_title(figTitle)