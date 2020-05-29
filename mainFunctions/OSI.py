import numpy as np
import matplotlib.pyplot as plt

# from ClaireRenataGrantFeb2020.polarTuningCurve import polarTuningCurve
# this is based on the Renata's paper; averaging across two halves of the orientations
# the other ideas didn't work, look at the OSi_toStudy.py

def OSI(responseFunction):

    degUnit = 360/len(responseFunction)*2
    theta = np.arange(degUnit,360+degUnit,degUnit)

    # horizontalVector1 = 0
    # verticalVector1 = 0
    # sumVector1 = 0
    
    # horizontalVector2 = 0
    # verticalVector2 = 0
    # sumVector2 = 0
    
    horizontalVector = 0
    verticalVector = 0
    sumVector = 0

    orientationCounter = 0

    for orientation in theta*2*np.pi/360:

        
        horizontalVector = horizontalVector + np.cos(orientation)*0.5*(\
                    responseFunction[orientationCounter] + \
                    responseFunction[orientationCounter\
                                     +int(len(responseFunction)/2)])
        
        verticalVector = verticalVector + np.sin(orientation)*0.5*(\
                    responseFunction[orientationCounter] + \
                    responseFunction[orientationCounter\
                                     +int(len(responseFunction)/2)])
        
        sumVector = sumVector + 0.5*(\
                    responseFunction[orientationCounter] + \
                    responseFunction[orientationCounter\
                                     +int(len(responseFunction)/2)])

        # horizontalVector1 = horizontalVector1 + np.cos(orientation)*(\
        #             responseFunction[orientationCounter])

        # horizontalVector2 = horizontalVector2 + np.cos(orientation)*\
        #             responseFunction[orientationCounter\
        #                              +int(len(responseFunction)/2)]
        
        # verticalVector1 = verticalVector1 + np.sin(orientation)*(\
        #             responseFunction[orientationCounter])

        # verticalVector2 = verticalVector2 + np.sin(orientation)*\
        #             responseFunction[orientationCounter\
        #                              +int(len(responseFunction)/2)]
        
        # sumVector1 = sumVector1 + responseFunction[orientationCounter]

        # sumVector2 = sumVector2 + responseFunction[orientationCounter\
        #                              +int(len(responseFunction)/2)]
        

        orientationCounter = orientationCounter + 1

    directionVector = np.sqrt(horizontalVector**2 + verticalVector**2)

    # directionVector1 = np.sqrt(horizontalVector1**2 + verticalVector1**2)
    # directionVector2 = np.sqrt(horizontalVector2**2 + verticalVector2**2)

    # print(directionVector1/sumVector1, directionVector2/sumVector2)
    # OSI = max(directionVector1/sumVector1, directionVector2/sumVector2)

    OSI = directionVector/sumVector

    return OSI