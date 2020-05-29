import os.path
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import csv
import numpy as np

def loadSpikesFromPhy(dataFileBaseFolder):
    defaultSpikeDir = dataFileBaseFolder

    if not os.path.isdir(defaultSpikeDir):
        defaultSpikeDir = "C:\\"
        
    root = Tk()
    root.withdraw()

    spikeFileAdd =  askopenfilename(initialdir = defaultSpikeDir,title = "Select file",\
                                filetypes = (("Spike Times","*.npy"),("all files","*.*")))

    spikeSortingBaseFolder = os.path.dirname(spikeFileAdd)




    spikesSampleFileAdd = spikeSortingBaseFolder + '/' + 'spike_times.npy'
    spikeClusterFileAdd = spikeSortingBaseFolder + '/' + 'spike_clusters.npy'


    spikeClusters = np.load(spikeClusterFileAdd)  #the file is saved after Ctl+s in Phy
    spikesSample = np.load(spikesSampleFileAdd)

    clusterLabelFileAdd = spikeSortingBaseFolder + '/' + 'cluster_info.tsv'

    clusterId = []
    clusterLabel = []
    with open(clusterLabelFileAdd) as tsvfile:
      reader = csv.reader(tsvfile, delimiter="\t")
      for row in reader:
        clusterId.append(row[0])
        clusterLabel.append(row[8])
        
    clusterId = np.array(clusterId[1:])
    clusterLabel = np.array(clusterLabel[1:])

    MUA_clusters = clusterId[np.where(np.array(clusterLabel)=='mua')[0]].astype('int')
    SUA_clusters = clusterId[np.where(np.array(clusterLabel)=='good')[0]].astype('int')

    print(SUA_clusters,'these clusters numbers should be the same as the ones that have been asigned as good units in Phy')
    
    return spikesSample, spikeClusters, SUA_clusters, MUA_clusters