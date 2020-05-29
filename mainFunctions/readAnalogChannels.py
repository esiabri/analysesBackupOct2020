import numpy as np
from os import path
from basicFunctions.filters import \
        butter_lowpass_filter

def readAnalogChannels(dataFileBaseFolder,ADC_channelsNo, diodeChannel=0,\
                    cameraStrobeChannel=3, wheelSensorChannel =4,fs=20e3):
    ADC_DataFileAdd = dataFileBaseFolder + '/' + 'ADC_data.dat' # 

    if not(path.exists(ADC_DataFileAdd)):
        ADC_DataFileAdd = dataFileBaseFolder + '/' + 'analogin.dat'

    ADC_dataFile = open(ADC_DataFileAdd, 'rb')
    ADC_dataArray = np.fromfile(ADC_dataFile,dtype='uint16')
    ADC_dataFile.close()

    ADC_dataMatrix = np.reshape(ADC_dataArray, (int(ADC_dataArray.shape[0]/ADC_channelsNo), ADC_channelsNo)).T

    photoDiodeSignal = ADC_dataMatrix[diodeChannel]*0.000050354

    cameraStrobe = ADC_dataMatrix[cameraStrobeChannel]*0.000050354
    # cameraStrobe = butter_lowpass_filter(cameraStrobe, 1390, fs, order=5)

    wheelSensorSignal = ADC_dataMatrix[wheelSensorChannel]*0.000050354
    wheelSensorSignal = butter_lowpass_filter(wheelSensorSignal, 50, fs, order=5)

#    del ADC_dataMatrix
#    del ADC_dataArray

    return photoDiodeSignal, cameraStrobe, wheelSensorSignal