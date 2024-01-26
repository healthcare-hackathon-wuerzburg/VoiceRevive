# third-party modules
from pyaudio import paFloat32
import numpy as np
import pyrubberband as pyrb
from scipy.signal import lfilter, butter


# Audio configuration
FORMAT = paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024


def apply_pitch_shift_filter(
        data: bytes,
        semitones: int
    ) -> bytes:
    """
    Shifts the pitch of the audio data. 

    `data: bytes` Audio data to filter.
    `semitones: int` Number of semitones to shift the pitch. Use 0.X to pitch down.
    """
    return pyrb.pitch_shift(data, RATE, semitones)


def apply_eq_filter(
        data: np.ndarray,
        low_gain: float = 1.5,
        mid_gain: float = 1.0,
        high_gain: float = 1.2,
        fs: int = 44100
    ) -> bytes:
    """
    Apply a three-band equalization filter to the audio data.

    `data: bytes` Audio data to filter.
    `low_gain: float` Gain for the low frequencies.
    `mid_gain: float` Gain for the mid frequencies.
    `high_gain: float` Gain for the high frequencies.
    `fs: int` Sampling rate.
    """
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
    return (low_freqs * low_gain) + (mid_freqs * mid_gain) + (high_freqs * high_gain)
