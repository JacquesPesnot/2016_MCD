# -*- coding: utf-8 -*-

import numpy as np
from MCD_model import *
import scipy.io as sio

###############################################################################
################################ FUNCTIONS  ###################################
###############################################################################

def compressArray(array, input_freq, output_freq):
    duration = round(len(array[0])*1000./float(input_freq))/1000.
    n = int(duration * output_freq)
    # array = np.concatenate((array, np.zeros(n - len(array)%n)))
    first = array[0][0:(len(array[0]) - len(array[0])%n)]
    first = np.reshape(first, (n, len(first)/n))
    first = np.sum(first, axis=1)
    second = array[1][0:(len(array[1]) - len(array[1])%n)]
    second = np.reshape(second, (n, len(second)/n))
    second = np.sum(second, axis=1)
    return [first, second]

def importStimuli(stim_path, name, start=0., stop=0., stim_freq=44100, meg_freq=200., MCDvalues=True):
    # Remember that stim arrays are built in that way: [auditory_array ; visual_array]
    # The auditory array we are looking for is in the first row of the array of the variable 'key'
    # For example auditory array for CCC is in the temp['CCCa'][0]
    stim = sio.loadmat(stim_path)
    stim = stim[name]

    # Compute MCD values
    MCD_corr, MCD_lag, MCD_corr_signal, MCD_lag_signal, MCD_aud_signal, MCD_vis_signal = int(), int(), [], [], [], []
    temp = np.concatenate((np.zeros((2, 7*stim_freq)), stim, np.zeros((2, 7*stim_freq))), axis=1) # Embed stimulus in 7 seconds of silence
    if MCDvalues:
        # Compute MCD values
        MCD_corr, MCD_lag, MCD_corr_signal, MCD_lag_signal, MCD_aud_signal, MCD_vis_signal = MCD_model(temp, stim_freq)
    
    # Compress arrays so that every one is at meg_freq Hz
    stim = np.concatenate((np.zeros((2, np.abs(start)*stim_freq)), stim, np.zeros((2, stop*stim_freq))), axis=1) # Fill the stimulus with zeros to go up to 'end'
    stim = compressArray(stim, stim_freq, meg_freq)
    if MCDvalues:
        MCD_corr_signal, MCD_lag_signal = compressArray([MCD_corr_signal, MCD_lag_signal], stim_freq, meg_freq)
        MCD_aud_signal, MCD_vis_signal = compressArray([MCD_aud_signal, MCD_vis_signal], stim_freq, meg_freq)

    # Shorten arrays to have values from 'start' to 'end' seconds
    if MCDvalues:
        end = np.int((1 + stop) * meg_freq) # stop in seconds
        begin = np.int(np.abs(start) * meg_freq) # start in seconds
        MCD_corr_signal = MCD_corr_signal[(7*meg_freq - begin):(7*meg_freq + end)]
        MCD_lag_signal = MCD_lag_signal[(7*meg_freq - begin):(7*meg_freq + end)]
        MCD_aud_signal = MCD_aud_signal[(7*meg_freq - begin):(7*meg_freq + end)]
        MCD_vis_signal = MCD_vis_signal[(7*meg_freq - begin):(7*meg_freq + end)]

    # Return structured dictionnaire
    return dict(signals = dict(audio = stim[0], visual = stim[1]),
                MCD_corr = MCD_corr, MCD_lag = MCD_lag,
                MCD_corr_signal = MCD_corr_signal, 
                MCD_lag_signal = MCD_lag_signal, 
                MCD_aud_signal = MCD_aud_signal, 
                MCD_vis_signal = MCD_vis_signal, freq=meg_freq)


def importRaw(nip):
    import mne 
    import os
    import glob
    
    # Import my modules
    import sys
    my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
    sys.path.append(my_module_path)
    from sharedTools.config import *
    
    # Directories to use
    data_preprocessed_directory = returnPreProcessedDirectory()
    nip_path = data_preprocessed_directory + nip + '/'
        
    # Load raw files 
    filePath = glob.glob(nip_path + nip + '_preprocessed_raw.fif') # Multiple files
    raw = mne.io.Raw(filePath, preload=True)
    return raw


def importEvents(raw, nip):
    import mne 
    import os
    
    # Import my modules
    import sys
    my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
    sys.path.append(my_module_path)
    from sharedTools.buildEvents import *
    from sharedTools.config import *
    
    stim_directory = returnStimuliDirectory()    
    stim_path = stim_directory + nip + '/'
    
    # Find events
    events = mne.find_events(raw, stim_channel=['STI101'], output='onset', 
                             consecutive=True, min_duration=0.1) # Find trigger timing
    events = addArtificialEvents(events, stim_path) # Add events (bips and flashs)
    
    return events

