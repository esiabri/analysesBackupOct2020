import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy as sc
from basicFunctions.firingRate import firingRate

# Here we generate the PSTH and firing rate of one neuron in response to different orientataions

# inputs:
# 1- clusterSpikeTime: the time of spikes for this cluster (in seconds)
# 2- clusterNo: the cluster No (used for labeling the output plots)
# 3- stimID: this vecotr contains the orientation id of each stimulus that has been presented
# 4- stimOnset: this vecotr contains the starting sample of each visual stimulus in terms of Intan sampling

# optional inputs:
# 1- responseWindowStart: the start of response window plot relative to stim onset in miliseconds (default:-500)
# 2- responseWindowEnd: the end of response window plot relative to stim onset in milliseconds (default: 500)
# 3- responseSignificanceWindow: the width of the window that is used to asses the responsiveness of the neuron
# in milliseconds (default: 400) and it means that the number of spikes in 400 ms window after stim onset is compared
# to the number of spikes in the 400-ms window before stim onset (the comparison is done for each orientation
# individually and if one orientation is found to be significant then the neuron is labeled as responsive)
# 4- histBinWidth: the width of bins used to generate and calculate the firing rate in milliseconds (default: 50)
# 5- fs: recording sampling frequency (default is 20000 that is commonly true but should be changed in case 
# the recording sampling freqeuncy is different)
# 6- responsivenessPvalThreshold: the significance threshold that is used to call the neuron responsive (comparision
# is done for each orientation and so this threshold is modified by bonferroni rule based on the number of orientations)
# 7- darkMode: to set the default coloring of the plots (default: False)

