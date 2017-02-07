# -*- coding: utf-8 -*-

import mne 
import os
from mne.report import Report
from mne.minimum_norm import (apply_inverse, read_inverse_operator)
from surfer import Brain


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
report = Report('Source reconstruction', verbose=False)

# Get the evoked directory
data_evoked_directory = returnEvokedDirectory() + '/stimulus_locked/'
data_mri_directory = returnMRIDirectory()

###############################################################################
############################# SOURCE EXTRACTION ###############################
###############################################################################

def time_label(t):
    return 'time=%0.2f ms' % (t * 1e3)

stimulus_names = ['DD', 'DC', 'CC', 'AA', 'AV', 'VV']
bloc_names = ['Auditory', 'Visual', 'Causality', 'Temporal']

method = 'dSPM'
snr = 3.
lambda2 = 1./snr ** 2

colormap = 'hot'
fmin, fmax = [0, 15]
fmid = int((fmin + fmax) / 2.)

times = np.arange(-0.1, 1.5, 0.1) # Timing of the source time course (shouldn't be too big)

for nip in nips:    
    for bloc in bloc_names:
        for stimulus in stimulus_names:

            ###################################################################
            ########################### Importation ###########################
            ###################################################################

            # Evoked responses            
            fname = data_evoked_directory + bloc + '/' + nip + '/' + stimulus
            evoked = mne.Evoked(fname + '-ave.fif')

            # Corresponding inverse operator
            inverse_operator = read_inverse_operator(fname + '-inv.fif')
            
            ###################################################################
            ######################### Source estimation #######################
            ###################################################################
            
            stc = apply_inverse(evoked, inverse_operator, lambda2, 
                                method=method, pick_ori=None)

            ###################################################################
            ########################### Visualization #########################
            ###################################################################
            
            # We need to separate right and left hemisphere
            stc_data = dict()
            stc_data['lh'] = stc.data[:len(stc.lh_vertno)]
            stc_data['rh'] = stc.data[-len(stc.rh_vertno):]
            
            # We need the nb of vertices in both hemisphere
            stc_vertices = dict()
            stc_vertices['lh'] = stc.lh_vertno
            stc_vertices['rh'] = stc.rh_vertno
                                      
            # We also need the timing of each hemisphere
            fig_temp = {'lh':[], 'rh':[]} # Figure arrays to plot with imshow()
            time_array = np.linspace(stc.tmin, stc.tmin + stc.data.shape[1] * stc.tstep,
                               stc.data.shape[1], endpoint=False) # Time array

            for hemi in ['lh', 'rh']:
                # Plot the blanck hemisphere
                brain = Brain(nip, hemi, 'inflated', size=(800, 400), 
                              subjects_dir=data_mri_directory)

                # Add source time course
                brain.add_data(stc_data[hemi], colormap=colormap, 
                               vertices=stc_vertices[hemi], smoothing_steps=10, 
                               time=time_array, time_label=time_label, 
                               hemi=hemi, initial_time=0.)
                  
                # Scale the F-map                         
                brain.scale_data_colormap(fmin=fmin, fmid=fmid, fmax=fmax,
                                          transparent=True)

                # Add the image array to all images                
                for time in times:
                        brain.set_time(time)
                        fig_temp[hemi].append(brain.save_montage(filename=None, 
                                                                 orientation='h'))

                fig_temp[hemi] = np.concatenate(fig_temp[hemi], axis=0)
                brain.close()


            # Correct for different lengths
            min_len = min(len(fig_temp['lh']), len(fig_temp['rh']))
            fig_temp['lh'] = fig_temp['lh'][0:min_len, :, :]
            fig_temp['rh'] = fig_temp['rh'][0:min_len, :, :]
            
            # Collapse hemispheric images into one
            fig_array = np.concatenate([fig_temp['lh'], fig_temp['rh']], axis=1)
            
            # Plot figure and save it to report
            fig, ax = subplots(figsize=(20, len(times) * 2))
            ax.imshow(fig_array)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            report.add_figs_to_section(fig, section=nip,
                                       captions=bloc + ' - ' + stimulus)

                       
        # Save HTML report                   
        report.save(os.getcwd() + '/4_sourceReconstruction.html', overwrite=True, 
                    open_browser=False)
                

