## Main Concepts
There are two main concepts for the real-time Voice Modulator:

1. A Speech to Speech (STS) Approach
    - Potentially low latency
    - Two possible options
    - ML Based Solution
        - Audio Stream (Chunk) is given as Input to ML-model
        - Model-output is outputted as Audio Stream (Chunk)
    - Filter Based 
        - Predefined filters are applied and their parameters are finetuned to fit the original voice of the patient

2. Speech to Text (STT) combined with Text to Speech (TTS) Approach
    - High Latency
    - Not very Applicable
    - Could be easier to realize
    - Train a ML-model based on old audio files 

## Primary Problems of Patients
- “Strange” voice
- Not able to (spontaneously) laugh, scream, …
- Cannot call for help/scream in dangerous situations
- Overall reduced quality of life

## Analyzed 3th Party Repositories
During the initial Healthcare Hackathon a multitude of different frameworks were evaluated for the use case. In the following an overview is provided regarding our findings.
### Promising Ones
- Denoise Frameworks
    - general Problem
        - voice is not recognized as noise
        - do only have a minimal effect on the audio
    - https://github.com/AP-Atul/Audio-Denoising/tree/master
        - No noticeable effect on the participant recording
        - easy to use
    - https://github.com/will-rice/denoisers/tree/main/denoisers
        - Did not run
        - could be a valid try though
    - https://github.com/jose-solorzano/audio-denoiser
        - Best model regarding the usability
        - no effect on the voice of participants
    - https://github.com/sa-if/Audio-Denoiser/blob/main/main.py
        - Only code of the script itself could be used for some reference
- ML-Models
    - https://github.com/NVIDIA/CleanUNet
    - https://github.com/santi-pdp/segan_pytorch 

### Dead Projects without much Potential for the Use Case
- https://github.com/juancarlospaco/pyvoicechanger
    - STS
    - Last commit 5 years ago
    - Runs on mac with Sox
    - No real documentation
- https://github.com/svc-develop-team/so-vits-svc
    - SVC = Singing Voice Conversion
- https://github.com/serp-ai/bark-with-voice-clone
    - TTS
    - Up-to-date
    - Problems running training with GPU on the server available at the time
    - CPU training very slow
    - Application of cloned voice still quite slow
- https://github.com/coqui-ai/tts
    - TTS
    - Up-to-date
    - ~3-4 seconds for a simple sentence
