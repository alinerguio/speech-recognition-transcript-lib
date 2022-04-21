# Speech Recognition Lib usage for Portuguese

## Goal

The goal is to download and process audios to be able to transcript them using the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library. The library allows the use of multiple services. In this repository, the goal is to use the following libraries: 
   - Google Cloud Speech API
   - Wit.ai
   - Azure Speech Services 
   - Vosk API

## Requirements

To use this code, you'll need this requirements.   

[![Python Version](https://img.shields.io/badge/python-3.9.5-green)](https://www.python.org/downloads/release/python-395/)

When the repository is first cloned, use this commands:
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Execution
Then, every time you want to access, don't forget to activate you enviroment:
```
$ source env/bin/activate
```

## Downloading and Processing Data

Check [this repository](https://github.com/alinerguio/processing-data) for more info on this matter.  

## Executing scripts

To execute the scripts, there is the need to set the environment - as stated in the "Requirements" session. After that, is also essential that the data is processed as described previously (Downloading and Processing Data). To execute the code, is only necessary to execute the python command and the script name, as ilustrated below:

```
$ python3 main-<engine-to-transcript>.py
```

```
<engine-to-transcript>:
   - azure
   - google
   - vosk
   - wit
```
