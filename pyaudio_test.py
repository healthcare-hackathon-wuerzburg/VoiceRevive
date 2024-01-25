import pyaudio
import numpy as np
import scipy.signal

# Audio configuration
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Low-pass filter configuration
cutoff_frequency = 3000  # 3000 Hz cutoff frequency
nyquist_frequency = RATE / 2  # Nyquist frequency is half the sampling rate
order = 6  # Order of the filter

# Design a Butterworth low-pass filter
b, a = scipy.signal.butter(order, cutoff_frequency / nyquist_frequency, btype='low', analog=False)

def distort_audio(data, gain=2):
    """
    A simple distortion effect by clipping the audio signal.
    """
    # Convert byte data to numpy array
    audio_data = np.frombuffer(data, dtype=np.float32)

    # Create a writable copy of the audio data
    audio_data = np.copy(audio_data)

    # Apply gain
    audio_data *= gain

    # Apply clipping for distortion
    audio_data = np.clip(audio_data, -1.0, 1.0)

    # Convert back to byte data
    return audio_data.tobytes()

def apply_filter(data, filter_coefficients):
    """
    Apply a filter to the audio signal.
    """
    audio_data = np.frombuffer(data, dtype=np.float32)
    filtered_data = scipy.signal.lfilter(filter_coefficients[0], filter_coefficients[1], audio_data)
    return filtered_data.astype(np.float32).tobytes()

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                output=True, frames_per_buffer=CHUNK)

print("Streaming distorted audio. Press Ctrl+C to stop.")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        data = apply_filter(data, (b, a))
        data = distort_audio(data)
        stream.write(data, CHUNK)
except KeyboardInterrupt:
    print("\nStopping audio stream.")

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()