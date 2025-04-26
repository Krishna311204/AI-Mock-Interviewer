# ultra_sensitive_sentiment_analyzer.py

from textblob import TextBlob
import re

# Define filler words
FILLER_WORDS = {
    "um", "uh", "like", "you know", "so", "actually", "basically", "literally", 
    "I mean", "right", "okay", "well", "hmm"
}

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Very sensitive thresholds
    if polarity > 0.05:
        return "Positive"
    elif polarity < -0.05:
        return "Negative"
    else:
        return "Neutral"

def detect_filler_words(text):
    text_lower = text.lower()
    fillers_found = []
    for word in FILLER_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, text_lower)
        fillers_found.extend(matches)
    return fillers_found

def detect_pauses(text):
    pauses = []
    # Detect ellipsis ...
    ellipsis = len(re.findall(r"\.\.\.", text))
    if ellipsis > 0:
        pauses.extend(["ellipsis"] * ellipsis)

    # Detect long spaces (more than 3 spaces)
    long_spaces = len(re.findall(r" {3,}", text))
    if long_spaces > 0:
        pauses.extend(["long_space"] * long_spaces)

    return pauses

def main():
    try:
        with open("script.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("The file 'script.txt' was not found.")
        return

    blob = TextBlob(text)
    sentences = blob.sentences

    results = {"Positive": 0, "Negative": 0, "Neutral": 0}
    polarities = []
    total_fillers = 0
    all_fillers = []
    total_pauses = 0
    all_pauses = []

    print("Sentence-wise Detailed Analysis:\n")
    for sentence in sentences:
        sentence_text = str(sentence)
        sentiment = analyze_sentiment(sentence_text)
        results[sentiment] += 1
        polarities.append(sentence.sentiment.polarity)

        fillers = detect_filler_words(sentence_text)
        pauses = detect_pauses(sentence_text)

        total_fillers += len(fillers)
        all_fillers.extend(fillers)

        total_pauses += len(pauses)
        all_pauses.extend(pauses)

        print(f"Sentence: {sentence_text}")
        print(f"Sentiment: {sentiment}")
        print(f"Polarity Score: {sentence.sentiment.polarity:.3f}")
        print(f"Filler Words: {fillers if fillers else 'None'}")
        print(f"Pauses Detected: {pauses if pauses else 'None'}\n")

    print("\nOverall Analysis:")
    total_sentences = sum(results.values())
    for sentiment, count in results.items():
        print(f"{sentiment}: {count} sentences ({(count/total_sentences)*100:.2f}%)")

    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    print(f"\nAverage Polarity Score: {avg_polarity:.4f}")
    if avg_polarity > 0.05:
        overall_sentiment = "Overall Positive"
    elif avg_polarity < -0.05:
        overall_sentiment = "Overall Negative"
    else:
        overall_sentiment = "Overall Neutral"
    print(f"Overall Sentiment: {overall_sentiment}")

    print("\nFiller Words Summary:")
    print(f"Total Filler Words Detected: {total_fillers}")
    if total_fillers > 0:
        filler_summary = {}
        for filler in all_fillers:
            filler_summary[filler] = filler_summary.get(filler, 0) + 1
        for filler, count in filler_summary.items():
            print(f"{filler}: {count} times")
    else:
        print("No filler words detected.")

    print("\nPauses Summary:")
    print(f"Total Pauses Detected: {total_pauses}")
    if total_pauses > 0:
        pause_summary = {}
        for pause in all_pauses:
            pause_summary[pause] = pause_summary.get(pause, 0) + 1
        for pause_type, count in pause_summary.items():
            print(f"{pause_type}: {count} times")
    else:
        print("No significant pauses detected.")

if __name__ == "__main__":
    main()