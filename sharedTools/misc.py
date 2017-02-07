# -*- coding: utf-8 -*-

import numpy as np
import mne
from mne.preprocessing.peak_finder import peak_finder
from mne.filter import band_pass_filter
from mne.utils import logger
from mne.epochs import Epochs
from mne import pick_types, pick_channels
from mne.preprocessing.bads import find_outliers
from scipy.signal import hilbert

def find_misc_events(raw, event_id=999, l_freq=1, h_freq=10,
                    filter_length='10s', ch_name=None, tstart=0,
                    verbose=None, first_samp=None):
    """Locate MISC artifacts
    Parameters
    ----------
    raw : instance of Raw
        The raw data.
    event_id : int
        The index to assign to found events.
    low_pass : float
        Low pass frequency.
    high_pass : float
        High pass frequency.
    filter_length : str | int | None
        Number of taps to use for filtering.
    ch_name: str | None
        If not None, use specified channel(s) for MISC
    tstart : float
        Start detection after tstart seconds.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).
    Returns
    -------
    eog_events : array
        Events.
    """

    # Getting MISC Channel
    misc_inds = _get_eog_channel_index(ch_name, raw)

    misc, _ = raw[misc_inds, :]

    if first_samp is None:
        first_samp=raw.first_samp

    misc_events = _find_misc_events(misc, event_id=event_id, l_freq=l_freq,
                                  h_freq=h_freq,
                                  sampling_rate=raw.info['sfreq'],
                                  first_samp=first_samp,
                                  filter_length=filter_length,
                                  tstart=tstart)
    misc_events = np.ndarray.astype(misc_events, int)
    return misc_events


