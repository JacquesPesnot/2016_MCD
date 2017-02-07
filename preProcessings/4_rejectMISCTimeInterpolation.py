# -*- coding: utf-8 -*-

import mne 
import os
import glob
import numpy as np
from mne.report import Report
from mne.io.pick import _picks_by_type as picks_by_type

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *
from sharedTools.misc import *

###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

if 'raw' in locals(): del raw

# Directories to use
data_sss_directory = returnSSSDirectory()
data_ica_directory = returnICADirectory()
data_preprocesed_directory = returnPreProcessedDirectory()

# NIPs of subjects
nips = returnNips()

# Bad EEG channels
bad_EEG = returnBadEEG()

# Parameters for automatic rejection
rejectDict = returnRejectLimits()

# Open html report 
report = Report('MISC artifacts automatic rejection', verbose=False)


###############################################################################
####################### ARTIFACTS REJECTION PER SUBJECT  ######################
###############################################################################

def interpolateAroundTimePoints(signal, events, delay=0, size=5):
    for event in events[:,0]:
        if event < len(signal)-size -delay:
            begin = event - size + delay
            end = event + size + delay
            signal[begin:end] = np.linspace(signal[begin], signal[end], size*2)
    return signal


for nip in nips:

    nip_path = data_ica_directory + '/' + nip + '/'
    
    # Load raw data (problem with MISC005 not present)
    for filePath in glob.glob(nip_path + '*_auto_ica_sss_raw.fif'):
        temp = mne.io.Raw(filePath, preload=True, add_eeg_ref=False)
        if 'MISC005' in temp.ch_names and nip in ['vV100048', 'Pb160320']:
            temp.drop_channels(['MISC005'])
        if not 'raw' in locals():
            raw = temp
        else:
            raw.append(temp)

    # Exclude bad EEG channels
    raw.info['bads'] = bad_EEG[nip]
    
    ###########################################################################
    ####################### Cycle across channel type #########################
    ###########################################################################    
    for ch_type, picks in picks_by_type(raw.info, meg_combined=True):
        
        #######################################################################
        ##################### Reject head-speaker artifacts ###################
        #######################################################################
       
        # Choose good channels (ch_types + misc)
        picks_misc = np.concatenate([picks, mne.pick_types(raw.info, misc=True, meg=False)])

        # Plot before transformation                   
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                         baseline=(None, 0), ch_name='MISC004', 
                                         tmax=0.5)

        misc_average = misc_epochs.average()
        report.add_figs_to_section(misc_average.plot(), 
                                   captions='MISC004 - Before time interpolation',
                                   section=nip)
         
        
        # Find MISC events  
        events = find_misc_events(raw, ch_name='MISC004', first_samp=0)
  
        # Interpolate points in time around MISC event
        raw.apply_function(interpolateAroundTimePoints, picks=picks, dtype=None, 
                           n_jobs=1, events=events)
                           
        # Create misc-based epochs                    
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                         baseline=(None, 0), ch_name='MISC004', 
                                         tmax=0.5)

        misc_average = misc_epochs.average()
        
        # Plot r score
        report.add_figs_to_section(misc_average.plot(), 
                                   captions='MISC004 - After time interpolation',
                                   section=nip)
                                   
        #######################################################################
        ########################## Reject LED artifacts #######################
        #######################################################################
       
        # Choose good channels (ch_types + misc)
        picks_misc = np.concatenate([picks, mne.pick_types(raw.info, misc=True, meg=False)])

        # Plot before transformation                   
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                         baseline=(None, 0), ch_name='MISC005', 
                                         tmax=0.5)

        misc_average = misc_epochs.average()
        report.add_figs_to_section(misc_average.plot(), 
                                   captions='MISC005 - Before time interpolation',
                                   section=nip)
         

        # Find MISC events  
        events = find_misc_events(raw, ch_name='MISC005', first_samp=0)
  
        # Interpolate points in time around MISC event
        raw.apply_function(interpolateAroundTimePoints, picks=picks, dtype=None, 
                           n_jobs=1, events=events, delay=5, size=8)
                           
        # Create misc-based epochs                    
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                         baseline=(None, 0), ch_name='MISC005', 
                                         tmax=0.5)

        misc_average = misc_epochs.average()

        # Plot r score
        report.add_figs_to_section(misc_average.plot(), 
                                   captions='MISC005 - After time interpolation',
                                   section=nip)
                                   
        # Save HTML report                   
        report.save(os.getcwd() + '/4_MISCArtifactsInterpolation.html', 
                    overwrite=True, open_browser=False)


    
    # Save not downsampled data (if we want to remove further ICAs) 
    ica_file_path = data_ica_directory + '/' + nip + '/' + nip + '_auto_ica_sss_raw.fif'
    raw.save(ica_file_path, overwrite=True, verbose=True)

    # Interpolate bad EEG channels
    raw.interpolate_bads()

    # Downsample data
    raw.resample(returnResampFreq(), npad="auto")
    
    # Save raw file after ICA correction
    preprocessed_file_path = data_preprocesed_directory + '/' + nip + '/' + nip + '_preprocessed_raw.fif'
    raw.save(preprocessed_file_path, overwrite=True, verbose=True)        
    del raw


