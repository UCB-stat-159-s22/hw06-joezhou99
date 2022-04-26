from ligotools import utils as utils
import numpy as np
from ligotools import readligo as rl
import json
from scipy.io import wavfile
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import os.path

fnjson = "/home/jovyan/HW/hw06-joezhou99/data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
eventname = 'GW150914' 
event = events[eventname]
fn_H1 = "/home/jovyan/HW/hw06-joezhou99/data/" + event['fn_H1'] 
fs = event['fs']
strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
time = time_H1
dt = time[1] - time[0]

make_psds = 1
if make_psds:
    # number of sample for the fast fourier transform:
    NFFT = 4*fs
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)

    # We will use interpolations of the ASDs computed above for whitening:
    psd_H1 = interp1d(freqs, Pxx_H1)
    
tevent = event['tevent']      
fband = event['fband'] 
deltat = 5
deltat_sound = 2.  
indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))

whiten_data = 1
if whiten_data:
    # now whiten the data from H1 and L1, and the template (use H1 PSD):
    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    
    # We need to suppress the high frequency noise (no signal!) with some bandpassing:
    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization

fshift = 400.
    
def test_type_whiten():
    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    assert (type(strain_H1_whiten)==np.ndarray)
    
def test_dim_whiten():
    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    assert (len(strain_H1_whiten)==131072)

def test_exist_write_wavfile():
    filename = "/home/jovyan/HW/hw06-joezhou99/audio/pytest.wav"
    utils.write_wavfile(filename,int(fs), strain_H1_whitenbp[indxd])
    assert os.path.isfile(filename) 
    
def test_reqshift():
    strain_H1_shifted = utils.reqshift(strain_H1_whitenbp,fshift=fshift,sample_rate=fs)
    shifted_l = len(strain_H1_shifted)
    unshifted_l = len(strain_H1)
    assert(shifted_l == unshifted_l)