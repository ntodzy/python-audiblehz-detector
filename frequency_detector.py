import numpy as np
import pyaudio
from scipy import fftpack

FREQ_ARRAY = []
NOTE_MIN = 60 #C4
NOTE_MAX = 80 #A4
FSAMP = 22050 #idk should be 1024 but ok?
FRAME_SIZE = 2048
FRAMES_PER_FFT = 32 # Average Across FFT (AKA REMOVE THE OVERTONES)

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)

#MINMAX INDEX

def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

#Allocate Space in Array for FFT
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)
stream.start_stream()

#Create an amazing thing that allows lots of plotting points
window = .5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

print ('sampling at', FSAMP, 'Hz with Max Resolutoin of', FREQ_STEP, 'Hz')
print

while stream.is_active():
        
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

    fft = np.fft.rfft(buf * window)

    raw_freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP
    freq = round(raw_freq, 1)
    
    n = freq_to_number(freq)
    n0 = int(round(n))

    num_frames += 1

    if num_frames >= FRAMES_PER_FFT:
        print (freq) #Frequency (hz)
        FREQ_ARRAY.append(freq) # Add to Freq Array
        print (len(FREQ_ARRAY))
        #print(n0) # Number in the equal temperment thing
       # print(num_frames)
