# -*- coding: utf-8 -*-
from numpy.fft import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

def MCD_model(signals, freq=44100):
    nsamp = len(signals[0])
    duration = nsamp/freq
    t = np.linspace(0, duration, nsamp)

    stimA = signals[0]
    stimV = signals[1]

    param = [0.0873, 0.0684, 0.7859]

    fv = fft(t*np.exp(-t/param[0]))
    fa = fft(t*np.exp(-t/param[1]))
    fav = fft(t*np.exp(-t/param[2]))

    st_a = fft(stimA) * fa
    st_v = fft(stimV) * fv

    st_a_av = st_a * fav
    st_v_av = st_v * fav

    u1 = np.real(ifft(st_a_av) * ifft(st_v))
    u2 = np.real(ifft(st_v_av) * ifft(st_a))

    MCD_aud_signal = np.real(ifft(st_a))
    MCD_vis_signal = np.real(ifft(st_v))
    MCD_corr_signal = u1 * u2
    MCD_lag_signal = u2 - u1
    

    MCD_corr = np.mean(MCD_corr_signal)
    MCD_lag = np.mean(MCD_lag_signal)

    return [MCD_corr, MCD_lag, MCD_corr_signal, MCD_lag_signal, MCD_aud_signal, 
            MCD_vis_signal]

def SCD_model(signals, freq=44100):
    nsamp = len(signals[0])
    duration = nsamp/freq
    t = np.linspace(0, duration, nsamp)

    stimA = signals[0]
    stimV = signals[1]

    param = [0.0873, 0.0684]
    param = [0.0873, 0.0684]    

    fv = fft(t*np.exp(-t/param[0]))
    fa = fft(t*np.exp(-t/param[1]))

    st_a = fft(stimA) * fa# * fav
    st_v = fft(stimV) * fv #* fav

    SCD_corr_signal = np.real(ifft(st_a) * ifft(st_v))
    SCD_lag_signal = np.real(ifft(st_v)) - np.real(ifft(st_a))
    
    SCD_corr = np.mean(SCD_corr_signal)
    SCD_lag = np.mean(SCD_lag_signal)

    return [SCD_corr, SCD_lag, SCD_corr_signal, SCD_lag_signal]

def plotModelOutput(stimA, stimV, corrSignal, lagSignal, title, freq=44100):
    duration = len(stimA)/freq
    t = np.linspace(0, duration, len(stimA))
    
    fig = plt.figure(figsize=(8, 6))
    fig.suptitle(title, fontsize=16)
    ax = plt.subplot(221)
    ax.set_title('Stimuli')
    ax.plot(t, stimA, 'g-', label='Auditory stimulus')
    ax.plot(t, stimV, 'm-', label='Visual stimulus')
    ax.legend()

    ax = plt.subplot(222)
    ax.set_title('Correlation unit output')
    ax.plot(t, corrSignal, 'b-')

    ax = plt.subplot(223)
    ax.set_title('Lag unit output')
    ax.plot(t, lagSignal, 'r-')
    plt.show()

    
    
    
    
    