import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

freq = 44100

duration = 5

recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

sd.wait()

wv.write("recording.wav", recording, freq, sampwidth=4)