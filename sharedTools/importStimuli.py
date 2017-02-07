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

def importStimuli(stim_path, name, offset=0, stim_freq=44100, meg_freq=200., MCDvalues=True):
    # Remember that stim arrays are built in that way: [auditory_array ; visual_array]
    # The auditory array we are looking for is in the first row of the array of the variable 'key'
    # For example auditory array for CCC is in the temp['CCCa'][0]
    stim = sio.loadmat(stim_path)
    stim = stim[name]

    # Compute MCD values
    MCD_corr, MCD_lag, MCD_corr_signal, MCD_lag_signal = [], [], int(), int()
    temp = np.concatenate((np.zeros((2, 7*stim_freq)), stim, np.zeros((2, 7*stim_freq))), axis=1) # Embed stimulus in 7 seconds of silence
    if MCDvalues:
        # Compute MCD values
        MCD_corr, MCD_lag, MCD_corr_signal, MCD_lag_signal = MCD_model(temp, stim_freq)

    # Compress arrays so that every one is at meg_freq Hz
    end = np.int(len(stim[0])/float(stim_freq) + offset) # offset in seconds
    stim = np.concatenate((stim, np.zeros((2, offset*stim_freq))), axis=1) # Fill the stimulus with zeros to go up to 'end'
    stim = compressArray(stim, stim_freq, meg_freq)
    if MCDvalues:
        MCD_corr_signal, MCD_lag_signal = compressArray([MCD_corr_signal, MCD_lag_signal], stim_freq, meg_freq)

    # Shorten arrays to have values from 'start' to 'end' seconds
    if MCDvalues:
        MCD_corr_signal = MCD_corr_signal[7*meg_freq:(7*meg_freq + end*meg_freq)]
        MCD_lag_signal = MCD_lag_signal[7*meg_freq:(7*meg_freq + end*meg_freq)]

    # Return structured dictionnaire
    return dict(signals = dict(audio = stim[0], visual = stim[1]),
                MCD_corr = MCD_corr, MCD_lag = MCD_lag,
                MCD_corr_signal = MCD_corr_signal, 
                MCD_lag_signal = MCD_lag_signal, freq=meg_freq)

