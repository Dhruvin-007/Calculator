import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import psutil
import platform
import re
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import wikipedia

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 190)  # Speed

# Function to search the web and get a brief summary
def web_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Look for the answer snippet (usually in a div with class="BNeawe iBp4i AP7Wnd")
    answer = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
    
    if answer:
        return answer.text
    else:
        return "Sorry, I couldn't find the answer."


def speak(text):
    print(f"Stella: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        command = r.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn’t reach the speech service.")
        return ""

def get_date():
    today = datetime.datetime.now()
    return today.strftime("%A, %d %B %Y")

def get_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    return f"Battery is at {percent}% and {'charging' if plugged else 'not charging'}."

def basic_web_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here is what I found on the web.")

def system_info():
    sys = platform.uname()
    return f"System: {sys.system}, Node Name: {sys.node}, Processor: {sys.processor}"

def perform_math_operation(command):
    if "multiply" in command:
        numbers = re.findall(r'\d+', command)
        if len(numbers) == 2:
            result = int(numbers[0]) * int(numbers[1])
            speak(f"The result is {result}")
            return

    elif "divide" in command:
        numbers = re.findall(r'\d+', command)
        if len(numbers) == 2:
            if int(numbers[1]) != 0:
                result = int(numbers[0]) / int(numbers[1])
                speak(f"The result is {result}")
            else:
                speak("Sorry, division by zero is not allowed.")
            return

    elif "add" in command or "plus" in command:
        numbers = re.findall(r'\d+', command)
        if len(numbers) == 2:
            result = int(numbers[0]) + int(numbers[1])
            speak(f"The result is {result}")
            return

    elif "subtract" in command or "minus" in command:
        numbers = re.findall(r'\d+', command)
        if len(numbers) == 2:
            result = int(numbers[0]) - int(numbers[1])
            speak(f"The result is {result}")
            return

    elif "percent" in command or "percentage" in command:
        numbers = re.findall(r'\d+', command)
        if len(numbers) == 2:
            result = (int(numbers[0]) * int(numbers[1])) / 100
            speak(f"The result is {result}")
            return

    else:
        speak("Sorry, I couldn't understand the math operation.")

def open_application(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "paint": "mspaint.exe",
        "command prompt": "cmd.exe",
        "tlauncher": r"C:\Users\DELL\AppData\Roaming\.minecraft\TLauncher.exe",
        "spotify": r"C:\Users\DELL\AppData\Roaming\Spotify\Spotify.exe",
        "snapchat": r"C:\Users\DELL\AppData\Local\Snapchat\Snapchat.exe",
        "discord": r"C:\Users\DELL\AppData\Local\Discord\Update.exe --processStart Discord.exe",
        "obs studio": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
        "vs code": r"C:\Users\DELL\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "whatsapp": r"C:\Users\DELL\AppData\Local\WhatsApp\WhatsApp.exe"
    }

    for app in apps:
        if app in command:
            try:
                subprocess.Popen(apps[app])
                speak(f"Opening {app}")
            except FileNotFoundError:
                speak(f"Sorry, {app} is not found on this system.")
            return
    speak("Sorry, I don't know how to open that application.")

# ---- Main Program ----
# System ready. Say 'Stella' to start.
wake_word = "stella"
awake = False

while True:
    command = listen()

    if wake_word in command:
        speak("Hello sir, how can I help you?")
        awake = True
        continue

    if not awake or command.strip() == "":
        continue

    if "goodbye" in command:
        speak("Goodbye sir. Have a nice day!")
        break

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        
        # Wikipedia answer
    elif any(q in command for q in ["who is", "what is", "tell me about", "where is", "whom is"]):
        try:
            summary = wikipedia.summary(command, sentences=2)
            speak(summary)
            print("Wikipedia:", summary)
        except:
            speak("Sorry, I couldn't find any details.")
            webbrowser.open(f"https://www.google.com/search?q={command}")

    # YouTube Search
    elif "search" in command and "youtube" in command:
        search_query = command.replace("search", "").replace("on youtube", "").strip()
        speak(f"Searching {search_query} on YouTube.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "volume up" in command:
        os.system("nircmd.exe changesysvolume 5000")
        speak("Volume increased")

    elif "volume down" in command:
        os.system("nircmd.exe changesysvolume -5000")
        speak("Volume decreased")

    elif "mute" in command:
        os.system("nircmd.exe mutesysvolume 1")
        speak("Volume muted")

    elif "unmute" in command:
        os.system("nircmd.exe mutesysvolume 0")
        speak("Volume unmuted")

    elif "what day is it" in command or "what's the date" in command:
        date = get_date()
        speak(f"Today is {date}")

    elif "battery" in command:
        battery = get_battery_status()
        speak(battery)

    elif "system info" in command:
        info = system_info()
        speak(info)

    if any(word in command for word in ["multiply", "divide", "add", "plus", "minus", "subtract", "percent", "percentage"]):
        perform_math_operation(command)

    elif "open" in command:
        open_application(command)

    elif any(word in command for word in ["what", "who", "when", "where", "whom"]):
        basic_web_search(command)

    elif "how are you" in command:
        speak("I'm doing great, thank you for asking!")

    elif "what can you do" in command:
        speak("I can help you with web searches, math problems, system info, and more.")

    else:
        speak("I'm sorry, I didn't understand that.")
