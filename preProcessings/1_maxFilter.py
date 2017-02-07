# -*- coding: utf-8 -*-

import mne
import os
import glob
import numpy as np
from mne.report import Report
from mne.preprocessing import maxwell_filter

# Import my modules
import sys
my_module_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])
sys.path.append(my_module_path)
from sharedTools.config import *


###############################################################################
########################## IMPORTATION PARAMETERS  ############################
###############################################################################

# Directories to use
data_raw_directory = returnRAWDirectory()
data_sss_directory = returnSSSDirectory()
cal_path = '/home/vv221713/Documents/MCD_Jacques_2016/analysis/data/utils/sss_cal.dat'
ct_path = '/home/vv221713/Documents/MCD_Jacques_2016/analysis/data/utils/ct_sparse.fif'

# NIPs of subjects
nips = returnNips()
nips = ['Ab140232']

# Bad MEG channels
bad_MEG = returnBadMEG()

# Bad EEG channels
bad_EEG = returnBadEEG()


###############################################################################
####################### FIND THE BEST HEAD REFERENCE  #########################
###############################################################################

def findRefrun(directory=0):
	
	# Current directory
	if directory == 0:
		directory = os.getcwd()
	
	# List of files
	fifFiles = []
	for dirs in glob.glob(directory + '*'):
		for files in glob.glob(dirs + '/*'):
			fifFiles.append(files)

	Files_tot = len(fifFiles)
	
	if Files_tot == 1:
		print fifFiles[0]
		return fifFiles[0]
	else:
		try:
			AllCoords = np.zeros((Files_tot,3))
			for index, eachFile in enumerate(fifFiles): 
				a = "cd && "       
				b = "cd MNE-2.7.4-3415-Linux-x86_64/bin && "
				c = "chmod +x mne_show_fiff && "
				d = "export MNE_ROOT=/home/vv221713/MNE-2.7.4-3415-Linux-x86_64 && "
				e = "./mne_show_fiff --verbose --tag 222 --in " + eachFile + " | tail -n 4"
				coords = os.popen(a + b + c + d + e).read().replace(')',"").split()
				coords = coords[4:7]
				AllCoords[index,:] = np.array([float(s) for s in coords])
				 
			Average = np.mean(AllCoords, axis=0)
			Distances = np.sqrt(np.sum((AllCoords-Average)**2, axis=1))
			
			TheFile = np.array(fifFiles)[Distances == np.min(Distances)]
			TheFile = TheFile[0]
			print TheFile
			return TheFile
				
		except ValueError:
			print "Can't find any file !"
		finally:
			os.chdir(os.getcwd())



###############################################################################
############################# APPLY MAXFILTER  ################################
###############################################################################

# Define reference run for Maxfilter : all subjects the same.
refrun_path = findRefrun(data_raw_directory)

for nip in nips:

    # Open html report     
    report = Report()

    nip_path = data_raw_directory + nip + '/'
    
    # Cycle across file
    for raw_file_path in glob.glob(nip_path + '*'):
        # Verbose
        print '---------------------------------------------------------------'
        print 'Subject ' + nip
        print ('File n° ' 
               + str(glob.glob(nip_path + '*').index(raw_file_path) + 1) 
               + '/' + str(len(glob.glob(nip_path + '*'))))

        #######################################################################
        ############################### Load raw ##############################
        #######################################################################
        raw = mne.io.read_raw_fif(raw_file_path, allow_maxshield=True, 
                                  preload=True, add_eeg_ref=False)

        # Filter data                    
        raw.filter(.1, 150., l_trans_bandwidth=.05, n_jobs=-1)
        
        # Interpolate bad EEG channels
        raw.info['bads'] = bad_EEG[nip]
        raw.interpolate_bads()
        raw.info['bads'] = bad_MEG[nip]

        #######################################################################
        ############################ Maxfilter data ###########################
        #######################################################################
        sss_file_path = data_sss_directory + '/' + nip + '/' + raw_file_path.split('/')[-1]
        sss_file_path = '_sss_raw'.join(sss_file_path.split('_raw'))
        
        sss_raw = maxwell_filter(raw, calibration=cal_path,  
                                 cross_talk=ct_path, verbose=False,
                                 destination=refrun_path, 
                                 bad_condition='warning')
        sss_raw.save(sss_file_path, overwrite=True, verbose=False)
        report.add_figs_to_section(sss_raw.plot(), captions=raw_file_path, 
                                   section=nip)

        #######################################################################
        ######################## Close and save report ########################
        ####################################################################### 
        # Delete variables
        del raw, sss_raw
        
    # Save report
    report.save(os.getcwd() + '/1_maxFilter.html', overwrite=True, 
                open_browser=False)

