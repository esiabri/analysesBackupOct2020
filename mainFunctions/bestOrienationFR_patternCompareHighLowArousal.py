import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy as sc
from basicFunctions.firingRate import firingRate

def bestOrienationFR_patternCompareHighLowArousal(clusterSpikeTime,clusterNo,stimOnsetSample, fs,\
    lowArousalStimTrials,highArousalStimTrials,baselineCorrectedResponse, \
        stimID,beforeStimTime = 500, afterStimTime = 3000, histBinWidth = 50, motionColor='#2BC084',stillnessColor='#C0392B',\
                            figHeight = 5, darkMode = False, figTitle='preferred orientation'):


    orientaionNoWithHighestResponse = np.argmax(np.array(baselineCorrectedResponse))

    alertTrialsForPreferredOrientation = np.intersect1d(np.where\
                (stimID==orientaionNoWithHighestResponse)[0], highArousalStimTrials)

    nonAlertTrialsForPreferredOrientation = np.intersect1d(np.where\
                (stimID==orientaionNoWithHighestResponse)[0], lowArousalStimTrials)

    wholeResponseWindowWidth = beforeStimTime + afterStimTime

    clusterSpikeTime = clusterSpikeTime*(10**3) #in ms

    alertTrialsStimTime = stimOnsetSample[alertTrialsForPreferredOrientation]*(10**3)/fs
    NonAlertTrialsStimTime = stimOnsetSample[nonAlertTrialsForPreferredOrientation]*(10**3)/fs

    FR_patternAlertTrials = []
    FR_patternNonAlertTrials = []

    for stimTime in alertTrialsStimTime:

                # extracting the spike times around the stimulus presentation
                SpikeTimesTrial = clusterSpikeTime[(clusterSpikeTime<(stimTime+afterStimTime))&\
                                            (clusterSpikeTime>(stimTime-beforeStimTime))] - stimTime
                
                timePoints, FR = firingRate(SpikeTimesTrial*1e-3,-beforeStimTime*1e-3,\
                                            afterStimTime*1e-3,\
                            windowSize=histBinWidth*1e-3)
                
                FR_patternAlertTrials.append(FR)
                
    FR_patternAlertTrials = np.array(FR_patternAlertTrials)

    for stimTime in NonAlertTrialsStimTime:

                # extracting the spike times around the stimulus presentation
                SpikeTimesTrial = clusterSpikeTime[(clusterSpikeTime<(stimTime+afterStimTime))&\
                                            (clusterSpikeTime>(stimTime-beforeStimTime))] - stimTime
                
                timePoints, FR = firingRate(SpikeTimesTrial*1e-3,-beforeStimTime*1e-3,\
                                            afterStimTime*1e-3,\
                            windowSize=histBinWidth*1e-3)
                
                FR_patternNonAlertTrials.append(FR)
                
    FR_patternNonAlertTrials = np.array(FR_patternNonAlertTrials)

    figFRpattern = plt.figure(figsize=(4*wholeResponseWindowWidth/1000,figHeight))
    axFRpattern = figFRpattern.add_axes([0.2,0.2,.6,.6])

    axFRpattern.plot(timePoints*1e3, np.mean(FR_patternNonAlertTrials,0),c=stillnessColor);
    axFRpattern.plot(timePoints*1e3, np.mean(FR_patternAlertTrials,0),c=motionColor);

    y1 = np.mean(FR_patternNonAlertTrials,0) - \
                                    stats.sem(FR_patternNonAlertTrials,0)
    y2 = np.mean(FR_patternNonAlertTrials,0) + \
                                    stats.sem(FR_patternNonAlertTrials,0)
    axFRpattern.fill_between(timePoints*1e3, y1, y2, color=stillnessColor, alpha=0.5)

    y1 = np.mean(FR_patternAlertTrials,0) - \
                                    stats.sem(FR_patternAlertTrials,0)
    y2 = np.mean(FR_patternAlertTrials,0) + \
                                    stats.sem(FR_patternAlertTrials,0)
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


    return timePoints, FR_patternAlertTrials, FR_patternNonAlertTrials