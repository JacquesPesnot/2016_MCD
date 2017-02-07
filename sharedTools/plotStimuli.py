# -*- coding: utf-8 -*-

import numpy as np
from config import *
import matplotlib.pyplot as plt



def plotStimulusModel(stimulus, stim=True, model=True, modelInput=False, 
                      start=-.2, stop=1.8, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1)

        # Define axis, axis limits and axis title
        ax.set_xlim([start, stop])
        ax.set_xlabel('Time (s)')
        #ax.set_ylim([-1, 1])
        ax.set_ylabel()
        ax.set_visible(False)
        ax.axhline(y=0, color='k')
    
    if stim:
        plotStimulus(ax, stimulus['signals']['audio'], 
                     {'marker':'o', 'color':'g', 's':40}, start=start,
                     freq=stimulus['freq'])
        plotStimulus(ax, stimulus['signals']['visual'],
                     {'marker':'o', 'color':'m', 's':40}, start=start,
                     freq=stimulus['freq'])

    if model:
        corrSignal = stimulus['MCD_corr_signal']/1000. # Normalize the signal between 0 and ~ 1 fT
        plotModel(ax, corrSignal, {'color':'b', 'linewidth':2},
                  freq=stimulus['freq'], start=start, stop=stop) # Plot corr signal
        lagSignal = stimulus['MCD_lag_signal']/200. # Normalize the signal between ~ -1 and ~ 1
        plotModel(ax, lagSignal, {'color':'r', 'linewidth':2},
                  freq=stimulus['freq'], start=start, stop=stop) # Plot lag signal

    if modelInput:
        audSignal = stimulus['MCD_aud_signal']/1. # Normalize the signal between 0 and ~ 1
        plotModel(ax, audSignal, {'color':'g', 'linewidth':2},
                  freq=stimulus['freq'], start=start, stop=stop) # Plot corr signal
        visSignal = stimulus['MCD_vis_signal']/1. # Normalize the signal between ~ -1 and ~ 1
        plotModel(ax, visSignal, {'color':'m', 'linewidth':2},
                  freq=stimulus['freq'], start=start, stop=stop) # Plot lag signal
    
    return ax


def plotStimulus(ax, stimSignal, param_dict, freq=200., start=-.2):
    # Plot stimuli 
    stimSignal = np.squeeze(np.where(stimSignal==1))/freq # find points in time
    stimSignal = stimSignal + start # Correct for start lag
    out = ax.scatter(stimSignal, np.zeros(len(stimSignal)), **param_dict)
    return out

def plotModel(ax, modelSignal, param_dict, freq=200., start=-.2, stop=1.8):
    t = np.linspace(start, stop, len(modelSignal))
    # Plot model
    out = ax.plot(t, modelSignal, linestyle='--', alpha=.8, **param_dict)
    return out


def plotEvoked(evoked, stimulus, start=-.2, stop=1.8, 
               times=np.arange(-0.1, .9, 0.1)):
                          
    # Compute the number of subplots needed : 
    # 2 butterfly + 1 stim + 1 model + len(times) topomap
    ncol = (len(times)*2)/2
    nrow = 4
    
    # Open figure                                      
    fig = plt.figure(figsize=(19, 9))
 
    # Butterfly plot
    ax1 = plt.subplot2grid((nrow, ncol), (0, 0), colspan=int((1./2.)*ncol), rowspan=2)
    ax2 = plt.subplot2grid((nrow, ncol), (2, 0), colspan=int((1./2.)*ncol), rowspan=2)
    axmeg = np.array([ax1, ax2])
    axmeg = evoked.plot(axes=axmeg, show=False)
    
    # Topomaps
    ax3 = np.array(np.zeros(len(times)), dtype='object')
    for i in range(len(times)):
        ax3[i] = plt.subplot2grid((nrow, ncol), (int(i/((1./2.)*ncol)), int((1./2.)*ncol) + i%(ncol/2)))
    ax3 = evoked.plot_topomap(times=times, axes=ax3, colorbar=False, show=False)
    
    # Stimulus
    ax4 = plt.subplot2grid((nrow, ncol), (2, int((1./2.)*ncol)), colspan=int((1./2.)*ncol), rowspan=1)
    ax4 = plotStimulusModel(stimulus, stim=True, model=False, modelInput=True, 
                            start=start, stop=stop, ax=ax4)
    
    # Model
    ax5 = plt.subplot2grid((nrow, ncol), (3, int((1./2.)*ncol)), colspan=int((1./2.)*ncol), rowspan=1)
    ax5 = plotStimulusModel(stimulus, stim=True, model=True, modelInput=False, 
                            start=start, stop=stop, ax=ax5)

    return fig



'''
###############################################################################
################################### EXAMPLE ###################################
###############################################################################

# Directories to use
stim_path = returnStimuliDirectory() + 'Mp150285/' # Whatever nip

# MEG sampling frequency
meg_freq = returnResampFreq()

# Get the dictionnary with every stimuli
stim_dict = returnStimuli(MCDvalues=True, stim_path=stim_path, meg_freq=meg_freq, offset=.8)
triggers = returnTriggerCode()

# Choose one and plot it
stimulus = stim_dict[triggers['Causality/Correlation/CC']]
plotStimulusModel(stimulus)

# Choose one and plot it
stimulus = stim_dict[triggers['Temporal/Order/AA']]
plotStimulusModel(stimulus)
'''