#!/usr/bin/env python3

import wave

import pyaudio
import speech_recognition as sr
import yaml
import os

import acumen_client as ac


class Aural:
    pyAudio = pyaudio.PyAudio()
    recognizer = sr.Recognizer()

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "configuration.yaml")) as config:
            self.config = yaml.load(config)

        self.microphone = sr.Microphone()
        self.acumenClient = ac.AcumenClient(self.config)

        self.recognition = wave.open(self.config["aural"]["sounds"]["recognition"])
        self.failure = wave.open(self.config["aural"]["sounds"]["failure"])

        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 900

    def listen(self):
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source)

            said = self.recognizer.recognize_google(audio)

            print("Heard: " + said)

            if "Edwin" in said:
                self.play_sound(self.recognition)
                self.acumenClient.process(said)
        except sr.UnknownValueError:
            print("Unable to process command.")
        except sr.WaitTimeoutError:
            print("Nothing detected.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.play_sound(self.failure)
        except AssertionError:
            print("Acumen API response wasn't 200")
            self.play_sound(self.failure)

        print("Threshold: " + self.recognizer.energy_threshold.__str__())

    def play_sound(self, wav):
        data = wav.readframes(1024)
        stream = self.pyAudio.open(
            format=self.pyAudio.get_format_from_width(wav.getsampwidth()),
            channels=wav.getnchannels(),
            rate=wav.getframerate(),
            output=True
        )

        while data != b'':
            stream.write(data)
            data = wav.readframes(1024)

        wav.setpos(0)

aural = Aural()
while True:
    aural.listen()
