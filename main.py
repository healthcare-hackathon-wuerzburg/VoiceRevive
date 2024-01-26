import pyaudio
from threading import Thread, Event
from queue import Queue
import time

from filters import apply_filter, pitch_shift, apply_eq_filter


# Audio configuration
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024


# Thread-safe queues for data sharing
audio_queue = Queue()
processed_queue = Queue()


def audio_input(stream, audio_queue, stop_event):
    while not stop_event.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)


def audio_processing(audio_queue, processed_queue, stop_event):
    while not stop_event.is_set():
        data = audio_queue.get()
        # Process data (apply filters, pitch shift, etc.)
        #data = pitch_shift(data, 2)
        processed_queue.put(data)


def audio_output(stream, processed_queue, stop_event):
    while not stop_event.is_set():
        data = processed_queue.get()
        stream.write(data)


def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)
    stop_event = Event()

    # Create and start threads
    input_thread = Thread(target=audio_input, args=(stream, audio_queue, stop_event))
    process_thread = Thread(target=audio_processing, args=(audio_queue, processed_queue, stop_event))
    output_thread = Thread(target=audio_output, args=(stream, processed_queue, stop_event))

    input_thread.start()
    process_thread.start()
    output_thread.start()

    print("Streaming audio. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping audio stream.")
        stop_event.set()

    # Wait for threads to finish
    input_thread.join()
    process_thread.join()
    output_thread.join()

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
