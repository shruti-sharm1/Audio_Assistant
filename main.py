# A Ok Google Audio assistant which can perform following tasks:
# 1. Sends email
# 2. Sends whatsapp messages
# 3. Search topics on wikipedia
# 4. Play songs on youtube
# 5. Tells you current time
# 6. Can read any pdf (as mentioned by you) ----> Alternative of audiobook
# 7. Opens map of specified place by user

import datetime  # To work with date and time
import os  # To interact with operating system and its application
import smtplib  # Defines an client session object used for sending mail to any machine
import webbrowser  # To allow displaying Web-based documents to users
from email.message import EmailMessage
import PyPDF2  # PDF ToolKit
import pyttsx3  # To convert text to speech
import pywhatkit  # For sending whatsapp Message
import requests  # Allows to send HTTP Requests
import speech_recognition as sr  # For recognizing users audio
import wikipedia  # To access and parse data from Wikipedia

#  !!!!!!!!  IMPORTANT
#  pip install pipwin
#  pipwin install pyaudio
#  To install pyaudio !!!!!!!!!!!!!

#  sapi5 Microsoft developed speech API. Helps in synthesis and recognition of voice.
#  engine = pyttsx3.init('sapi5')
#  init function to get an engine instance for the speech synthesis
engine = pyttsx3.init()  # to load a driver engine for speech synthesis
voices = engine.getProperty('voices')  # getting details of current voice
engine.setProperty('voice', voices[1].id)  # helps us to select different voices 0 => male 1 => female


# Function to make computer speak
def speak(audio):
    # device speaks the command as specified in audio
    # runAndWait function is used hold the code so that device could speak
    engine.say(audio)
    engine.runAndWait()


# Function To take command from the user
def take_command():
    listener = sr.Recognizer()
    my_mic = sr.Microphone(device_index=1)
    with my_mic as source:
        print("HEARING!!!!")
        # device listens the users command
        audio = listener.listen(source)
        try:
            print("Recognizing...")
            # Recognizing the user command
            query = listener.recognize_google(audio)
            # Using google for command validation if user says google then only action can be done
            if "google" in query.lower():
                a = query.replace("Google", "")
                speak(a)
        except Exception:
            # If recognizer is not able to recognize exception is thrown
            print("Say that again please...")  # Say that again will be printed in case of improper voice
            return "None"  # None string will be returned
    # Returning the well recognized command
    return query


# Computer wishes the user as per the time
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening!")
    speak("How can I help You!!!")


# Checking the connection because some steps need a good connection
def net_connection():
    try:
        # requesting URL
        requests.get("https://www.geeksforgeeks.org", timeout=10)
        return True
    except Exception:
        return False


# Sending the email by taking mail id of receiver, subject of the email and message to be sent
# Replace the email id and passwords
def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('enter_ur_email_id', 'enter_ur_password')
    email = EmailMessage()
    email['From'] = 'enter_ur_email_id'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)


# Getting the information by the user fo sending the email
def get_email_info():
    speak('To Whom you want to send email give the email id')
    email = take_command()
    speak('What is the subject of your email?')
    subject = take_command()
    speak('Tell me the text in your email')
    message = take_command()
    send_email(email, subject, message)
    speak('Hey lazy ass. Your email is sent')
    speak('Do you want to send more email?')
    send_more = take_command()
    if 'yes' in send_more:
        get_email_info()


if __name__ == '__main__':
    wish_me()
    m = True
    while m:
        actionToDo = take_command().lower()
        netstatus = net_connection()
        if "google" in actionToDo:
            if 'wikipedia' in actionToDo:
                speak("What do u wanna search on Wikipedia")
                topic = take_command()

                speak("Searching Wikipedia!! for " + topic)
                if netstatus:
                    try:
                        results = wikipedia.summary(topic, sentences=2)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                    except Exception:
                        speak("Sorry but can I help You in some other way")
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif 'open youtube' in actionToDo:
                if netstatus:
                    webbrowser.open("www.youtube.com")
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif 'open google' in actionToDo and 'map' not in actionToDo:
                if netstatus:
                    webbrowser.open("www.google.com")
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif "play song" in actionToDo or "play music" in actionToDo:
                if netstatus:
                    speak("which song you want to hear")
                    name_song = take_command()
                    pywhatkit.playonyt(name_song)
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif 'time' in actionToDo:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'send' in actionToDo and ('message' in actionToDo or "whatsapp message" in actionToDo):
                if netstatus:
                    speak("Say the message to be sent")
                    msg = take_command()

                    speak("Say the Number to whom u want to sent")
                    number = take_command()
                    pywhatkit.sendwhatmsg_instantly("+91" + number, msg)
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif "open notepad" in actionToDo:
                os.system("Notepad")

            elif "open map" in actionToDo or "open google map" in actionToDo:
                if netstatus:
                    speak("Where would you like to go")
                    place = take_command()
                    webbrowser.open('https://www.google.com/maps/place/' + place)
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif "read a pdf" in actionToDo or "audiobook" in actionToDo:
                book = open('Data-Structures-Abstractions-and-Design-Using-Java-Third-Edition-2016.pdf', 'rb')
                pdfReader = PyPDF2.PdfFileReader(book)
                pages = pdfReader.numPages

                for num in range(7, pages):
                    page = pdfReader.getPage(num)
                    text = page.extractText()
                    speak(text)

            elif "send" in actionToDo and "email" in actionToDo:
                if netstatus:
                    get_email_info()
                else:
                    speak("Sorry no Internet connection can I help you with something else")

            elif "quit" in actionToDo or "sleep" in actionToDo or "stop" in actionToDo \
                    or "exit" in actionToDo or "close" in actionToDo:
                break

            else:
                speak("I am sorry but can I help in some other way")

        else:
            m = False

    speak("Exiting....")
