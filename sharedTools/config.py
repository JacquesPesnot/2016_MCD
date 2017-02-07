# -*- coding: utf-8 -*-

import os

###############################################################################
#################################### PATHS ####################################
###############################################################################

def getParentDirectory(deepness=1):
    return os.path.sep.join(os.getcwd().split(os.path.sep)[:-deepness])

def returnRAWDirectory():
    return getParentDirectory() + '/data/meg/raw/'

def returnSSSDirectory():
    return getParentDirectory() + '/data/meg/sss/'

def returnICADirectory():
    return getParentDirectory() + '/data/meg/ica/'

def returnPreProcessedDirectory():
    return getParentDirectory() + '/data/meg/preprocessed/'

def returnEvokedDirectory():
    return getParentDirectory() + '/data/meg/evoked/'

def returnCoregistrationDirectory():
    return getParentDirectory() + '/data/coregistration/'

def returnMRIDirectory():
    return getParentDirectory() + '/data/mri/'

def returnForwardDirectory():
    return getParentDirectory() + '/data/forward_model/'

def returnStimuliDirectory(deepness=2):
    return getParentDirectory() + '/data/stimuli/'

###############################################################################
#################################### NIPS #####################################
###############################################################################

def returnNips():
    return ['Ab140232', 'Jl150443', 'Mm150194', 
            'Mp110340', 'Rt160359', 'Cb140229', 'Al150424', 'Cc160310',
            'Lb160367', 'Mb160304', 'Mk150295', 'Sl160372', 'Mp150285']
#'Ai160065', 'Cd130323'
###############################################################################
################################# BAD CHANNELS ################################
###############################################################################

def returnBadMEG():
    return dict(vV100048 = ['MEG0113', 'MEG0413', 'MEG0522', 'MEG2321'], 
                Pb160320 = ['MEG0123', 'MEG0813', 'MEG0812', 'MEG0822', 
                            'MEG0823', 'MEG1813', 'MEG0913', 'MEG0912', 
                            'MEG1122', 'MEG1222', 'MEG0523', 'MEG0811', 
                            'MEG0821', 'MEG0911'],
                Ab140232 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Ai160065 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Cd130323 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Jl150443 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Mm150194 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Mp110340 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Rt160359 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Cb140229 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Al150424 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Cc160310 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'],
                Lb160367 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Mb160304 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Mk150295 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Sl160372 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'], 
                Mp150285 = ['MEG0713', 'MEG0932', 'MEG2442', 'MEG0813', 'MEG1122'])

def returnBadEEG():
    return dict(vV100048 = [], 
                Pb160320 = ['EEG001', 'EEG002', 'EEG025', 'EEG035', 'EEG043',
                            'EEG044', 'EEG008', 'EEG060', 'EEG018', 'EEG064'], 
                Ab140232 = [], 
                Ai160065 = [],
                Cd130323 = [],
                Jl150443 = [],
                Mm150194 = [],
                Mp110340 = [],
                Rt160359 = [],
                Cb140229 = [], 
                Al150424 = [],
                Cc160310 = [],
                Lb160367 = [], 
                Mb160304 = [], 
                Mk150295 = [], 
                Sl160372 = [], 
                Mp150285 = [])

###############################################################################
############################### ICA PARAMETERS  ###############################
###############################################################################

def returnICAParameters():
    n_components = .9999  # no more than number of channels
    method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
    decim = 3 # we need sufficient statistics, not all time points -> saves time
    random_state = 23
    return n_components, method, decim, random_state

def returnRejectLimits():
    return dict(meg = dict(mag=10e-12, grad=500e-12), 
                eeg = dict(eeg=3000e-6)) #300e-6

def returnResampFreq():
    return 200.

###############################################################################
############################## BAD ICA COMPONENTS #############################
###############################################################################

def returnBadICA():
    return dict(Pb160320 = 
                      dict(eeg = 
                           dict(eog = [],
                                ecg = [],
                                others = []),
                           meg = 
                           dict(eog1 = [],
                                eog2 = [],
                                ecg = [],
                                others = [])),
                Ab140232 = 
                      dict(meg = 
                           dict(eog = [1, 5, 9],
                                ecg = [36, 65],
                                others = [])),

                Jl150443 = 
                      dict(meg = 
                           dict(eog = [1, 2, 5],
                                ecg = [41, 59],
                                others = [])),

                Mm150194 = 
                      dict(meg = 
                           dict(eog = [1],
                                ecg = [29, 30, 50, 69],
                                others = [])),

                Rt160359 = 
                      dict(meg = 
                           dict(eog = [6],
                                ecg = [2, 3, 51],
                                others = [])),

                 vV100048 = 
                     dict(meg = 
                          dict(eog1 = [], 
                               eog2 = [], 
                               ecg = [], 
                               others = [])))
               
###############################################################################
################################# TRIGGER CODE ################################
###############################################################################                

def returnTriggerCode():
    return {'Causality/DD':11,
            'Causality/DC':12,
            'Causality/CC':13,
            'Causality/AA':14,
            'Causality/AV':15,
            'Causality/VV':16,
            'Temporal/DD':21,
            'Temporal/DC':22,
            'Temporal/CC':23,
            'Temporal/AA':24,
            'Temporal/AV':25,
            'Temporal/VV':26,
            'Auditory/DD':41,
            'Auditory/DC':42,
            'Auditory/CC':43,
            'Auditory/AA':44,
            'Auditory/AV':45,
            'Auditory/VV':46,
            'Visual/DD':51,
            'Visual/DC':52,
            'Visual/CC':53,
            'Visual/AA':54,
            'Visual/AV':55,
            'Visual/VV':56,
            # Artificial trigger (added manually)
            'Causality/bip':70, 
            'Causality/flash':71,
            'Temporal/bip':72,
            'Temporal/flash':73,
            'Auditory/bip':76,
            'Auditory/flash':77, 
            'Visual/bip':78,
            'Visual/flash':79}


def returnStimuli(stim_path, MCDvalues=True, meg_freq=None, start=-.2, stop=1.8):
    from sharedTools.importFunctions import *
    if meg_freq is None:
        meg_freq = returnResampFreq()
    
    # Define name of the bloc stimulus directory
    stim_path_bloc = {'Causality':'main/', 
                  'Temporal':'main/',
                  'Auditory':'auditory_localizer/', 
                  'Visual':'visual_localizer/'}
                  
    # Define extension of the bloc stimulus name 
    stim_extension_bloc = {'Causality':'', 
                  'Temporal':'', 
                  'Auditory':'a', 
                  'Visual':'v'}
                  
    stimuli = dict()
    # Build the stimulus dict that contain streams of events and MCD associated values
    for key, value in returnTriggerCode().iteritems():
        bloc = key.split('/')[0] # Get the bloc name
        item = key.split('/')[-1] # Get the stimulus name
        fullname = item + stim_extension_bloc[bloc] # Get extension
        # Get stim path associated to bloc name
        path = stim_path + stim_path_bloc[bloc] + item
        if os.path.isfile(path + '.mat'):
            print 'Computing stimulus ' + bloc + ' - ' + item + ' ...'
            stim_dict = importStimuli(path, fullname, MCDvalues=MCDvalues, 
                                      meg_freq=meg_freq, start=start, stop=stop-1)
            stimuli[value] = stim_dict # Add to big dict
    
    return stimuli



