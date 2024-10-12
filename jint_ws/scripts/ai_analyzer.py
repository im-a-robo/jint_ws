import speech_recognition as sr
from transformers import pipeline
import threading

# Initialize the recognizer and classifier
recognizer = sr.Recognizer()
classifier = pipeline("zero-shot-classification")

# Define candidate labels (topics)
candidate_labels = ["technology", "health", "finance", "education", "entertainment"]

# Device index for PulseAudio
device_index = 6  # 'pulse' in your case

def recognize_and_classify():
    text_data = ""
    with sr.Microphone(device_index=device_index) as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening with PulseAudio...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                current_text = recognizer.recognize_google(audio)
                print(f"Recognized: {current_text}")
                text_data += current_text + " "

                if len(text_data.split()) > 0:
                    results = classifier(text_data, candidate_labels)
                    max_score = results['scores'][0]
                    index = 0

                    for i in range(len(results['scores'])):
                        if results['scores'][i] > max_score:
                            max_score = results['scores'][i]
                            index = i

                    print(f"Classification result: {results['labels'][index]}")
                    text_data = ""  # Clear for the next cycle

            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except KeyboardInterrupt:
                print("Stopping...")
                break

if __name__ == "__main__":
    recognize_and_classify()
