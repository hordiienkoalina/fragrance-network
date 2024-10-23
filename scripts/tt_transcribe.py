import re
import os
import subprocess
import whisper
import json
from pydub import AudioSegment
import argparse

class SpeechConverter:
    def __init__(self, mp4, method='openai'): 
        self.mp4 = mp4
        self.method = method
        self.basefilepath = re.match(r'(.*)\.mp4$', self.mp4).group(1)
        # Load OpenAI Whisper model
        self.model = whisper.load_model("base")
        
    def convert_mp4_to_mp3(self):
        """Convert mp4 video to mp3 audio."""
        mp3_file = f"{self.basefilepath}.mp3"
        ffmpeg_command = [ "ffmpeg", "-i", self.mp4, "-vn", "-acodec", "mp3", mp3_file ]
        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"MP3 Conversion successful for {self.mp4}.\n")
            return mp3_file
        except subprocess.CalledProcessError as e:
            print(f"Error during MP3 conversion: {e}")
            return None
        
    def convert_speech_to_text(self, audio_file):
        """Transcribe speech to text using the specified method."""
        try:
            if self.method == 'openai': 
                result = self.model.transcribe(audio_file)
                return result['text']
            else:
                print("Only 'openai' method is supported in this script.")
                return None
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None

    def save_as_json(self, text, output_file):
        """Save transcribed text as a JSON file."""
        with open(output_file, 'w') as json_file:
            json.dump({"text": text}, json_file, indent=4)
        print(f"Data saved as JSON: {output_file}.\n")
    
    def extract_and_transform_speech(self):
        """Process the mp4 video, transcribe it, and save results as JSON."""
        # Step 1: Convert mp4 to mp3
        mp3_file = self.convert_mp4_to_mp3()
        if mp3_file:
            # Step 2: Convert speech to text
            extracted_text = self.convert_speech_to_text(mp3_file)
            if extracted_text:
                # Step 3: Save transcribed text as JSON
                self.save_as_json(extracted_text, f"{self.basefilepath}.json")
            return extracted_text
        return None

def main():
    # Set up argparse for CLI arguments
    parser = argparse.ArgumentParser(description="Batch Video Transcription Script")
    parser.add_argument("data_folder", type=str, help="Path to the folder containing mp4 video files.")
    args = parser.parse_args()

    # Get list of all .mp4 files in the specified directory
    mp4_files = [f for f in os.listdir(args.data_folder) if f.endswith(".mp4")]

    if not mp4_files:
        print(f"No mp4 files found in directory {args.data_folder}.")
        return

    # Process each video file
    for mp4_file in mp4_files:
        mp4_filepath = os.path.join(args.data_folder, mp4_file)
        print(f"Processing video: {mp4_filepath}")
        speech_converter = SpeechConverter(mp4_filepath)
        transcription = speech_converter.extract_and_transform_speech()

        if transcription:
            print(f"Transcription completed for {mp4_file} successfully.")
        else:
            print(f"Transcription failed for {mp4_file}.")

if __name__ == "__main__":
    main()