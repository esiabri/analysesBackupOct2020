import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def twoVectorCompare(vec1,vec2,vec1Label,vec2Label,yaxisLabel):

    fig = plt.figure(figsize=(4,6))
    ax = fig.add_axes([0.2,0.2,0.6,0.6])

    ax.bar([1,2],[np.mean(vec1), np.mean(vec2)])#, width=0.8)


    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_position(('axes', -0.02))
    ax.spines['bottom'].set_position(('axes', -0.02))

    pval = stats.ttest_ind(vec1,vec2)[1]

    ax.set_xticks([1,2])
    ax.set_xticklabels([vec1Label,vec2Label],fontsize=13)

    ax.set_ylabel(yaxisLabel,fontsize=14,labelpad=10)

    ax.text(1.5,np.max((np.mean(vec1), np.mean(vec2)))*1.1,\
                                'p=%(number).1E'%{'number':pval},\
                                ha='center',va='bottom',fontsize=12)

    # ax.text(1,np.max((np.mean(vec1), np.mean(vec2))),\
    #                             'n=%(number)d'%{'number':len(vec1)},\
    #                             ha='center',va='bottom',fontsize=10)

    # ax.text(2,np.max((np.mean(vec1), np.mean(vec2))),\
    #                             'n=%(number)d'%{'number':len(vec2)},\
    #                             ha='center',va='bottom',fontsize=10)