def neuronVisualResponse(clusterSpikeTime,clusterNo,stimID,stimOnset, responseWindowEnd = 500,\
                        responseWindowStart = -500, responseSignificanceWindow = 400,histBinWidth = 50,\
                             fs=20e3,\
                        responsivenessPvalThreshold = 0.05,darkMode = False):

    if darkMode:
        plt.style.use('dark_background')


    responsiveness = 0
    
    # change the spike times scale from seconds to milliseconds
    clusterSpikeTime = clusterSpikeTime*(10**3) #in ms

    # the whole duration of response window to plot 
    responseWindowDur = responseWindowEnd - responseWindowStart

    # spike length to be plot on the PSTH
    spikelength = 0.2
    
    # the number of bins of response histogram calculated based on the response duration and width of each bin
    binNo = int(responseWindowDur/histBinWidth)

    # the orientations that are present in the stimID vector
    allOrientations = np.unique(stimID)

    # the number of trials per orientation
    trialPerDir = len(stimID)/len(allOrientations)

    # calculating the rotation step in terms of degrees
    degUnit = 360/len(allOrientations)

    # default number of trials per orientation, used to calibrate the PSTH figure size
    defaultTrialNoToPlot = 50

    # calculating the height the PSTH figure based on the number of trials per orientation
    figHeight = 8*(trialPerDir/defaultTrialNoToPlot)
    
    # the following sets were defined to keep the variables that we want to return from this function
    clusterResponsivenessPvals = [] # the p-value for the responsiveness of the neuron for each orientation
    clusterBaselineCorrectedResponse = [] # the baseline corrected responses for the neuron for each orientation
    clusterMaxResponse = [] # maximum absolute response of the neuron for each orientation
    FR_responsePattern = [] # the firing pattern of the neuron in response to each orienation


    # in each iteration of this loop we extract the response the neuron to one orientation
    for orientation in allOrientations[:]:

        # extracting the onset of all stimuli with this orientation
        orientationStimOnset = stimOnset[stimID==orientation]*(10**3)/fs # in ms


        figPSTH = plt.figure(figsize=(6*responseWindowEnd/1000,figHeight))
        axPSTH = figPSTH.add_axes([0.2,0.1 + 0.35*8/figHeight,.6,.4])
        axFR = figPSTH.add_axes([0.2,0.1,0.6,0.3*8/figHeight])

        trialCounter = 0

        # in this variable, we gather the spikes relative to stim onsets from different trials of the same orientation
        allStimTriggeredResponses=np.array([])
        
        baselineSpikeCount = []
        evokedSpikeCount = []

        # in each iteration of this loop we plot the spikes around one stim presentation
        for stimTime in orientationStimOnset:

            # extracting the spike times around the stimulus presentation
            SpikeTimesTrial = clusterSpikeTime[(clusterSpikeTime<(stimTime+responseWindowEnd))&\
                                                             (clusterSpikeTime>(stimTime+responseWindowStart))] - stimTime

            # the x and y are set to contatin the values to plot the spikes 
            x = np.array([SpikeTimesTrial.T, SpikeTimesTrial.T])
            x = x.squeeze()
            y = np.array([(trialCounter)*np.ones((1,SpikeTimesTrial.shape[0]))-spikelength/2,\
                          (trialCounter)*np.ones((1,SpikeTimesTrial.shape[0]))+spikelength/2]) # with trialCounter we make sure that we put the spike a new row relating to a new trial
            y = y.squeeze()

            # plotting the spikes for this trial
            axPSTH.plot(x,y,color='w')

            # add the spikes relating to this trial to pull of relative spike timings we keep for this orientation 
            allStimTriggeredResponses = np.append(allStimTriggeredResponses, SpikeTimesTrial)

            # trial counter is set for the next loop iteration; putting the spikes of the next trial on the next row of the plot
            trialCounter = trialCounter + 1

            # counting the number of baseline spikes for this trial and adding it to the vector (baselineSpikeCount) to keep the baseline spike counts of all trials
            baselineSpikeCount.append(len(clusterSpikeTime[\
                                    (clusterSpikeTime>(stimTime-responseSignificanceWindow))&\
                                                (clusterSpikeTime<stimTime)]))

            # counting the number of evoked spikes for this trial adding it to the vector (evokedSpikeCount) to keep the evoked spikes counts of all trials
            evokedSpikeCount.append(len(clusterSpikeTime[\
                                    (clusterSpikeTime<(stimTime+responseSignificanceWindow))&\
                                                (clusterSpikeTime>stimTime)]))


        # at the end of the previous loop, two vectors of baselineSpikeCount and evokedSpikeCount contain all the baseline and evoked spike counts for all trials and here we compare these across all the trials for this orientation
        # the pvalue of this comparison is saved in pvalResponsivenees
        pvalResponsiveness = stats.ttest_rel(baselineSpikeCount,evokedSpikeCount)[1]
        
        # to calculate the responsive to this orientation we subtract the mean of evoked pike count from the mean of baseline spike count and devided it by the width of reponse window to get the firing rate
        responseRelative = (np.mean(evokedSpikeCount) - np.mean(baselineSpikeCount))/(responseSignificanceWindow*1e-3)
        # keeping the response to all orientations here
        clusterBaselineCorrectedResponse.append(responseRelative)
        # keeping the pvalue of responses to all orientations here
        clusterResponsivenessPvals.append(pvalResponsiveness)
        
        # setting the title of the PSTH figure and reporting cluster number and the orientation for this figure
        axPSTH.set_title('cluster: %(number1)d, stimulus orientation: %(number)d deg'\
                        %{'number1':clusterNo,'number':orientation*degUnit})
        
        # plotting the histogram of responses across all trials for this orientation; to adjust the height of the histogram so that it represents the firing rate we first calculate the histogram bins and counts using np.histogram
        # then devide the number of spikes counted in each bin (counts) by the histogram width and the number of trials 
        counts, bins = np.histogram(allStimTriggeredResponses,bins=binNo)
        axFR.hist(bins[:-1], bins, weights=counts*np.ones(len(counts))*1e3/histBinWidth/trialCounter,\
            align='right',color='w')

        # we use firingRate function to calculate the smoothed firing rate in response to this orientation (sommthed version of the estimated reponse calculated through the above histogram!)
        timePoints, FR = firingRate(allStimTriggeredResponses*1e-3,responseWindowStart*1e-3,responseWindowEnd*1e-3,\
                        windowSize=histBinWidth*1e-3)

        # this firing rate should be corrected for the number of trials used to estimate the firing rate in response to this orientation
        FR = FR/trialCounter

        # plotting the smoothed firing rate on top of the histogram
        axFR.plot(timePoints*1e3, FR,c='#C0392B')

        # maximum absolute response during the responseSignificance window
        responseMax = np.max(FR[(timePoints>0)&(timePoints<responseSignificanceWindow)])

        # keeping the maximum response for all the orientations
        clusterMaxResponse.append(responseMax)
        # keeping the firing patterin in response to all orientation
        FR_responsePattern.append(FR)

        # setting the paramters for PSTH plot
        axPSTH.set_ylabel('Trial #',labelpad=-10)
        axPSTH.spines['right'].set_visible(False)
        axPSTH.spines['top'].set_visible(False)
        axPSTH.spines['bottom'].set_visible(False)
        axPSTH.axes.get_xaxis().set_visible(False)


        axPSTH.set_ylim(-spikelength,int(trialCounter)+spikelength)
        axPSTH.set_xlim(responseWindowStart,responseWindowEnd)

        axPSTH.set_yticks([0,trialCounter])
        axPSTH.spines['left'].set_position(('outward', 10))


        axFR.spines['right'].set_visible(False)
        axFR.spines['top'].set_visible(False)
        axFR.set_xlim(responseWindowStart,responseWindowEnd)

        axFR.set_yticks([0,axFR.get_ylim()[1]])
        axFR.set_yticklabels([0,int((axFR.get_ylim()[1]*10)/10)])

        axFR.set_xlabel('time from the stimulus onset (ms)')
        axFR.set_ylabel('FR (Hz) [bin size: %(number)dms]' %{'number':histBinWidth},labelpad=-10)
        axFR.set_title('relR: %(number3)0.1fHz, p=%(number2)0.2E, maxR: %(number4)dHz'\
                       %{'number2':pvalResponsiveness,\
                        'number3':responseRelative, 'number4':responseMax})

        axFR.spines['bottom'].set_position(('outward', 10))
        axFR.spines['left'].set_position(('outward', 10))
        


    # at the end of running the above loop for all the orientation, here we look at the pvalues for all orientations; if the minimum p-value across all orientation (multipled by the number of orientation; bonferroni correction) is less than
    # the pvalue threshold then we set the responsiveness flag for this neuron to 1, indicating that this neuron is visually responsive
    if min(np.array(clusterResponsivenessPvals)*len(allOrientations)) < responsivenessPvalThreshold:
        responsiveness = 1


    return responsiveness, clusterBaselineCorrectedResponse, clusterMaxResponse,\
                                 clusterResponsivenessPvals, FR_responsePattern, timePoints
