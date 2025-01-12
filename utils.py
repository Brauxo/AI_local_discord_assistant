import pyttsx3
import json
import os
from ollama import chat
from config import MODEL_NAME, HISTORY_FILE, SYSTEM_PROMPT
import azure.cognitiveservices.speech as speechsdk
import speech_recognition as sr
import subprocess
import emoji
import re



def init_system_prompt() :
    json_prompt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(json_prompt, f, ensure_ascii=False, indent=4)

def process_input(messages):
    try:
        response = chat(model=MODEL_NAME, messages=messages)
        return response.message.content
    except Exception as e:
        return f"Error: {e}"
    

def process_speech(messages):
    try:
        response = chat(model=MODEL_NAME, messages=messages)
        
        return response.message.content
    except Exception as e:
        return f"Error: {e}"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening... talk in your microphone")
            audio = recognizer.listen(source, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language='fr-FR')
            print(f"Reconnu : {text}")
            return text
        except sr.UnknownValueError:
            print("Didn't understand")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognizer : {e}")
            return None

def generate_audio(text, filename="response.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
