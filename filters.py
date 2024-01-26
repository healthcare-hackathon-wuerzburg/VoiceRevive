import pyaudio
import numpy as np
import pyrubberband as pyrb
from scipy.signal import lfilter, butter


# Audio configuration
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024


def apply_filter(data):
    """
    Apply a filter to the audio signal. // should be equal to equalizer and unnecessary
    """
    # Low-pass filter configuration
    cutoff_frequency = 2000  # 3000 Hz cutoff frequency
    nyquist_frequency = RATE / 2  # Nyquist frequency is half the sampling rate
    order = 6  # Order of the filter

    # Design a Butterworth low-pass filter
    b, a = butter(order, cutoff_frequency / nyquist_frequency, btype='low', analog=False)

    audio_data = np.frombuffer(data, dtype=np.float32)
    filtered_data = lfilter(a, b, audio_data)
    return filtered_data.astype(np.float32).tobytes()


def pitch_shift(data, semitones):
    """
    Shifts the pitch of the audio data.
    """
    audio_data = np.frombuffer(data, dtype=np.float32)
    shifted_data = pyrb.pitch_shift(audio_data, RATE, semitones)
    return shifted_data.astype(np.float32).tobytes()


def apply_eq_filter(data, low_gain, mid_gain, high_gain, fs):
    """
    Apply a three-band equalization filter to the audio data.

    :param data: The input audio data (numpy array).
    :param low_gain: Gain for low frequencies.
    :param mid_gain: Gain for mid frequencies.
    :param high_gain: Gain for high frequencies.
    :param fs: Sampling frequency.
    :return: Equalized audio data.
    """
    data = np.frombuffer(data, dtype=np.float32)

    # Low-pass filter for low frequencies
    b, a = butter(2, 250 / (0.5 * fs), btype='low')
    low_freqs = lfilter(b, a, data)

    # Band-pass filter for mid frequencies
    b, a = butter(2, [250 / (0.5 * fs), 4000 / (0.5 * fs)], btype='band')
    mid_freqs = lfilter(b, a, data)

    # High-pass filter for high frequencies
    b, a = butter(2, 4000 / (0.5 * fs), btype='high')
    high_freqs = lfilter(b, a, data)

    # Apply gains
    equalized_signal = (low_freqs * low_gain) + (mid_freqs * mid_gain) + (high_freqs * high_gain)

    return equalized_signal
