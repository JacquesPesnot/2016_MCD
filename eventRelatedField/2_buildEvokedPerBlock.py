# -*- coding: utf-8 -*-

import mne 
import os
from mne.report import Report
from mne.minimum_norm import (make_inverse_operator, write_inverse_operator)

import numpy as np
import matplotlib.pyplot as plt

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *
from sharedTools.importFunctions import *
from sharedTools.plotStimuli import *

###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

# NIPs of subjects
nips = returnNips()
nips = ['Ab140232']

# Open html report 
report = Report('Build evoked', verbose=False)

# Get the evoked directory
data_evoked_directory = returnEvokedDirectory() + '/stimulus_locked/'
data_forward_directory = returnForwardDirectory()

# Get the dictionnary with every stimuli
stim_path = returnStimuliDirectory() + 'Mp150285/' # Whatever nip
stim_dict = returnStimuli(MCDvalues=True, stim_path=stim_path, start=-.2, stop=1.8)


###############################################################################
############################# EVOKED EXTRACTION ###############################
###############################################################################


stimulus_names = ['DD', 'DC', 'CC', 'AA', 'AV', 'VV']
bloc_names = ['Auditory', 'Visual', 'Causality', 'Temporal']

# Parameters of rejection
reject = {'mag':5e-12, 'grad':500e-12} # MAG too high ??? Nearly no rejection ...

# Parameters of timing
tmin = -0.2
tmax = 1.8
times = np.arange(-0.1, .9, 0.1) # Timing of the topomap (try to be %% 2)

'''
We build for every subject, every bloc, and every stimulus the evoked response. 
The result is saved in the folder to the format "meg/evoked/stimulus_locked/Aud
itory/nip/DD-ave.fif". We basically cicle across subject, bloc and stimulus and
compute the mean epoched data (evoked).
'''

for nip in nips:
    
    ###########################################################################
    ####################### Import preprocessed data ##########################
    ###########################################################################

    raw = importRaw(nip)
    events = importEvents(raw, nip)
    
    # Filter data
    raw.filter(None, 40.)
    
    # Pick only meg channels (mag only ?)
    picks = mne.pick_types(raw.info, eeg=False, eog=False, meg=True)

    ###########################################################################
    ############################## Extract evoked #############################
    ###########################################################################
    
    for bloc in bloc_names:
        for stimulus in stimulus_names:

            ###################################################################
            ############################ Epoch data ###########################
            ###################################################################
                        
            # Find the corresponding trigger code 
            events_to_average = returnTriggerCode()[bloc + '/' + stimulus]
            
            # Eliminate doublons
            events_temp = events[events[:,2] == events_to_average,:]
            
            # Epoch data (reject)
            epochs = mne.Epochs(raw, events_temp, events_to_average, 
                                reject=reject, tmin=tmin, tmax=tmax, 
                                picks=picks)

            ###################################################################
            ########################## Average epochs #########################
            ###################################################################

            # Compute evoked response
            evoked = epochs.average()
            
            # Plot evoked response + model + topomap
            signals = stim_dict[events_to_average]
            fig = plotEvoked(evoked, signals)
            report.add_figs_to_section(fig, section=nip,
                                       captions=bloc + ' - ' + stimulus)
            

            # Save evoked file
            name_temp = data_evoked_directory + bloc + '/' + nip + '/' + stimulus + '-ave.fif'
            evoked.save(name_temp)

            ###################################################################
            #################### Compute covariance matrix ####################
            ###################################################################

            # Compute and save covariance matrix
            noise_cov = mne.compute_covariance(epochs, tmax=0., 
                                               method=['shrunk', 'empirical'])
            fig_cov, fig_spectra = mne.viz.plot_cov(noise_cov, raw.info)         
            name_temp = data_evoked_directory + bloc + '/' + nip + '/' + stimulus + '_noise-cov.fif'
            noise_cov.save(name_temp)
            
            ###################################################################
            ###################### Make inverse operator ######################
            ###################################################################
            
            # Load forward solution
            fname = data_forward_directory + nip + '/FM_trans_sss_MEG-ico5-fwd.fif'
            fwd = mne.read_forward_solution(fname, surf_ori=True)
            fwd = mne.pick_types_forward(fwd, meg=True, eeg=False)
            
            # Compute inverse operator
            info = evoked.info
            inverse_operator = make_inverse_operator(info, fwd, noise_cov, 
                                                     loose=0.2, depth=0.8)
            
            # Save inverse operator 
            name_temp = data_evoked_directory + bloc + '/' + nip + '/' + stimulus + '-inv.fif'
            write_inverse_operator(name_temp, inverse_operator)

               
    # Save HTML report                   
    report.save(os.getcwd() + '/2_buildEvokedPerBlock.html', overwrite=True, 
                open_browser=False)
                

