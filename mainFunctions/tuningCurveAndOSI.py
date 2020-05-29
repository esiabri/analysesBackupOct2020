import numpy as np
import matplotlib.pyplot as plt

from mainFunctions.polarTuningCurve import polarTuningCurve
from mainFunctions.OSI import OSI
from mainFunctions.normalizedBetween_0_and_1 import normalizedBetween_0_and_1

import warnings
warnings.filterwarnings("ignore")

def tuningCurveAndOSI(responseFunction,clusterNo):

    # baslineOSI = OSI(np.ones(len(responseFunction)))

    # allRotatedOSI_values = []
    # for rotationCounter in range(len(responseFunction)):
    #     allRotatedOSI_values.append(OSI(np.roll(responseFunction,rotationCounter)))

    # maxOSI_value = np.max(allRotatedOSI_values)

    # OSI_val = (maxOSI_value - baslineOSI)/(1-baslineOSI)

    # OSI_val = OSI(responseFunction)
    # OSI_val = OSI(normalizedBetween_0_and_1(responseFunction))

    # to correct for the negative responses and more than 1 OSI values, the responses shifted upward
    # by the minimum value

    # to correct for orienation selectivity the OSI is calculated as the maximum of the two halves
    # but which two halves? we do it for all the cuts and pick up the maximum!

    # OSI_val = 0
    # for loopCounter in range(len(responseFunction)):
    #     OSI_val = max(OSI_val,  OSI(np.roll((responseFunction - min(responseFunction)),loopCounter)))
    # # print(OSI_val)

    OSI_val = OSI((responseFunction - min(responseFunction)))

    polarFigTitle = 'OSI: %(number1)0.2f, cluster: %(number)d' %{'number1':OSI_val,'number':clusterNo}
    # print(polarFigTitle)
    polarTuningCurve(responseFunction, figtitle = OSI_val)

    # print(preferredDir,directionVector,OSI)
    # print('')

    degUnit = 360/len(responseFunction)

    figTuning = plt.figure(figsize=(8,6))
    axTuning = figTuning.add_axes([0.2,0.2,0.6,0.6])

    axTuning.plot(np.arange(0,360,degUnit),np.roll(responseFunction,1),'o-')

    axTuning.spines['right'].set_visible(False)
    axTuning.spines['top'].set_visible(False)
    # axTuning.set_xlim(0,360-degUnit)

    axTuning.set_xticks(np.arange(0,360,degUnit))

    # axTuning.set_yticks([int(axTuning.get_ylim()[0]),int(axTuning.get_ylim()[1])])
    # axTuning.set_yticklabels([axTuning.get_ylim()[0],axTuning.get_ylim()[1]])

    axTuning.set_xlabel('orientation (deg)')
    axTuning.set_ylabel('response',labelpad=10)
    axTuning.set_title(polarFigTitle)

    axTuning.spines['bottom'].set_position(('outward', 10))
    axTuning.spines['left'].set_position(('outward', 10))

    return OSI_val