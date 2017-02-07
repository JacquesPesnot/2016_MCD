# -*- coding: utf-8 -*-

import mne 
import os
import glob
import numpy as np
from mne.preprocessing import read_ica
from mne.report import Report
from mne.preprocessing import create_eog_epochs, create_ecg_epochs
from mne.io.pick import _picks_by_type as picks_by_type

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *

###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

# Directories to use
data_ica_directory = returnICADirectory()
data_preprocesed_directory = returnPreProcessedDirectory()

# NIPs of subjects
nips = returnNips()
nips = ['Pb160320']
# Bad EEG channels
bad_EEG = returnBadEEG()

# Parameters for automatic rejection
rejectDict = returnRejectLimits()

# ICA components manually rejected
ica_rejects = returnBadICA()


###############################################################################
############################ ARTIFACTS REJECTION  #############################
###############################################################################

# Open html report 
report = Report('EOG/ECG artifacts manual rejection', verbose=False)

for nip in nips:

    nip_path = data_ica_directory + '/' + nip + '/'
    
    # Load raw data (already gone trough 3_rejectArtifactsAutomatically.py)
    filePath = glob.glob(nip_path + nip + '_auto_ica_sss_raw*.fif') # Multiple files
    raw = mne.io.Raw(filePath, preload=True)

    # Exclude bad EEG channels
    raw.info['bads'] = bad_EEG[nip]
    
    ###########################################################################
    ####################### Cycle across channel type #########################
    ########################################################################### 
    for ch_type, picks in picks_by_type(raw.info, meg_combined=True):
        
        # Load ICA  
        ica = read_ica(data_ica_directory + nip + '/' + nip + '_' + ch_type + '-ica.fif')
        reject = rejectDict[ch_type]

        #######################################################################
        ######################### Check EOG061 artifacts ######################
        #######################################################################
        # Choose good channels (ch_types + EOG061)
        eog_channels = mne.pick_channels_regexp(raw.info['ch_names'], 'EOG *')
        picks_eog1 = np.concatenate([picks, np.array([eog_channels[0]])]) # 382 = EOG061
        # Create eog-based epochs 
        eog_epochs = create_eog_epochs(raw, reject=reject, picks=picks_eog1, 
                                       baseline = (None, 0), ch_name='EOG061')
        eog_average = eog_epochs.average()

        if len(eog_epochs) > 0:        
            for bad_component in ica_rejects[nip][ch_type]['eog1']:
                # Plots                            
                report.add_figs_to_section(ica.plot_properties(eog_epochs, picks=[bad_component]), 
                                           captions=ch_type.upper() + ' - EOG061 - ICA n. ' + str(bad_component),
                                           section=nip)

                report.add_figs_to_section(ica.plot_overlay(eog_average, exclude=[bad_component]),
                                           captions=' ',
                                           section=nip)
    
            report.add_figs_to_section(ica.plot_overlay(eog_average, exclude=ica_rejects[nip][ch_type]['eog1']), 
                                       captions=ch_type.upper() + ' - EOG061 - All bad components',
                                       section=nip)   
    
            # Save HTML report                   
            report.save(os.getcwd() + '/4_rejectArtifactsManually.html', overwrite=True, 
                        open_browser=False)


        #######################################################################
        ######################### Check EOG062 artifacts ######################
        #######################################################################
        # Choose good channels (ch_types + EOG062)
        picks_eog2 = np.concatenate([picks, np.array([eog_channels[1]])]) # 383 = EOG062
        # Create eog-based epochs 
        eog_epochs = create_eog_epochs(raw, reject=reject, picks=picks_eog2, 
                                       baseline = (None, 0), ch_name='EOG062')
        eog_average = eog_epochs.average()
        
        if len(eog_epochs) > 0:
            for bad_component in ica_rejects[nip][ch_type]['eog2']:
                # Plots                            
                report.add_figs_to_section(ica.plot_properties(eog_epochs, picks=[bad_component]), 
                                           captions=ch_type.upper() + ' - EOG062 - ICA n. ' + str(bad_component),
                                           section=nip)

                report.add_figs_to_section(ica.plot_overlay(eog_average, exclude=[bad_component]),
                                           captions=' ',
                                           section=nip)
    
            report.add_figs_to_section(ica.plot_overlay(eog_average, exclude=ica_rejects[nip][ch_type]['eog2']), 
                                       captions=ch_type.upper() + ' - EOG062 - All bad components',
                                       section=nip)   
    
            # Save HTML report                   
            report.save(os.getcwd() + '/4_rejectArtifactsManually.html', overwrite=True, 
                        open_browser=False)


        #######################################################################
        ######################### Check ECG063 artifacts ######################
        #######################################################################
        # Choose good channels (ch_types + ECG063)
        ecg_channel = mne.pick_channels_regexp(raw.info['ch_names'], 'ECG *')
        picks_ecg = np.concatenate([picks, np.array([ecg_channel[0]])]) # 384 = ECG063
        # Create eog-based epochs 
        ecg_epochs = create_ecg_epochs(raw, reject=reject, picks=picks_ecg, 
                                       baseline = (None, 0), ch_name='ECG063')
        ecg_average = ecg_epochs.average()
        
        if len(ecg_epochs) > 0:
            for bad_component in ica_rejects[nip][ch_type]['ecg']:
                # Plots                            
                report.add_figs_to_section(ica.plot_properties(ecg_epochs, picks=[bad_component]), 
                                           captions=ch_type.upper() + ' - ECG063 - ICA n. ' + str(bad_component),
                                           section=nip)

                report.add_figs_to_section(ica.plot_overlay(ecg_average, exclude=[bad_component]),
                                           captions=' ',
                                           section=nip)
    
            report.add_figs_to_section(ica.plot_overlay(ecg_average, exclude=ica_rejects[nip][ch_type]['ecg']), 
                                       captions=ch_type.upper() + ' - ECG063 - All bad components',
                                       section=nip)   
    
            # Save HTML report                   
            report.save(os.getcwd() + '/4_rejectArtifactsManually.html', overwrite=True, 
                        open_browser=False)
        
        
        #######################################################################
        ######################### Check other artifacts #######################
        #######################################################################
        for bad_component in ica_rejects[nip][ch_type]['others']:
            # Plots                            
            report.add_figs_to_section(ica.plot_overlay(raw, exclude=[bad_component]), 
                                       captions=ch_type.upper() + ' - Others - ICA n. ' + str(bad_component),
                                       section=nip)


        # Save HTML report                   
        report.save(os.getcwd() + '/4_rejectArtifactsManually.html', overwrite=True, 
                    open_browser=False)
        

        #######################################################################
        ############################### Apply ICA  ############################
        #######################################################################
        # Get all values of 'ica_rejects' dict for this nip and this ch_type
        exclude_ICA = ica_rejects[nip][ch_type].values() # Get values
        exclude_ICA = np.unique(np.hstack(exclude_ICA))  # Eliminate doublons 
        exclude_ICA = np.ndarray.tolist(exclude_ICA)     # Convert to python list
        raw = ica.apply(raw, exclude=exclude_ICA)        # Apply ICA

    ###########################################################################
    ############################ Save cleaned data ############################
    ########################################################################### 

    # Interpolate bad EEG channels
    raw.interpolate_bads()

    # Downsample data
    raw.resample(returnResampFreq(), npad="auto")

    # Save raw file after ICA correction  
    preprocessed_file_path = data_preprocesed_directory + '/' + nip + '/' + nip + '_preprocessed_raw.fif'
    raw.save(preprocessed_file_path, overwrite=True, verbose=False)
    del ica, raw

