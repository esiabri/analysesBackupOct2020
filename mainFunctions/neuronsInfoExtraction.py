import numpy as np
import matplotlib.pyplot as plt

def neuronsInfoExtraction(highPassFilteredDataFileAdd, spikeTime, spikeClusters, SUA_clusters, MUA_clusters,\
                             firstBeforeStimTagSampleNo, \
                             fs, spikeTypes = 'SUA', channelsNo = 64,\
                                 darkMode = False):

    if darkMode:
        plt.style.use('dark_background')

    
    dataFile = open(highPassFilteredDataFileAdd)
    dataArray = np.fromfile(dataFile,dtype='int16')
    dataFile.close()

    del dataFile

    dataMatrixReorderHighPassFiltered = np.reshape(dataArray, (int(dataArray.shape[0]/channelsNo), channelsNo)).T

    recordingDurInMS = dataMatrixReorderHighPassFiltered.shape[1]*1e3/fs

    del dataArray
    
    # the end of the spont activity (just before the first stimTag)
    spontDuration = (firstBeforeStimTagSampleNo)/fs
    
    clusterFirstCh = 0
    clusterLastCh = 63

    channelsRange = np.arange(clusterFirstCh,clusterLastCh+1)
    spikeShapeWidth = 4 #ms

    spikeShapesFiltered = []

    spontFRs = []
    spikeWidthAll = []

    # spikeFigs = []

    if spikeTypes == 'SUA':
        spikeClustersToPlot = SUA_clusters 
    else:
        spikeClustersToPlot = np.sort(np.concatenate((MUA_clusters,SUA_clusters)))
        
    clusterChannel = []

    for clusterNo in spikeClustersToPlot:

        clusterSpikeSample = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()

        # excluding the spikes that can't be used for averaging; close to the begining and the end 
        clusterSpikeSample = clusterSpikeSample[(clusterSpikeSample > ((spikeShapeWidth/10**3)*fs/2)) &
                         (clusterSpikeSample < int((recordingDurInMS*1e-3 - (spikeShapeWidth)/10**3)*fs))]
        # clusterSpikeTime = clusterSpikeSample*(10**3)/fs 

        spikeWindows = np.array([np.arange((clusterSpikeSample[sp] - (spikeShapeWidth/10**3)*fs/2), \
                         (clusterSpikeSample[sp] + (spikeShapeWidth/10**3)*fs/2)).astype(int) for sp in range(len(clusterSpikeSample))])


        # spikeShapeAvg = np.zeros([len(channelsRange),int(spikeShapeWidth*fs/10**3)])

        spikeShapeAvgFiltered = np.zeros([len(channelsRange),int(spikeShapeWidth*fs/10**3)])


        for channelID in range(channelsNo):#

                spikeShapeAvgFiltered[channelID] = np.mean(dataMatrixReorderHighPassFiltered[channelID,spikeWindows],0)
                
                spikeShapeAvgFiltered[channelID] = spikeShapeAvgFiltered[channelID]*0.195



        channelWithHighestSpikeAmp = np.argmax(np.array([np.max(np.abs(spikeShapeAvgFiltered[ch])) for ch in range(channelsNo)]))
        
        

        figSpikeShapeAvg = plt.figure(figsize=(6,4))
        axSpikeShapeAvg = figSpikeShapeAvg.add_axes([0.2,0.2,0.6,0.6])
        
        if clusterNo in SUA_clusters:
            spikeShapeColor = "#229954"
        else:
            spikeShapeColor = "#AF601A"
            
        
        axSpikeShapeAvg.plot(np.arange(-spikeShapeWidth/2,spikeShapeWidth/2,1e3/fs),\
                             spikeShapeAvgFiltered[channelWithHighestSpikeAmp],color=spikeShapeColor)

        cellFR = len(clusterSpikeSample[(clusterSpikeSample<firstBeforeStimTagSampleNo) & \
                                                        (clusterSpikeSample>0)])/spontDuration

        # print(cellFR)
        spontFRs.append(cellFR)
        
        tickFontSize = 14
        labelFontSize = 14
        axSpikeShapeAvg.set_xlabel('ms',fontsize=tickFontSize)
        axSpikeShapeAvg.set_ylabel('$\mu$V',fontsize=tickFontSize)
        
        if spikeShapeAvgFiltered[channelWithHighestSpikeAmp]\
            [np.argmax(np.abs(spikeShapeAvgFiltered[channelWithHighestSpikeAmp]))] < 0: #positive spike 
        
            spikeShapeTroughToPeak = np.argmax(spikeShapeAvgFiltered[channelWithHighestSpikeAmp]\
                                            [np.argmin(spikeShapeAvgFiltered[channelWithHighestSpikeAmp]):])*1e3/fs

        else: #negative spike
            spikeShapeTroughToPeak = np.argmin(spikeShapeAvgFiltered[channelWithHighestSpikeAmp]\
                                            [np.argmax(spikeShapeAvgFiltered[channelWithHighestSpikeAmp]):])*1e3/fs

        axSpikeShapeAvg.set_title('cluster: %(number1)d, Ch: %(number2)d, width: %(number3)0.2fms, FR: %(number4)0.1fHz' \
                                  %{'number1': clusterNo, 'number2': channelWithHighestSpikeAmp,\
                                  'number3': spikeShapeTroughToPeak, 'number4': cellFR}, fontsize=labelFontSize)
        
        
        spikeShapesFiltered.append(spikeShapeAvgFiltered[channelWithHighestSpikeAmp])

        
        clusterChannel.append(channelWithHighestSpikeAmp)

        spikeWidthAll.append(spikeShapeTroughToPeak)
        
    return spontFRs, spikeWidthAll, clusterChannel,\
        spikeShapesFiltered, spikeClustersToPlot, recordingDurInMS
    
