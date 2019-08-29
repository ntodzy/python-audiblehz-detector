import numpy as np
import pyaudio
# import matplotlib for other stuff later <3
# import pyautogui 

#dont define filesystem as fs thx
FREQ_ARRAY = []
NOTE_MIN = 20 #C4 = 60, Feel free to change these. I've only tested this range but it should work from 0-9 octaves
NOTE_MAX = 80 #A4 = 69
FSAMP = 22050 #idk should be 1024 but ok?
FRAME_SIZE = 2048
FRAMES_PER_FFT = 32 # Average Across FFT (AKA REMOVE THE OVERTONES)

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] #+ str(n/12 - 1)

#MINMAX INDEX

def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

#Allocate Space in Array for FFT
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

#Create a live audio data channel. Pyaudio will create a numpy array for the fft
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

#Live User Interaction
#interactions = dict({'B': b, 'C':c,'C#':cs,'D':d,'D#':ds,'E':e,'F':f, 'F#':fs, 'G':g, 'G#':gs, 'A': a , 'A#': ash}) # This next section is for post-interactions, aka playing beeps writing more code, exporting certain things when certain notes happen! Please leave it all commented if you dont want that to happen.

# def b() :
# def c() :
# def cs() :
# def d() :
# def ds() :
# def e() :
# def f() :
# def fs() :
# def g() :
# def gs() :
# def a() :
# def ash() :

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
        FREQ_ARRAY.append(freq) # Add to Freq Array
        print(note_name(n0), freq, len(FREQ_ARRAY)) #Run N0 through note name function to retreive note

        # interactionToCall = interactions[note_name(n0)] # These two lines are for serving out the interactions. If you dont want any interactions please leave commented! 
        # interactionToCall() 
