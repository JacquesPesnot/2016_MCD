
    ###########################################################################
    ###################### Find best activated sensors ########################
    ###########################################################################

    best_sensors = {k: {'Auditory':[], 'Visual':[]} for k in stimulus_names}
    for stimulus_name in stimulus_names:
        for bloc in ['Auditory', 'Visual']:
            # Take the mean absolute value and find the best activated sensors
            evoked_temp = evoked_dict[stimulus_name][bloc]
            evoked_temp.data = np.abs(evoked_temp.data) # Absolute value
            evoked_temp.data = np.mean(evoked_temp.data, 1) # Mean values
            highest_values = np.sort(evoked_temp.data)[-20:] # Take 20 highest values
            for value in highest_values:
                sensor_index = np.where([evoked_temp.data == value])[1][0] # Find the corresponding index
                sensor_name = evoked_temp.ch_names[sensor_index] # Find the corresponding sensors
                best_sensors[stimulus_name][bloc].append(sensor_name) # Save it to the dictionnary

    print best_sensors
