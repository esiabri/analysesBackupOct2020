import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def noiseCorrBetweenAlertAndNonAlertTrials(allClustersRelResponse,highArousalStimTrials,\
                    lowArousalStimTrials):

    if len(allClustersRelResponse) < 2 :
        print ('less than 2 responsive neurons')
        return [],[],[]
        
    noiseCorrAlert = []
    noiseCorrNonAlert = []
    for ClusterCounter1 in range(1,len(allClustersRelResponse)):
        
        for ClusterCounter2 in range(ClusterCounter1):
            
            noiseCorrAlert.append(stats.pearsonr(\
                                    allClustersRelResponse[ClusterCounter1][highArousalStimTrials]\
                                    ,allClustersRelResponse[ClusterCounter2][highArousalStimTrials])[0])
            
            noiseCorrNonAlert.append(stats.pearsonr(\
                                    allClustersRelResponse[ClusterCounter1][lowArousalStimTrials]\
                                    ,allClustersRelResponse[ClusterCounter2][lowArousalStimTrials])[0])

    pvalNoiseCorrBetweenStates = stats.ttest_ind(noiseCorrAlert,noiseCorrNonAlert)[1]

    figNoiseCorr_HighLowArousal = plt.figure(figsize=(4,6))
    axNoiseCorr_HighLowArousal = figNoiseCorr_HighLowArousal.add_axes([0.2,0.2,0.6,0.6])

    axNoiseCorr_HighLowArousal.bar([1,2],\
                                    [np.mean(noiseCorrAlert), np.mean(noiseCorrNonAlert)])#, width=0.8)


    axNoiseCorr_HighLowArousal.spines['right'].set_visible(False)
    axNoiseCorr_HighLowArousal.spines['top'].set_visible(False)
    axNoiseCorr_HighLowArousal.spines['left'].set_position(('axes', -0.02))
    axNoiseCorr_HighLowArousal.spines['bottom'].set_position(('axes', -0.02))


    axNoiseCorr_HighLowArousal.set_xticks([1,2])
    axNoiseCorr_HighLowArousal.set_xticklabels(['Alert','NonAlert'],fontsize=13)

    axNoiseCorr_HighLowArousal.set_ylabel('Noise Correlation',fontsize=14,labelpad=10)

    axNoiseCorr_HighLowArousal.text(1.5,np.max((np.mean(noiseCorrAlert), np.mean(noiseCorrNonAlert)))*1.1,\
                                'p=%(number).1E'%{'number':pvalNoiseCorrBetweenStates},\
                                ha='center',va='bottom',fontsize=12)
    return noiseCorrAlert, noiseCorrNonAlert, pvalNoiseCorrBetweenStates