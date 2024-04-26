import speech_recognition as sr
import pyttsx3
import subprocess

start = pyttsx3.init()

def listen():
    '''Voice recording function'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Printing and pronunciation of the message "It is possible to speak"
        print('Можно говорить')
        start.say('Можно говорить')
        start.runAndWait()
        # Setting the pause threshold and adjusting to ambient noise

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        # Attempt to recognize audio and convert it to text using the Google Web Speech API
        task = r.recognize_google(audio, language='ru-RU').lower()
        print(task)
        return task
    except sr.UnknownValueError:
        # If speech is not recognized, display an error message and ask to repeat
        print("Голос не распознан, повторите")
        start.say('Голос не распознан, повторите')
        start.runAndWait()
        return listen()
    except sr.RequestError:
        # If it was not possible to send a request to the speech Recognition API, return an empty string
        print("Не удалось отправить запрос к сервису распознавания речи")
        return ""

def request(task):
    '''The function of answering questions and executing commands
    variations  - you can write your own answers and questions
    open_app - opens the specified application by command'''
    variations = {
        'привет': 'Привет!',
        'как дела': 'Хорошо, спасибо!',
        'пока': 'До свидания!'
    }

    open_app = {
        'блокнот': 'notepad',
        'калькулятор': 'calc'
    }

    # commands for conversation
    if task in variations:
        text = variations[task]
        start.say(text)
        start.runAndWait()
    # commands to launch the application
    elif task in open_app:
        program_path = open_app[task]
        subprocess.Popen(program_path, shell=True)
    # command for exit and answer
    elif task == 'выход':
        print("До свидания!")
        start.say("До свидания!")
        start.runAndWait()
        exit()
    # if command was not recognized
    else:
        start.say("Команда не распознана")
        start.runAndWait()
        print("Команда не распознана")

while True:
    request(listen())
