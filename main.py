# Python modules
from time import sleep
from threading import Thread, Event
from queue import Queue

# third-party modules
import numpy as np
from pyaudio import PyAudio, Stream, paFloat32

# own modules
from filters import apply_eq_filter


# Audio configuration
FORMAT = paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024


def audio_input(
        stream: Stream,
        audio_queue: Queue,
        stop_event: Event
    ) -> None:
    """
    Audio input thread. Responsible for reading the audio data from the microphone.

    `stream: pyaudio.Stream` PyAudio stream object.
    `audio_queue: queue.Queue` Queue to forward the audio data to.
    `stop_event: threading.Event` Event to stop the thread.
    """
    while not stop_event.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)


def audio_processing(
        audio_queue: Queue,
        processed_queue: Queue,
        stop_event: Event
    ) -> None:
    """
    Audio processing thread. Responsible for processing the audio data.

    `audio_queue: queue.Queue` Queue containing the raw audio data.
    `processed_queue: queue.Queue` Queue to forward the processed audio data to.
    `stop_event: threading.Event` Event to stop the thread.
    """
    while not stop_event.is_set():
        data = audio_queue.get()
        # transform audio bytes to numpy array
        data = np.frombuffer(data, dtype=np.float32)
        
        # add filters here
        data = apply_eq_filter(data, 2)
        
        # transform numpy array back to audio bytes
        data = data.astype(np.float32).tobytes()
        processed_queue.put(data)


def audio_output(
        stream: Stream,
        processed_queue: Queue,
        stop_event: Event
    ) -> None:
    """
    Audio output thread. Responsible for outputting the processed audio data.

    `stream: pyaudio.Stram` PyAudio stream object.
    `processed_queue: queue.Queue` Queue containing the processed audio data.
    `stop_event: threading.Event` Event to stop the thread.
    """
    while not stop_event.is_set():
        data = processed_queue.get()
        stream.write(data)


def main() -> None:
    """
        Dummy main function to show how to use the audio processing functions.
        This function spawns three threads for audio input, processing and output.
        It still has a significant delay, but allows a seamless audio stream.
    """
    # pyaudio base setup
    p = PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

    # queues for sharing data between threads
    audio_queue = Queue()
    processed_queue = Queue()
    
    stop_event = Event()

    # Create and start threads
    input_thread = Thread(target=audio_input, args=(stream, audio_queue, stop_event))
    process_thread = Thread(target=audio_processing, args=(audio_queue, processed_queue, stop_event))
    output_thread = Thread(target=audio_output, args=(stream, processed_queue, stop_event))

    input_thread.start()
    process_thread.start()
    output_thread.start()

    print('Streaming audio. Press Ctrl+C to stop.')
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        print('\n\'-> Stopping audio stream.')
        stop_event.set()

    print(' \'->Waiting for threads to finish.')
    input_thread.join()
    process_thread.join()
    output_thread.join()

    print(' \'->Threads finished.')
    print('Shutting down.')
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    main()
