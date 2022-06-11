from logging.config import stopListening
import os
import time
import pyttsx3
import datetime
import sys
from sys import exec_prefix
import speech_recognition as sr
from fuzzywuzzy import fuzz


# engine = pyttsx3.init()
# engine.say("Привет мир")
# engine.runAndWait()
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("name: \"{1}\" \n `Micro(device_index={0})`".format(index,name))


# r = sr.Recognizer()
# with sr.Microphone(device_index=1) as source:
#     # print()
#     audio = r.listen(source)

# query = r.recognize_google(audio, language="ru-RU")
# print('Распознано: ' + query.lower())


opts = {
    "alias": ('зентрея', 'зен', 'жен', 'зена', 'зина', 'жена', 'зентрея мать твою', 'зен мать твою', 'жен мать твою', 'зена мать твою', 'зина мать твою', 'жена мать твою'),  # обращение
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        "sleep": ('пора спать', 'спать', 'усни', 'пока')
    }
}


def speak(what):
    print(what)
    speack_engine.say(what)
    speack_engine.runAndWait()
    speack_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("D:\\Jarvis\\res\\radio_record.m3u")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

    elif cmd == 'sleep':
        # воспроизвести радио
        speak('До встречи')
        sys.exit()

    else:
        print('Команда не распознана, повторите!')


if __name__ == "__main__":
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    with m as source:
        r.adjust_for_ambient_noise(source)

    speack_engine = pyttsx3.init()

    voices = speack_engine.getProperty('voices')
    speack_engine.setProperty('voice', voices)

    speak('Слушаю')

    stop_listening = r.listen_in_background(m, callback)
    while True:
        time.sleep(0.1)
