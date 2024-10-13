import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wavfile
import os
import tempfile
import csv
from datetime import datetime

class Transcriber:
    def __init__(self, output_csv="transcription.csv", interval=5):
        self.output_csv = output_csv
        self.interval = interval
        self.model = whisper.load_model("base")

    def record_audio(self):
        sample_rate = 16000
        print(f"Recording audio for {self.interval} seconds...")
        audio = sd.rec(int(self.interval * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is finished
        return audio

    def save_audio_to_wav(self, audio, sample_rate):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        wavfile.write(temp_file.name, sample_rate, audio)
        return temp_file.name

    def transcribe_mic_audio(self):
        sample_rate = 16000
        audio = self.record_audio()
        audio_file_path = self.save_audio_to_wav(audio, sample_rate)

        try:
            # Open the CSV file for appending (append mode)
            with open(self.output_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Transcribe the audio file using Whisper
                print("Transcribing...")
                result = self.model.transcribe(audio_file_path, language="en", verbose=True)
                transcription_text = result['text']

                # Get the current timestamp
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Write the transcription to the CSV with the current timestamp
                writer.writerow([current_time, transcription_text])
                print(f"{current_time}: {transcription_text}")

        finally:
            # Clean up and remove the temporary audio file
            os.remove(audio_file_path)

    def start_transcription(self):
        # Clear the CSV file and write the header row
        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'transcription'])  # Write headers

        while True:
            self.transcribe_mic_audio()

if __name__ == "__main__":
    transcriber = Transcriber(interval=5, output_csv="transcription.csv")
    transcriber.start_transcription()
