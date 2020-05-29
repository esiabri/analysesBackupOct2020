import numpy as np
import matplotlib.pyplot as plt

def LFP_plot(inputSignal, startSample, endSample, rowDistance=0.5,\
                reducedSamplingRate=2e3,figSize=(15,10),lineColor='w',scaleLength=10,figNo=0):

    channelsNo = len(inputSignal)

    rowCounter = 0

    # plt.show(block=True)
    figRawData = plt.figure(num=figNo,figsize=figSize)
    axRawData = figRawData.add_axes([0.01,0.01,.99,.99])
    

    for channelToShow in range(channelsNo):#

        axRawData.plot((np.arange(0,endSample-startSample)/reducedSamplingRate)*1e3,\
                    rowDistance*rowCounter - inputSignal[channelToShow,startSample:endSample]\
                    ,c=lineColor,linewidth=1);


        rowCounter = rowCounter + 1


        axRawData.set_xlabel('time (ms)')
        axRawData.set_ylabel('Channel No')

        axRawData.set_yticks(np.arange(channelsNo)*rowDistance)
        axRawData.set_yticklabels(np.arange(channelsNo))

        axRawData.set_ylim([channelsNo*rowDistance+10*rowDistance,-1*rowDistance-10*rowDistance])


        axRawData.axis('off')


    scaleStartTime = ((startSample + endSample)/2/reducedSamplingRate)*1e3 - 4


    axRawData.plot(np.linspace(scaleStartTime,scaleStartTime+scaleLength,100),\
                        0.9*axRawData.get_ylim()[0]*np.ones(100),\
                                                            c='k')


    axRawData.text(scaleStartTime+scaleLength/2,\
                        0.93*axRawData.get_ylim()[0],'%(number)d ms'%{'number':scaleLength},fontsize=14,
                        ha='center')

    
