import numpy as np
import matplotlib.pyplot as plt

# NON OF THIS WORKED, the other 

# Here we want to estimate the orientation/direction selectivity of the each neuron
# The general idea is to consider the response in each direction as a vector and then by adding the
# vectors, we get the preferred direction and the effective magnitufe in that direction is the
# reperesantative of the net selectivity of the neuron for that direction

# couple of notes:
# 1 - most of the neurons are selective for the orientation and just a few percent of the neurons are
# sensitive to the direction of the motion; for the algorithm to work appropriately in both conditions
# starting from each direction we keep the next N/2 orientations (N is the number of all orientations),
# so we we keep (N/2) orientation, devide them with equal distances across the circle and then compute
# the effective sum vecotr. We repeat the same procedure N time (starting from each orientation) and then keep 
# the highest number as the orientation selectivity index.
# 2 - there are some instances that one neuron is inhibited for non-preferred directions and excited for
# the prefered directions. And in general some neurons are just inhibited in response to visual stimulation
# and for this algorithm works in such situations we scale all the responses to the orientation so that
# span between 0 and 1 (0 the lowest response across all orientations and 1 is the highest response across
# all orientations), the caveat here is that if one neuron is selectively inhibited in response to a specific
# orienatation then we can't assign a sensable direction selectivity to it. 

# this function get the the response vector to ordered orientations and returns an estimation
# for the orientation selectivity
def OSI_toStudy(responseFunction):

    # the degree distance between vectors when deviding orientations to two groups
    degUnit = 360/len(responseFunction)*2

    # all the orientation on the circle that is used to calculate the vector sum
    theta = np.arange(degUnit,360+degUnit,degUnit)

    # all the OSIs that will calculate by starting from each orientation and considering the next half of
    # all orientations
    allTempOSIs = np.zeros(len(responseFunction))

    # repeat the response function so that we can rotate and calculate the half circule starting from
    # all the orientations
    extendedResponseFunction = np.concatenate((responseFunction,responseFunction))

    # in each iteration of this loop, we start from one orienation and compute the effective vector
    # by considering response to the first orientation being at the degUnit (60 degree for 12 totall orientations)
    # and the next (N/2 - 1) orientation (5 for 12 totall orientations) spanned up to 360 in equal distances
    # (120,180,240,300 and 360 for 12 total orientations) 
    for startingOrientationCounter in range(len(responseFunction)):
    
        horizontalVector = 0
        verticalVector = 0
        sumVector = 0

        orientationCounter = 0

        

        for orientation in theta*2*np.pi/360:


            horizontalVector = horizontalVector + np.cos(orientation)*(\
                        extendedResponseFunction[orientationCounter+startingOrientationCounter])
            
            verticalVector = verticalVector + np.sin(orientation)*(\
                        extendedResponseFunction[orientationCounter+startingOrientationCounter])
            
            sumVector = sumVector + extendedResponseFunction[orientationCounter+startingOrientationCounter]
            
            # horizontalVector = horizontalVector + np.cos(orientation)*0.5*(\
            #             responseFunction[orientationCounter] + \
            #             responseFunction[orientationCounter\
            #                              +int(len(responseFunction)/2)])
            
            # verticalVector = verticalVector + np.sin(orientation)*0.5*(\
            #             responseFunction[orientationCounter] + \
            #             responseFunction[orientationCounter\
            #                              +int(len(responseFunction)/2)])
            
            # sumVector = sumVector + 0.5*(\
            #             responseFunction[orientationCounter] + \
            #             responseFunction[orientationCounter\
            #                              +int(len(responseFunction)/2)])
            

            orientationCounter = orientationCounter + 1

        directionVector = np.sqrt(horizontalVector**2 + verticalVector**2)

        allTempOSIs[startingOrientationCounter] = directionVector/sumVector

    # print(allTempOSIs)
    return max(allTempOSIs)