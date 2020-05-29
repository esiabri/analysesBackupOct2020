import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def bestOrienationResponseChangeByAlertness(spikeClustersToPlot,allTrialsRelResponse,\
    highArousalStimTrials,lowArousalStimTrials,allClustersBaselineCorrectedResponse,\
    allClustersResponsiveness,stimID,figTitle = 'Response Change By Alertness'):

    if not(len(allClustersResponsiveness)):
        return [],[]

    orientaionNoWithHighestResponse = [np.argmax(np.array(allClustersBaselineCorrectedResponse)[clusterNo])+1\
                 for clusterNo in np.where(allClustersResponsiveness)[0]]

    alertTrialsForMostResponsiveChannel = [np.intersect1d(np.where\
                (stimID==orientaionNoWithHighestResponse[clusterCounter])[0], highArousalStimTrials) \
                for clusterCounter in range(len(orientaionNoWithHighestResponse))]

    nonAlertTrialsForMostResponsiveChannel = [np.intersect1d(np.where\
                (stimID==orientaionNoWithHighestResponse[clusterCounter])[0], lowArousalStimTrials) \
                for clusterCounter in range(len(orientaionNoWithHighestResponse))]

    alertEvokedResponseInPreferredStim = [allTrialsRelResponse[clusterNo]\
                                    [alertTrialsForMostResponsiveChannel[clusterNo]]\
                                    for clusterNo in range(len(allTrialsRelResponse))]

    nonAlertEvokedResponseInPreferredStim = [allTrialsRelResponse[clusterNo]\
                                    [nonAlertTrialsForMostResponsiveChannel[clusterNo]]\
                                    for clusterNo in range(len(allTrialsRelResponse))]

    allClustersNormalizedArousalResponseChange = []
    allPvalArousalResponseDiff = []

    for clusterNo in range(len(allTrialsRelResponse)):

        highArousalResponses = alertEvokedResponseInPreferredStim[clusterNo]
        lowArousalResponses = nonAlertEvokedResponseInPreferredStim[clusterNo]

        allClustersNormalizedArousalResponseChange.append((np.mean(highArousalResponses) - \
                                            np.mean(lowArousalResponses))/np.mean(lowArousalResponses))

        allPvalArousalResponseDiff.append(stats.ttest_ind(highArousalResponses,lowArousalResponses)[1])
        
        # print(stats.ttest_ind(highArousalResponses,lowArousalResponses)[1],\
        #     np.mean(highArousalResponses),np.mean(lowArousalResponses))

    figRelResponse_HighLowArousal = plt.figure(figsize=(len(allTrialsRelResponse)*2,6))
    axRelResponse_HighLowArousal = figRelResponse_HighLowArousal.add_axes([0.2,0.2,0.6,0.6])

    axRelResponse_HighLowArousal.bar(range(len(allTrialsRelResponse)),\
                                    100*np.array(allClustersNormalizedArousalResponseChange))#, width=0.8)


    axRelResponse_HighLowArousal.spines['right'].set_visible(False)
    axRelResponse_HighLowArousal.spines['top'].set_visible(False)
    axRelResponse_HighLowArousal.spines['left'].set_position(('axes', -0.02))
    axRelResponse_HighLowArousal.spines['bottom'].set_position(('axes', -0.02))


    axRelResponse_HighLowArousal.set_xticks(range(len(allTrialsRelResponse)))
    axRelResponse_HighLowArousal.set_xticklabels(spikeClustersToPlot,fontsize=13)

    axRelResponse_HighLowArousal.set_ylabel('Percent',fontsize=14,labelpad=10)
    axRelResponse_HighLowArousal.set_xlabel('Cluster No',fontsize=14,labelpad=10)

    axRelResponse_HighLowArousal.set_title(figTitle,fontsize=15,pad=10)

    for clusterNo in range(len(allTrialsRelResponse)):
        axRelResponse_HighLowArousal.text(clusterNo,100*np.array(\
                                allClustersNormalizedArousalResponseChange[clusterNo])+1,\
                                'p=%(number).1E'%{'number':allPvalArousalResponseDiff[clusterNo]},\
                                ha='center',va='bottom',fontsize=12)

    return allClustersNormalizedArousalResponseChange, allPvalArousalResponseDiff