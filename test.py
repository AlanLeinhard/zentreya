import pyttsx3
import speech_recognition as sr
engine = pyttsx3.init()
# engine.say("Привет мир")
engine.runAndWait()
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("name: \"{1}\" \n `Micro(device_index={0})`".format(index,name))