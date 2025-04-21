import speech_recognition as sr
import keyboard
import os
from textblob import TextBlob
import time

# Function for speech-to-text
def listen_and_write_to_file():
    """Listens to the microphone and writes recognized text to script.txt."""
    recognizer = sr.Recognizer()
    
    # Clear the script.txt file before starting
    with open("script.txt", "w") as file:
        file.write("")

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

# Function for sentiment analysis
def analyze_sentiment(text):
    """Analyze sentiment of the text using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    subjectivity = blob.sentiment.subjectivity  # Range: 0 (objective) to 1 (subjective)
    
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, polarity, subjectivity

# Function to analyze the script.txt file line by line
def analyze_script():
    """Analyze the script.txt line by line and provide sentiment analysis."""
    sentiment_results = []
    try:
        while True:
            # Open script.txt and read all lines
            with open("script.txt", "r") as file:
                lines = file.readlines()

            if lines:
                for line in lines:
                    if line.strip():  # Ignore empty lines
                        sentiment, polarity, subjectivity = analyze_sentiment(line.strip())
                        sentiment_results.append({
                            "text": line.strip(),
                            "sentiment": sentiment,
                            "polarity": polarity,
                            "subjectivity": subjectivity
                        })

            # Wait for a few seconds before checking for new lines in script.txt
            time.sleep(5)

            # If the file is still empty, or if user chooses to stop, break the loop
            if not lines:
                break

    except KeyboardInterrupt:
        print("\nSentiment analysis finished.")

    return sentiment_results

# Function to print sentiment analysis results
def print_analysis_results(results):
    """Print the sentiment analysis results with confidence scores."""
    if results:
        print("\nSentiment Analysis Results:")
        for result in results:
            print(f"Text: {result['text']}")
            print(f"Sentiment: {result['sentiment']}")
            print(f"Polarity: {result['polarity']}")
            print(f"Subjectivity: {result['subjectivity']}")
            print("-" * 50)
    else:
        print("No content to analyze.")

# Main function to run both speech-to-text and sentiment analysis
def main():
    # Start listening and writing to file
    listen_and_write_to_file()

    # After speech-to-text stops, analyze the script.txt content
    print("Starting sentiment analysis...")
    sentiment_results = analyze_script()

    # Print the final sentiment analysis result
    print_analysis_results(sentiment_results)

if __name__ == "__main__":
    main()
