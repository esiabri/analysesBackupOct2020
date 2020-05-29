import numpy as np
import matplotlib.pyplot as plt

def polarTuningCurve(responseVector, figtitle = '', darkMode = False):

    theta = np.arange(1,len(responseVector))*2*np.pi/(len(responseVector))
    theta = np.append(theta,[0,theta[0]])  

    r = responseVector
    r = np.append(r,r[0])

    figTuningPolar = plt.figure()
    axTuningPolar = figTuningPolar.add_axes([0.2,0.2,0.6,0.6], polar=True)
    axTuningPolar.plot(theta,r,'r')
    
    axTuningPolar.set_thetagrids(theta[:-1]*360/(2*np.pi))
    # axTuningPolar.set_rmax(int(axTuningPolar.get_rmax())+1)
    axTuningPolar.set_rgrids([axTuningPolar.get_rmax()])
    axTuningPolar.set_rticks([axTuningPolar.get_rmax()])
    axTuningPolar.set_yticklabels([str(int(axTuningPolar.get_rmax()))+'Hz'])
    
    axTuningPolar.set_rlabel_position(50)
    axTuningPolar.tick_params(axis='y',labelsize=12)

    if isinstance(figtitle, float):
        axTuningPolar.set_title('OSI: %(number)0.2f'%{'number':figtitle}, pad = 20)