def _find_misc_events(misc, event_id, l_freq, h_freq, sampling_rate, first_samp,
                     filter_length='10s', tstart=0.):
    """Helper function"""
    misc_events = []
    misc = np.abs(misc[0])

    mn, mx = np.Inf, -np.Inf
    mxpos = np.NaN
    x = np.arange(len(misc))
    delta = np.max(misc)/1.5
    
    lookformax = True
    
    for i in np.arange(len(misc)):
        this = misc[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
        
        if lookformax:
            if this < mx-delta:
                misc_events.append(mxpos)
                mn = this
                lookformax = False
        else:
            if this > mn+delta:
                mx = this
                mxpos = x[i]
                lookformax = True

    misc_events = np.array(misc_events)
    n_events = len(misc_events)
    logger.info("Number of MISC events detected : %d" % n_events)
    misc_events = np.c_[misc_events + first_samp, np.zeros(n_events),
                       event_id * np.ones(n_events)]
    
    return misc_events


def _get_eog_channel_index(ch_name, inst):
    if isinstance(ch_name, str):
        # Check if multiple EOG Channels
        if ',' in ch_name:
            ch_name = ch_name.split(',')
        else:
            ch_name = [ch_name]

        eog_inds = pick_channels(inst.ch_names, include=ch_name)

        if len(eog_inds) == 0:
            raise ValueError('%s not in channel list' % ch_name)
        else:
            logger.info('Using channel %s as EOG channel%s' % (
                        " and ".join(ch_name),
                        '' if len(eog_inds) < 2 else 's'))
    elif ch_name is None:

        eog_inds = pick_types(inst.info, meg=False, eeg=False, stim=False,
                              eog=True, ecg=False, emg=False, ref_meg=False,
                              exclude='bads')

        if len(eog_inds) == 0:
            logger.info('No EOG channels found')
            logger.info('Trying with EEG 061 and EEG 062')
            eog_inds = pick_channels(inst.ch_names,
                                     include=['EEG 061', 'EEG 062'])
            if len(eog_inds) != 2:
                raise RuntimeError('EEG 61 or EEG 62 channel not found !!')

    else:
        raise ValueError('Could not find EOG channel.')
    return eog_inds


def create_misc_epochs(raw, ch_name=None, event_id=999, picks=None,
                      tmin=-0.2, tmax=0.05, l_freq=1, h_freq=10,
                      reject=None, flat=None,
                      baseline=None, verbose=None):
    """Conveniently generate epochs around EOG artifact events
    Parameters
    ----------
    raw : instance of Raw
        The raw data
    ch_name : str
        The name of the channel to use for ECG peak detection.
        The argument is mandatory if the dataset contains no ECG channels.
    event_id : int
        The index to assign to found events
    picks : array-like of int | None (default)
        Indices of channels to include (if None, all channels
        are used).
    tmin : float
        Start time before event.
    tmax : float
        End time after event.
    l_freq : float
        Low pass frequency.
    h_freq : float
        High pass frequency.
    reject : dict | None
        Rejection parameters based on peak to peak amplitude.
        Valid keys are 'grad' | 'mag' | 'eeg' | 'eog' | 'ecg'.
        If reject is None then no rejection is done. You should
        use such parameters to reject big measurement artifacts
        and not ECG for example
    flat : dict | None
        Rejection parameters based on flatness of signal
        Valid keys are 'grad' | 'mag' | 'eeg' | 'eog' | 'ecg'
        If flat is None then no rejection is done.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).
    baseline : tuple or list of length 2, or None
        The time interval to apply rescaling / baseline correction.
        If None do not apply it. If baseline is (a, b)
        the interval is between "a (s)" and "b (s)".
        If a is None the beginning of the data is used
        and if b is None then b is set to the end of the interval.
        If baseline is equal ot (None, None) all the time
        interval is used. If None, no correction is applied.
    Returns
    -------
    ecg_epochs : instance of Epochs
        Data epoched around ECG r-peaks.
    """
    events = find_misc_events(raw, ch_name=ch_name, event_id=event_id,
                             l_freq=l_freq, h_freq=h_freq)

    # create epochs around EOG events
    misc_epochs = Epochs(raw, events=events, event_id=event_id,
                        tmin=tmin, tmax=tmax, proj=False, reject=reject,
                        flat=flat, picks=picks, baseline=baseline,
                        preload=True)
    return misc_epochs



def find_bads_misc(ica, inst, ch_name=None, threshold=3.0,
                  start=None, stop=None, l_freq=1, h_freq=10,
                  verbose=None):
    """Detect EOG related components using correlation
    Detection is based on Pearson correlation between the
    filtered data and the filtered ECG channel.
    Thresholding is based on adaptive z-scoring. The above threshold
    components will be masked and the z-score will be recomputed
    until no supra-threshold component remains.
    Parameters
    ----------
    inst : instance of Raw, Epochs or Evoked
        Object to compute sources from.
    ch_name : str
        The name of the channel to use for ECG peak detection.
        The argument is mandatory if the dataset contains no ECG
        channels.
    threshold : int | float
        The value above which a feature is classified as outlier.
    start : int | float | None
        First sample to include. If float, data will be interpreted as
        time in seconds. If None, data will be used from the first sample.
    stop : int | float | None
        Last sample to not include. If float, data will be interpreted as
        time in seconds. If None, data will be used to the last sample.
    l_freq : float
        Low pass frequency.
    h_freq : float
        High pass frequency.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).
        Defaults to self.verbose.
    Returns
    -------
    ecg_idx : list of int
        The indices of EOG related components, sorted by score.
    scores : np.ndarray of float, shape (ica.n_components_) | list of array
        The correlation scores.
    """

    misc_inds = _get_eog_channel_index(ch_name, inst)
    if len(misc_inds) > 2:
        misc_inds = misc_inds[:1]
    scores, misc_idx = [], []
    misc_chs = [inst.ch_names[k] for k in misc_inds]

    # some magic we need inevitably ...
    # get targets befor equalizing
    targets = [ica._check_target(k, inst, start, stop) for k in misc_chs]

    if inst.ch_names != ica.ch_names:
        inst = inst.pick_channels(ica.ch_names)

    for misc_chs, target in zip(misc_chs, targets):
        scores += [ica.score_sources(inst, target=target,
                                      score_func='pearsonr',
                                      start=start, stop=stop,
                                      l_freq=l_freq, h_freq=h_freq,
                                      verbose=verbose)]
        misc_idx += [find_outliers(scores[-1], threshold=threshold)]

    # remove duplicates but keep order by score, even across multiple
    # EOG channels
    scores_ = np.concatenate([scores[ii][inds]
                              for ii, inds in enumerate(misc_idx)])
    misc_idx_ = np.concatenate(misc_idx)[np.abs(scores_).argsort()[::-1]]

    misc_idx_unique = list(np.unique(misc_idx_))
    misc_idx = []
    for i in misc_idx_:
        if i in misc_idx_unique:
            misc_idx.append(i)
            misc_idx_unique.remove(i)
    if len(scores) == 1:
        scores = scores[0]

    return misc_idx, scores


