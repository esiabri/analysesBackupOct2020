import numpy as np

def allTrialsResponses(spikeClusters, spikeTime, stimOnset, spikeClustersToPlot, fs=20e3,\
                                responseSignificanceWindow = 400):
    # responseSignificanceWindow = 400 #response window in ms
    allClustersRelResponse = []
    allClustersBaselineResponse = []
    allClustersEvokedResponse = []

    for clusterNo in spikeClustersToPlot:

        clusterSpikeTime = spikeTime[np.where(spikeClusters==clusterNo)].squeeze()*1e3

        clusterResponse = []
        clusterBaselineResponse = []
        clusterEvokedResponse = []

        for stimTime in stimOnset*(10**3)/fs:

                baselineSpikeCount = len(clusterSpikeTime[\
                                        (clusterSpikeTime>(stimTime-responseSignificanceWindow))&\
                                                    (clusterSpikeTime<stimTime)])

                evokedSpikeCount = len(clusterSpikeTime[\
                                        (clusterSpikeTime<(stimTime+responseSignificanceWindow))&\
                                                    (clusterSpikeTime>stimTime)])

                clusterResponse.append((evokedSpikeCount - baselineSpikeCount)\
                                    /(responseSignificanceWindow*1e-3))

                clusterBaselineResponse.append(baselineSpikeCount\
                                    /(responseSignificanceWindow*1e-3))

                clusterEvokedResponse.append(evokedSpikeCount\
                                    /(responseSignificanceWindow*1e-3))
        
        allClustersRelResponse.append(clusterResponse)
        allClustersBaselineResponse.append(clusterBaselineResponse)
        allClustersEvokedResponse.append(clusterEvokedResponse)
        
    allClustersRelResponse = np.array(allClustersRelResponse)
    allClustersBaselineResponse = np.array(allClustersBaselineResponse)
    allClustersEvokedResponse = np.array(allClustersEvokedResponse)

    return allClustersRelResponse, allClustersBaselineResponse, allClustersEvokedResponse