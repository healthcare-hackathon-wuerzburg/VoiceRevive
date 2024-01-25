import pyaudio
import wave

# Audio configuration
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Mono audio
RATE = 44100              # Sampling rate
CHUNK = 1024              # Audio chunk size

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream for both input and output
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    output=True, frames_per_buffer=CHUNK)

print("Streaming audio. Press Ctrl+C to stop.")

try:
    while True:
        data = stream.read(CHUNK)
        stream.write(data, CHUNK)
except KeyboardInterrupt:
    print("\nStopping audio stream.")

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PortAudio interface
audio.terminate()