import numpy as np
from scipy.signal import hilbert
from basicFunctions.filters import \
                        butter_bandpass_filter,butter_highpass_filter,butter_lowpass_filter


# This is to filter the LFP and average the the hilbert amp of LFP during each frame so 
# to calculate the crosscorrelation of LFP and motion or pupil size extracted from facemap

def hilbertTransformedLFP_FrameRateAvg(inputSignalToFreqAnalysis,lowFreqBand,highFreqBand,\
                reducedSamplingRate,framesStartSample,cameraAvgFrameRate,fs):

    if lowFreqBand:

        inputSignalToFreqAnalysis = butter_bandpass_filter(inputSignalToFreqAnalysis,\
                                np.array([lowFreqBand,highFreqBand]),reducedSamplingRate)
    else:
        inputSignalToFreqAnalysis = butter_lowpass_filter(inputSignalToFreqAnalysis,\
                                highFreqBand,reducedSamplingRate)


    hilbertTransformedSig = hilbert(inputSignalToFreqAnalysis)
    ampTransformedSig = np.abs(hilbertTransformedSig)


    # adding the end of the last frame to the frame start vector
    framesStartSampleCorrected = np.append(framesStartSample, framesStartSample[-1]\
                                        +int(fs/cameraAvgFrameRate))

    # this should be with reduced sampling rate because we want to average on LFP which has been subsampled
    framesStartSampleCorrectedReducedRate = (framesStartSampleCorrected*reducedSamplingRate/fs).astype('int')
    # the below vector shows the boundries of the frames by intan sameple number 
    framesBoundsSamples = np.array([framesStartSampleCorrectedReducedRate[:-1],\
                                    framesStartSampleCorrectedReducedRate[1:]]).T

    # averaging the amplitude of the hilbert in each frame, so the output vector is the same size as 
    # the movement extracted for each frame
    ampHilTransformedFrameAvg = np.array([np.mean(ampTransformedSig\
                [frameBounds[0]:frameBounds[1]]) for frameBounds in \
                                framesBoundsSamples])


    return ampHilTransformedFrameAvg