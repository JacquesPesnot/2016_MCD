# -*- coding: utf-8 -*-

import mne 
import os
import pandas as pd
import numpy as np

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *
from sharedTools.importFunctions import *

###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

# NIPs of subjects
nips = returnNips()
nips = ['Ab140232']

# Get the evoked directory
data_evoked_directory = returnEvokedDirectory() + '/stimulus_locked/'

# Get the dictionnary with every stimuli
stim_path = returnStimuliDirectory() + 'Mp150285/' # Whatever nip
stim_dict = returnStimuli(MCDvalues=True, stim_path=stim_path, start=-.2, stop=1.8)


###############################################################################
###################### EXPORT IN R-READABLE FORMAT (TXT) ######################
###############################################################################

if 'df' in locals(): del df

stimulus_names = ['DD', 'DC', 'CC', 'AA', 'AV', 'VV']
bloc_names = ['Auditory', 'Visual', 'Causality', 'Temporal']


for nip in nips:
    for bloc in bloc_names:
        for stimulus in stimulus_names:
            
            # Read the evoked file
            fname = data_evoked_directory + bloc + '/' + nip + '/' + stimulus + '-ave.fif'
            evoked = mne.Evoked(fname)
            
            # Convert it to a table
            tab = evoked.to_data_frame()
            
            # Add context information columns
            tab['subject'] = nip  # Name
            tab['bloc'] = bloc  # Bloc
            tab['stimulus'] = stimulus  # Stimulus
            
            # Add model activity columns
            signals = stim_dict[returnTriggerCode()[bloc + '/' + stimulus]]
            tab['stimulus_signal_aud'] = np.concatenate([signals['signals']['audio'], [0]]) # Audio 
            tab['stimulus_signal_vis'] = np.concatenate([signals['signals']['visual'], [0]]) # Visual 
            tab['mcd_aud'] = np.concatenate([signals['MCD_aud_signal'], [0]]) # MCD_aud 
            tab['mcd_vis'] = np.concatenate([signals['MCD_vis_signal'], [0]]) # MCD_vis 
            tab['mcd_corr'] = np.concatenate([signals['MCD_corr_signal'], [0]]) # MCD_corr 
            tab['mcd_lag'] = np.concatenate([signals['MCD_lag_signal'], [0]]) # MCD_lag 
            
            # Add this table to the global table
            if 'df' not in locals():
                df = tab
            else:
                df = pd.concat([df, tab])

# Save table to CSV format 
fname = data_evoked_directory + 'stimulus_locked_evoked.csv'
df.to_csv(fname, sep=' ')
            
            