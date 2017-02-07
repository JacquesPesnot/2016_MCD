# -*- coding: utf-8 -*-

import mne 
import os
import glob
from mne.preprocessing import ICA
from mne.report import Report
from mne.io.pick import _picks_by_type as picks_by_type

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *

###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

if 'raw' in locals(): del raw

# Directories to use
data_sss_directory = returnSSSDirectory()
data_ica_directory = returnICADirectory()

# NIPs of subjects
nips = returnNips()
nips = ['Mb160304']
# ICA parameters
n_components, method, decim, random_state = returnICAParameters()

# Bad EEG channels
bad_EEG = returnBadEEG()

# Rejection limits
reject = returnRejectLimits()

# Open html report
report = Report('ICA Processing', verbose=False)


###############################################################################
############################### ICA PER SUBJECT ###############################
###############################################################################

for nip in nips:
    
    nip_path = data_sss_directory + nip + '/'

    # Load raw (problem with MISC005 not present)
    for filePath in glob.glob(nip_path + '*sss_raw.fif'):
        temp = mne.io.Raw(filePath, preload=True, add_eeg_ref=False)
        if 'MISC005' in temp.ch_names and nip in ['vV100048', 'Pb160320']:
            temp.drop_channels(['MISC005'])
        if not 'raw' in locals():
            raw = temp
        else:
            raw.append(temp)

    # Filter data
    raw.info['bads'] = bad_EEG[nip]
    raw.filter(1., 40., n_jobs=-1)


    ###########################################################################
    ####################### Cycle across channel type #########################
    ########################################################################### 
    for ch_type, picks in picks_by_type(raw.info, meg_combined=True):
        
        # Apply ICA
        ica = ICA(n_components=n_components, method=method, random_state=random_state)
        # Fit it to the data we have
        ica.fit(raw, picks=picks, decim=decim, reject=reject[ch_type])

        # Plot ICA components location        
        for figure in ica.plot_components():
            report.add_figs_to_section(figure, captions=(ch_type.upper() + ' - ICA Components'),
                                   section=nip)

        # Save ICA
        ica.save(data_ica_directory + nip + '/' + nip + '_' + ch_type + '-ica.fif')
        report.save(os.getcwd() + '/2_computeICA.html', overwrite=True, 
                    open_browser=False)
    
    del ica, raw


# Save report
report.save(os.getcwd() + '/2_computeICA.html', overwrite=True, 
            open_browser=False)
