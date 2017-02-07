# -*- coding: utf-8 -*-

import numpy as np
from config import (returnStimuli, 
                    returnTriggerCode)

''' This script is a function that return the events of the MEG raw data. It
also add a lot of 'artificial' events, corresponding to the apparition of bips
and flashs.
'''


def addEvents(events, events_to_add):
    if events_to_add == None:
        return events
    return np.concatenate((events, events_to_add), axis=0)


def findTimingStimulus(stim_onset, stim_signal, stim_trigger_value):
    # Find events time
    event_to_add = np.where(stim_signal == 1)
    if len(event_to_add[0]) == 0:
        return

    # Convert to 'event-like' array
    timing = np.transpose(event_to_add) + stim_onset
    previous_trigger = np.transpose([np.zeros(len(event_to_add[0]))]) # Wathever
    present_trigger = np.transpose([np.ones(len(event_to_add[0]))*stim_trigger_value])
    
    # Return array
    event_to_add = np.concatenate((timing, previous_trigger, present_trigger), axis=1)
    event_to_add = event_to_add.astype(int)
    return event_to_add


def addBipFlash(events, events_of_interest, bloc, trigger_code, stim_dict):  
    # Find stim-events
    temp = events[:]
    for event in events:
        if event[2] in events_of_interest.values():
            bips = findTimingStimulus(event[0], 
                                      stim_dict[event[2]]['signals']['audio'], 
                                      trigger_code[bloc + '/bip'])
            flashs = findTimingStimulus(event[0], 
                                        stim_dict[event[2]]['signals']['visual'], 
                                        trigger_code[bloc + '/flash'])
            temp = addEvents(temp, bips)
            temp = addEvents(temp, flashs)
    return temp
          

def addArtificialEvents(events, stim_path):
    # Add events corresponding to bips and flashs
    # If block is e.g. Causality, add every Causality/bip and Causality/flash
    blocs = ['Causality', 'Temporal', 'Visual', 'Auditory']
    trigger_code = returnTriggerCode()
    stim_dict = returnStimuli(MCDvalues=False, stim_path=stim_path)
    
    for bloc in blocs:
        # Operate only on events that corresponds to the block
        events_of_interest = {k: v for k, v in trigger_code.iteritems() 
                              if k.split('/')[0] == bloc and v < 70}
        events = addBipFlash(events, events_of_interest, bloc, trigger_code, 
                             stim_dict)
    return events

    
    

