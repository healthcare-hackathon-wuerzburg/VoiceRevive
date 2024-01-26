# Lyrebird - Towards a Real-Time Voice Modulator

## Problem Statement
The aim of this project is to develop a real-time voice modulator designed to enhance communication for patients who have undergone laryngectomy (removal of the larynx/throat) due to laryngeal cancer.

It focuses on improving communication capabilities and social integration for individuals who have lost their natural voice as a result of laryngectomy. The project seeks to provide a solution that can restore a semblance of their original voice, thereby aiding in daily communication and enhancing their quality of life.
In order to enable a normal conversation a near realtime approach is required.

## Getting Started
This project only contains a minimal pipeline to get started with the development of a solution to the problem stated above. It does not provide a solution.

### Requirements and Installation
The project is implemented using Python 3.11 and was tested on Mac.

First install the required system packages. For max this can be done using the
following commands:
```
brew install portaudio
brew install libsndfile
brew install rubberband
```

Afterward, the python packages can be installed using `pip install -r requirement.txt`.

## How to use the Project 
The project can be run after installing all dependencies using `python main.py`. This starts 3 threads, one listening to the audio, one processing it, and one returning the processed audio. Currently a pitch and noise filter are available with little effect on the actual voice and only as stumps for further implementation.

## Deployment
The current code base is not conceived for deployment but rather exploration. However, it can be run and therefore be deployed on any platform supporting python 3.11 and the required additional software packages.

## Project Overview

Describe how the project is structured. Describe the architecture and the main components (if necessary) and the interaction between these components.

## How to Contribute
If you want to contribute to the idea of a real-time voice modulator for laryngectomy patients please reach out to us or open your own pull request.

For pull requests pleas stick to this guide:
1) clone the repository
2) work on a dedicated branch for your feature `git branch -b feature_name`
3) create a pull request for the feature and document the changes accordingly
4) you have to write tests in order to get your PR merged
5) send changes against `main` branch

## Additional Information
Further information is available in the [Project Charter](./docs/ProjectCharter.md).