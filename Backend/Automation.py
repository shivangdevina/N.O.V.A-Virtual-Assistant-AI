from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print as rich_print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

from googlesearch import search as google_search

# Load .env
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Groq Client Init
client = Groq(api_key=GroqAPIKey)

# System message for Groq Chat
messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('Username', 'JARVIS')} , you're a content writer. You have to write content like a letter."}]

# Professional messages (optional usage)
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need - don't hesitate to ask.",
]

# -------------------- Utility Functions --------------------

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "").strip()
    filename = rf"Data\{Topic.lower().replace(' ', '')}.txt"

    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(filename)
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def get_first_link(query):
    try:
        for result in google_search(query, num_results=1):
            print(f"[GoogleSearch] First result for '{query}': {result}")
            return result
    except Exception as e:
        print(f"[Googlesearch error]: {e}")
    return None

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"[AppOpener failed]: {e}")
        link = get_first_link(app)
        if link:
            webopen(link)
            return True
        else:
            print(f"No valid link found for '{app}'")
            return False

def CloseApp(app):
    if "chrome" in app:
        return False  # Let user close browser manually
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    def bluetooth_on():
        os.system('powershell.exe -Command "Set-Service bthserv -StartupType Automatic; Start-Service bthserv"')

    def bluetooth_off():
        os.system('powershell.exe -Command "Stop-Service bthserv"')

    def wifi_on():
        os.system("""netsh interface set interface "Wi-Fi" enabled""")

    def wifi_off():
        os.system("""netsh interface set interface "Wi-Fi" disabled""")

    match command.strip().lower():
        case "mute":
            mute()
        case "unmute":
            unmute()
        case "volume up":
            volume_up()
        case "volume down":
            volume_down()
        case "bluetooth on":
            bluetooth_on()
        case "bluetooth off":
            bluetooth_off()
        case "wifi on":
            wifi_on()
        case "wifi off":
            wifi_off()
    return True
# -------------------- Async Automation Engine --------------------

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        command = command.strip().lower()

        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)
        else:
            rich_print(f"[red]No Function Found for: {command}[/red]")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

# -------------------- Entry Point --------------------

if __name__ == "__main__":
    asyncio.run(Automation(["system wifi on"]))
