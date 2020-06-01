import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy as sc
from basicFunctions.firingRate import firingRate

def FR_patternCompareHIghLowArousal(clusterSpikeTime,clusterNo,stimOnsetSample, fs, lowArousalStimTrials, \
                        highArousalStimTrials, beforeStimTime = 500,\
                        afterStimTime = 3000, histBinWidth = 50, motionColor='#2BC084',stillnessColor='#C0392B',\
                            figHeight = 5, darkMode = False, figTitle='all trials'):


    wholeResponseWindowWidth = beforeStimTime + afterStimTime

    clusterSpikeTime = clusterSpikeTime*(10**3) #in ms

    FR_patternAllTrials = []

    for stimTime in stimOnsetSample*(10**3)/fs:

                # extracting the spike times around the stimulus presentation
                SpikeTimesTrial = clusterSpikeTime[(clusterSpikeTime<(stimTime+afterStimTime))&\
                                            (clusterSpikeTime>(stimTime-beforeStimTime))] - stimTime
                
                timePoints, FR = firingRate(SpikeTimesTrial*1e-3,-beforeStimTime*1e-3,\
                                            afterStimTime*1e-3,\
                            windowSize=histBinWidth*1e-3)
                
                FR_patternAllTrials.append(FR)
                
    FR_patternAllTrials = np.array(FR_patternAllTrials)

    figFRpattern = plt.figure(figsize=(4*wholeResponseWindowWidth/1000,figHeight))
    axFRpattern = figFRpattern.add_axes([0.2,0.2,.6,.6])

    axFRpattern.plot(timePoints*1e3, np.mean(FR_patternAllTrials[lowArousalStimTrials],0),c=stillnessColor);
    axFRpattern.plot(timePoints*1e3, np.mean(FR_patternAllTrials[highArousalStimTrials],0),c=motionColor);

    y1 = np.mean(FR_patternAllTrials[lowArousalStimTrials],0) - \
                                    stats.sem(FR_patternAllTrials[lowArousalStimTrials],0)
    y2 = np.mean(FR_patternAllTrials[lowArousalStimTrials],0) + \
                                    stats.sem(FR_patternAllTrials[lowArousalStimTrials],0)
    axFRpattern.fill_between(timePoints*1e3, y1, y2, color=stillnessColor, alpha=0.5)

    y1 = np.mean(FR_patternAllTrials[highArousalStimTrials],0) - \
                                    stats.sem(FR_patternAllTrials[highArousalStimTrials],0)
    y2 = np.mean(FR_patternAllTrials[highArousalStimTrials],0) + \
                                    stats.sem(FR_patternAllTrials[highArousalStimTrials],0)
    axFRpattern.fill_between(timePoints*1e3, y1, y2, color=motionColor, alpha=0.5)

    axFRpattern.legend(['stillness','movement'])

    axFRpattern.spines['right'].set_visible(False)
    axFRpattern.spines['top'].set_visible(False)
    axFRpattern.set_xlim(-beforeStimTime,afterStimTime)

    axFRpattern.set_yticks([0,axFRpattern.get_ylim()[1]])
    axFRpattern.set_yticklabels([0,int((axFRpattern.get_ylim()[1]*10)/10)])

    axFRpattern.set_xlabel('time from the stimulus onset (ms)')
    axFRpattern.set_ylabel('FR (Hz)' ,labelpad=-10)

    axFRpattern.set_title('cluster: %(number)d, ' %{'number':clusterNo} + figTitle)

    axFRpattern.spines['bottom'].set_position(('outward', 10))
    axFRpattern.spines['left'].set_position(('outward', 10))


    return timePoints, FR_patternAllTrials