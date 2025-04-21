import speech_recognition as sr
import keyboard
import os

# Clear the script.txt file before starting
with open("script.txt", "w") as file:
    file.write("")

# Initialize recognizer
recognizer = sr.Recognizer()

print("Listening... Press 'q' to stop.")

try:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            if keyboard.is_pressed('q'):
                print("Stopped by user.")
                break

            print("Listening for speech...")
            audio = recognizer.listen(source, phrase_time_limit=5)

            try:
                text = recognizer.recognize_google(audio)
                print("Heard:", text)

                # Immediately write the recognized text to script.txt
                with open("script.txt", "a") as file:
                    file.write(text + "\n")

            except sr.UnknownValueError:
                print("Didn't catch that.")
            except sr.RequestError as e:
                print(f"API error: {e}")
except KeyboardInterrupt:
    print("Program exited.")
