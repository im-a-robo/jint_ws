import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wavfile
import os
import tempfile
import csv
import time
from datetime import datetime, timedelta

# Load the Whisper model
model = whisper.load_model("base")

# Function to record audio from microphone
def record_audio(duration, sample_rate=16000):
    print(f"Recording audio for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return audio

# Function to save the audio as a temporary WAV file
def save_audio_to_wav(audio, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavfile.write(temp_file.name, sample_rate, audio)
    return temp_file.name

# Function to transcribe audio from microphone and save to CSV with datetime timestamps
def transcribe_mic_audio_to_csv(duration=2, output_csv="transcription.csv", interval=5):
    sample_rate = 16000  # Whisper models typically work well with 16kHz audio

    # Record audio from the microphone
    audio = record_audio(duration, sample_rate)

    # Save the audio as a temporary WAV file
    audio_file_path = save_audio_to_wav(audio, sample_rate)

    try:
        # Open the CSV file for writing
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Text"])  # Write the headers

            # Transcribe the audio file using Whisper
            print("Transcribing...")
            result = model.transcribe(audio_file_path, verbose=True)
            transcription_text = result['text']

            # Get the current time as the start timestamp
            start_time = datetime.now()

            # Split transcription into intervals based on the total duration and interval
            num_intervals = duration // interval
            interval_duration = len(transcription_text) // num_intervals

            # Write transcription to CSV in time intervals (5 seconds)
            for i in range(num_intervals):
                # Calculate the timestamp for each interval
                current_time = start_time + timedelta(seconds=i * interval)
                text_chunk = transcription_text[i * interval_duration:(i + 1) * interval_duration]
                writer.writerow([current_time.strftime("%Y-%m-%d %H:%M:%S"), text_chunk])

                print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}: {text_chunk}")

    finally:
        # Clean up and remove the temporary audio file
        os.remove(audio_file_path)

if __name__ == "__main__":
    # Specify the duration of the recording and transcribe to CSV
    transcribe_mic_audio_to_csv(duration=10, output_csv="transcription.csv", interval=5)
