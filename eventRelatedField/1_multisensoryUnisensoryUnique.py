# -*- coding: utf-8 -*-

import mne 
import os
import glob
from mne.report import Report

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

###############################################################################
################################ FUNCTIONS ####################################
###############################################################################


def collapseEvoked(modality):
    # This dictionnary will be fill with evoked response to auditory stimuli in
    # different conditions. Modality can be 'bip' or 'flash'
    evoked_dict = {}
    
    # There is no bips in 'Visual' blocs so we build different set of blocs
    blocs = (['Causality', 'Temporal', 'Auditory'] if modality == 'bip' else
             ['Causality', 'Temporal', 'Visual'])
    
    times = np.arange(-0.1, 1., 0.1)
    
    for bloc in blocs:
        # Extract epochs
        events_to_average = returnTriggerCode()[bloc + '/' + modality]
        temp_events = events[events[:,2] == events_to_average,:] # Eliminate doublons
        epochs = mne.Epochs(raw, temp_events, events_to_average, reject=reject,
                            tmin=-0.2, tmax=1.8, picks=picks, baseline=(None, 0))
        
        # Compute evoked response
        evoked = epochs.average()
        
        # Add it to the dictionnary
        evoked_dict[bloc] = evoked
        
        # Plot it 
        report.add_figs_to_section(evoked.plot(), section=nip, captions=bloc + ' - Auditory evoked fields')
        report.add_figs_to_section(evoked.plot_topomap(times=times),
                                   section=nip, captions=bloc + 'Topomap')
    
    return evoked_dict


def comparativePlot(evoked_dict, section=None, captions=None, colors=colors):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax = mne.viz.plot_compare_evokeds(evoked_dict, truncate_yaxis=False, 
                                      show=False, axes=ax, colors=colors)

    report.add_figs_to_section(fig, section=nip, captions=captions)
   



###############################################################################
############################# SUBJECTS ANALYSIS ###############################
###############################################################################

# Open html report 
report = Report('Mutlisensory vs Unisensory evoked response', verbose=False)

group_evoked_dict_aud = {'Causality':[], 'Temporal':[], 'Auditory':[]}
group_evoked_dict_vis = {'Causality':[], 'Temporal':[], 'Visual':[]}

for nip in nips:
    
    ###########################################################################
    ####################### Import preprocessed data ##########################
    ###########################################################################

    raw = importRaw(nip)
    events = importEvents(raw, nip)

    ###########################################################################
    ########################## Cycle across blocs #############################
    ###########################################################################

    # Parameters of rejection
    reject = {'mag':8e-12, 'grad':600e-12}
    picks = mne.pick_types(raw.info, eeg=False, eog=False, meg=True)

    # Build dictionnary of evoked response, one auditory and one visual
    auditory_evoked_dict = collapseEvoked('bip')
    visual_evoked_dict = collapseEvoked('flash')
    
    # Add them for group analysis
    group_evoked_dict_aud['Causality'].append(auditory_evoked_dict['Causality'])
    group_evoked_dict_aud['Temporal'].append(auditory_evoked_dict['Temporal'])
    group_evoked_dict_aud['Auditory'].append(auditory_evoked_dict['Auditory'])
    group_evoked_dict_vis['Causality'].append(visual_evoked_dict['Causality'])
    group_evoked_dict_vis['Temporal'].append(visual_evoked_dict['Temporal'])
    group_evoked_dict_vis['Visual'].append(visual_evoked_dict['Visual']) 

    # Plot to compare different conditions
    colors = dict(Causality="b", Temporal="r", Auditory="g")
    comparativePlot(auditory_evoked_dict, section=nip, colors=colors,
                    captions='Multisensory/Unisensory - Auditory ERF')
    colors = dict(Causality="b", Temporal="r", Visual="m")
    comparativePlot(visual_evoked_dict, section=nip, colors=colors, 
                    captions='Multisensory/Unisensory - Visual ERF')

                     
    # Save HTML report                   
    report.save(os.getcwd() + '/1_mutlisensoryUnisensoryERF.html', overwrite=True, 
                open_browser=False)



###############################################################################
############################### GROUP ANALYSIS ################################
###############################################################################

# Open html report 
report = Report('Mutlisensory vs Unisensory evoked response - group', verbose=False)
'''
blocs = ['Causality', 'Temporal', 'Auditory']
    
times = np.arange(-0.1, 1., 0.1)
    
for bloc in blocs:

    evoked = group_evoked_dict_aud[bloc]
    
    # Plot it 
    report.add_figs_to_section(evoked.plot(), section=nip, captions=bloc + ' - Auditory evoked fields')
    report.add_figs_to_section(evoked.plot_topomap(times=times),
                               section=nip, captions=bloc + 'Topomap')

report.add_figs_to_section(evoked.plot(), section=nip, captions=bloc + ' - Auditory evoked fields')

'''
# Plot to compare different conditions
colors = dict(Causality="b", Temporal="r", Auditory="g")
comparativePlot(group_evoked_dict_aud, section='GROUP', colors=colors,
                captions='Multisensory/Unisensory - Unique Auditory ERF - Groupe')

colors = dict(Causality="b", Temporal="r", Visual="m")
comparativePlot(group_evoked_dict_vis, section='GROUP', colors=colors,
                captions='Multisensory/Unisensory - Unique Visual ERF - Groupe')

# Save HTML report                   
report.save(os.getcwd() + '/1_mutlisensoryUnisensoryERF_Group.html', overwrite=True, 
            open_browser=False)
