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
report = Report('EOG/ECG/MISC artifacts automatic rejection', verbose=False)


###############################################################################
####################### ARTIFACTS REJECTION PER SUBJECT  ######################
###############################################################################

for nip in nips:

    nip_path = data_sss_directory + '/' + nip + '/'
    
    # Load raw data (problem with MISC005 not present)
    for filePath in glob.glob(nip_path + '*sss_raw.fif'):
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
        
        # Load ICA        
        ica = read_ica(data_ica_directory + nip + '/' + nip + '_' + ch_type + '-ica.fif')
        reject = rejectDict[ch_type]
 
        #######################################################################
        ########################## Reject ECG artifacts #######################
        #######################################################################
        if 'ECG064' in raw.ch_names:
            # Choose good channels (ch_types + ecg)
            picks_ecg = np.concatenate([picks, mne.pick_types(raw.info, meg=False, 
                                                              eeg=False, ecg=True, 
                                                              eog=False)])
            # Create ecg-based epochs   
            ecg_epochs = create_ecg_epochs(raw, reject=reject, picks=picks_ecg, 
                                           baseline = (None, 0))
            ecg_average = ecg_epochs.average()
            # Find ecg artifacts based on correlation between ICA and ECG063
            ecg_inds, scores = ica.find_bads_ecg(ecg_epochs)
    
            # Plot r score
            report.add_figs_to_section(ica.plot_scores(scores, exclude=ecg_inds), 
                                       captions=ch_type.upper() + ' - ECG - ' + 'R scores',
                                       section=nip)
                                       
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_sources(ecg_average, exclude=ecg_inds), 
                                       captions=ch_type.upper() + ' - ECG - ' + 'Sources time course',
                                       section=nip)
                                       
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_overlay(ecg_average, exclude=ecg_inds), 
                                       captions=ch_type.upper() + ' - ECG - ' + 'Corrections',
                                       section=nip)
                                   
        else:
            ecg_inds = returnBadICA()[nip]['meg']['ecg']
            
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_overlay(raw, exclude=ecg_inds, start=20000, stop=25000), 
                                       captions=ch_type.upper() + ' - ECG - ' + 'Corrections',
                                       section=nip)

        # Reject bad ICA                               
        raw = ica.apply(raw, exclude=(ecg_inds))
        # Save HTML report                   
        report.save(os.getcwd() + '/3_rejectArtifactsAutomatically.html', 
                    overwrite=True, open_browser=False)

        
        #######################################################################
        ########################## Reject EOG artifacts #######################
        #######################################################################
        if 'EOG062' in raw.ch_names:
            # Choose good channels (ch_types + eog)
            picks_eog = np.concatenate([picks, mne.pick_types(raw.info, meg=False, 
                                                              eeg=False, ecg=False, 
                                                              eog=True)])
            # Create eog-based epochs                                                      
            eog_epochs = create_eog_epochs(raw, reject=reject, picks=picks_eog, 
                                           baseline = (None, 0))
            eog_average = eog_epochs.average()
            # Find eog artifacts based on correlation between ICA and EOG061/EOG062
            eog_inds, scores = ica.find_bads_eog(eog_epochs)

            # Plot r score
            report.add_figs_to_section(ica.plot_scores(scores, exclude=eog_inds), 
                                       captions=ch_type.upper() + ' - EOG - ' + 'R scores',
                                       section=nip)
                                       
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_sources(eog_average, exclude=eog_inds), 
                                       captions=ch_type.upper() + ' - EOG - ' + 'Sources time course',
                                       section=nip)
                                       
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_overlay(eog_average, exclude=eog_inds), 
                                       captions=ch_type.upper() + ' - EOG - ' + 'Corrections',
                                       section=nip)
                                       
        else:
            eog_inds = returnBadICA()[nip]['meg']['eog']
            
            # Plot source time course                            
            report.add_figs_to_section(ica.plot_overlay(raw, exclude=eog_inds, start=20000, stop=25000), 
                                       captions=ch_type.upper() + ' - EOG - ' + 'Corrections',
                                       section=nip)
                                       
        # Reject bad ICA                               
        raw = ica.apply(raw, exclude=(eog_inds))
        # Save HTML report                          
        report.save(os.getcwd() + '/3_rejectArtifactsAutomatically.html', 
                    overwrite=True, open_browser=False)

        
        #######################################################################
        ##################### Reject head-speaker artifacts ###################
        #######################################################################
       
        # Choose good channels (ch_types + misc)
        picks_misc = np.concatenate([picks, mne.pick_types(raw.info, misc=True, meg=False)])
        # Create misc-based epochs   
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                       baseline = (None, 0), ch_name='MISC004')
        misc_average = misc_epochs.average()
        # Find misc artifacts based on correlation between ICA and MISC004
        misc4_inds, scores = find_bads_misc(ica, misc_epochs, ch_name='MISC004')

        # Plot r score
        report.add_figs_to_section(ica.plot_scores(scores, exclude=misc4_inds), 
                                   captions=ch_type.upper() + ' - MISC004 - ' + 'R scores',
                                   section=nip)
                                   
        # Plot source time course                            
        report.add_figs_to_section(ica.plot_sources(misc_average, exclude=misc4_inds), 
                                   captions=ch_type.upper() + ' - MISC004 - ' + 'Sources time course',
                                   section=nip)
                                   
        # Plot source time course                            
        report.add_figs_to_section(ica.plot_overlay(misc_average, exclude=misc4_inds), 
                                   captions=ch_type.upper() + ' - MISC004 - ' + 'Corrections',
                                   section=nip)

        # Reject bad ICA                               
        raw = ica.apply(raw, exclude=(misc4_inds))
        # Save HTML report                   
        report.save(os.getcwd() + '/3_rejectArtifactsAutomatically.html', 
                    overwrite=True, open_browser=False)


        #######################################################################
        ########################## Reject LED artifacts #######################
        #######################################################################
       
        # Choose good channels (ch_types + misc)
        picks_misc = np.concatenate([picks, mne.pick_types(raw.info, misc=True, meg=False)])
        # Create misc-based epochs   
        misc_epochs = create_misc_epochs(raw, reject=reject, picks=picks_misc, 
                                       baseline = (None, 0), ch_name='MISC005', 
                                       event_id=998)
        misc_average = misc_epochs.average()
        # Find misc artifacts based on correlation between ICA and MISC004
        misc5_inds, scores = find_bads_misc(ica, misc_epochs, ch_name='MISC005')

        # Plot r score
        report.add_figs_to_section(ica.plot_scores(scores, exclude=misc5_inds), 
                                   captions=ch_type.upper() + ' - MISC005 - ' + 'R scores',
                                   section=nip)
                                   
        # Plot source time course                            
        report.add_figs_to_section(ica.plot_sources(misc_average, exclude=misc5_inds), 
                                   captions=ch_type.upper() + ' - MISC005 - ' + 'Sources time course',
                                   section=nip)
                                   
        # Plot source time course                            
        report.add_figs_to_section(ica.plot_overlay(misc_average, exclude=misc5_inds), 
                                   captions=ch_type.upper() + ' - MISC005 - ' + 'Corrections',
                                   section=nip)

        # Reject bad ICA                               
        raw = ica.apply(raw, exclude=(misc5_inds))

        # Save HTML report                   
        report.save(os.getcwd() + '/3_rejectArtifactsAutomatically.html', 
                    overwrite=True, open_browser=False)

        
        '''
        #######################################################################
        ######################## Apply ICA, save and close ####################
        #######################################################################
        exclude_ICA = (eog_inds + ecg_inds + misc4_inds + misc5_inds)
        exclude_ICA = np.unique(np.hstack(exclude_ICA))# Eliminate doublons 
        exclude_ICA = np.ndarray.tolist(exclude_ICA)   # Convert to python list
        raw = ica.apply(raw, exclude=(exclude_ICA))
        '''

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
    del ica, raw


