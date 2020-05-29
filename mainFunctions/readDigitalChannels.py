# Here we read the data from the digital port of the intan to extract
# - stimulus IDs
# - the sample that the first stimulus appears
# - the sample that the last stimulus appears
# - an estimation of stim onsets based on the digital tags (the actual stimonset has aournd 10 ms delay relative
# to this estimeation-late 2019, and 2020)

# input to the function: address of the data folder

# output of the function: the above extracted variables with the same order

import numpy as np

def readDigitalChannels(dataFileBaseFolder):

    # building the address to the digital data file
    Digital_DataFileAdd = dataFileBaseFolder + '/' + 'digitalin.dat' # 

    # reading the data file
    Digital_dataFile = open(Digital_DataFileAdd, 'rb')
    Digital_data = np.fromfile(Digital_dataFile,dtype='uint16')
    Digital_dataFile.close()



    # needed transformation to extract the stimID from the digital bits recorded by intan
    stimIDbitRange = range(4,8) #NIC-card bit 0 connected to Intan bit 7, ni1 to intan6, ni2 to intan5, ni3 to intan4 
        
    stimID = np.zeros(Digital_data.shape)

    for digiChanNo in stimIDbitRange:
        
        bitValue = (((Digital_data & 2**digiChanNo) > 0).astype('int'))
        
        if digiChanNo == 4:
            stimID = stimID + bitValue*(2**3)
            
        elif digiChanNo == 5:
            stimID = stimID + bitValue*(2**2)
            
        elif digiChanNo == 6:
            stimID = stimID + bitValue*(2**1)
            
        elif digiChanNo == 7:
            stimID = stimID + bitValue*(2**0)
        
    beforeFlipTagCh = 0
    afterFlipTagCh = 1

    beforeFlipTag = ((Digital_data & 2**beforeFlipTagCh) > 0).astype('int')
    afterFlipTag = ((Digital_data & 2**afterFlipTagCh) > 0).astype('int')

    stimOnset_DigitalTag_beforeStimOnFlip = np.where (np.diff(beforeFlipTag)<0)[0] + 1
    stimOnset_DigitalTag_afterStimOnFlip = np.where (np.diff(afterFlipTag)<0)[0] + 1

    # detecting the noise on the digital channels, a moment that both tags go down together
    detectedNoise = np.where(stimOnset_DigitalTag_afterStimOnFlip==stimOnset_DigitalTag_beforeStimOnFlip)[0]
    stimOnset_DigitalTag_beforeStimOnFlip = np.delete(stimOnset_DigitalTag_beforeStimOnFlip,detectedNoise)
    stimOnset_DigitalTag_afterStimOnFlip = np.delete(stimOnset_DigitalTag_afterStimOnFlip,detectedNoise)


    stimID = stimID[stimOnset_DigitalTag_beforeStimOnFlip]
    
    firstBeforeStimTag = stimOnset_DigitalTag_beforeStimOnFlip[0]
    lastStimTagSampleNo = stimOnset_DigitalTag_beforeStimOnFlip[-1]

    return stimID, firstBeforeStimTag, lastStimTagSampleNo, \
        stimOnset_DigitalTag_afterStimOnFlip