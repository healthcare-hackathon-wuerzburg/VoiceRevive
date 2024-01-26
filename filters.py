# third-party modules
from pyaudio import paFloat32
import numpy as np
import pyrubberband as pyrb
from scipy.signal import lfilter, butter


def apply_pitch_shift_filter(
    data: bytes,
    semitones: int,
    sampling_rate: int = 44100
) -> bytes:
    """
    Shifts the pitch of the audio data.

    `data: bytes` Audio data to filter.
    `semitones: int` Number of semitones to shift the pitch. Use 0.X to pitch down.
    `sampling_rate: int` Sampling rate.
    """
    return pyrb.pitch_shift(data, sampling_rate, semitones)


def apply_eq_filter(
    data: np.ndarray,
    low_gain: float = 1.5,
    mid_gain: float = 1.0,
    high_gain: float = 1.2,
    sampling_rate: int = 44100
) -> bytes:
    """
    Apply a three-band equalization filter to the audio data.

    `data: bytes` Audio data to filter.
    `low_gain: float` Gain for the low frequencies.
    `mid_gain: float` Gain for the mid frequencies.
    `high_gain: float` Gain for the high frequencies.
    `sampling_rate: int` Sampling rate.
    """
    # Low-pass filter for low frequencies
    b, a = butter(2, 250 / (0.5 * sampling_rate), btype='low')
    low_freqs = lfilter(b, a, data)

    # Band-pass filter for mid frequencies
    b, a = butter(2, [250 / (0.5 * sampling_rate), 4000 / (0.5 * sampling_rate)], btype='band')
    mid_freqs = lfilter(b, a, data)

    # High-pass filter for high frequencies
    b, a = butter(2, 4000 / (0.5 * sampling_rate), btype='high')
    high_freqs = lfilter(b, a, data)

    # Apply gains
    return (low_freqs * low_gain) + (mid_freqs * mid_gain) + (high_freqs * high_gain)
