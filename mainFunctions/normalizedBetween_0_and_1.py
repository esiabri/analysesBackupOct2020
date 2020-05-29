import numpy as np

def normalizedBetween_0_and_1(inputSignal):
    if not(len(inputSignal)):
        raise ValueError('empty input')

    if np.max(inputSignal) > np.min(inputSignal):
        return (inputSignal- np.min(inputSignal))/(np.max(inputSignal) - np.min(inputSignal))
    else:
        raise ValueError('not enough inputs for normalization')