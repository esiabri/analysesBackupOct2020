import numpy as np
# from scipy.signal import hilbert
from basicFunctions.filters import \
                        butter_bandpass_filter,butter_highpass_filter,butter_lowpass_filter


# This is to filter the LFP and average the the hilbert amp of LFP during each frame so 
# to calculate the crosscorrelation of LFP and motion or pupil size extracted from facemap

def powerLFP_FrameAvg(inputSignalToFreqAnalysis,lowFreqBand,highFreqBand,\
                reducedSamplingRate,framesStartSample,cameraAvgFrameRate,fs):

    if lowFreqBand:

        inputSignalToFreqAnalysis = butter_bandpass_filter(inputSignalToFreqAnalysis,\
                                np.array([lowFreqBand,highFreqBand]),reducedSamplingRate)
    else:
        inputSignalToFreqAnalysis = butter_lowpass_filter(inputSignalToFreqAnalysis,\
                                highFreqBand,reducedSamplingRate)


    # hilbertTransformedSig = hilbert(inputSignalToFreqAnalysis)
    # ampTransformedSig = np.abs(hilbertTransformedSig)

    signalAmpSquared = inputSignalToFreqAnalysis**2


    # adding the end of the last frame to the frame start vector
    framesStartSampleCorrected = np.append(framesStartSample, framesStartSample[-1]\
                                        +int(fs/cameraAvgFrameRate))

    # this should be with reduced sampling rate because we want to average on LFP which has been subsampled
    framesStartSampleCorrectedReducedRate = (framesStartSampleCorrected*reducedSamplingRate/fs).astype('int')
    # the below vector shows the boundries of the frames by intan sameple number 
    framesBoundsSamples = np.array([framesStartSampleCorrectedReducedRate[:-1],\
                                    framesStartSampleCorrectedReducedRate[1:]]).T


    # duration of each frame in seconds
    framesDurationInSec = np.array([(frameBounds[1] - frameBounds[0])/reducedSamplingRate for frameBounds in \
                                framesBoundsSamples])

    # sum the the square of amplitudes during each frame
    ampSquared_FrameSum = np.array([np.sum(signalAmpSquared\
                [frameBounds[0]:frameBounds[1]]) for frameBounds in \
                                framesBoundsSamples])

    dt = 1/reducedSamplingRate
    powerInEachFrame = ampSquared_FrameSum*dt/framesDurationInSec


    return powerInEachFrame