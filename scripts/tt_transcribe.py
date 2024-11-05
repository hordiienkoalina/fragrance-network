import re
import os
import subprocess
import whisper
import json
import argparse
from dotenv import load_dotenv

class SpeechConverter:
    def __init__(self, mp4, json_output_folder, mp3_output_folder, method='openai'):
        self.mp4 = mp4
        self.json_output_folder = json_output_folder
        self.mp3_output_folder = mp3_output_folder
        self.method = method
        self.basefilename = re.match(r'(.*)\.mp4$', os.path.basename(self.mp4)).group(1)
        # Load OpenAI Whisper model
        self.model = whisper.load_model("base")
        
    def convert_mp4_to_mp3(self):
        """Convert mp4 video to mp3 audio."""
        mp3_file = os.path.join(self.mp3_output_folder, f"{self.basefilename}.mp3")
        ffmpeg_command = ["ffmpeg", "-i", self.mp4, "-vn", "-acodec", "mp3", mp3_file]
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

    def save_as_json(self, text):
        """Save transcribed text as a JSON file."""
        output_file = os.path.join(self.json_output_folder, f"{self.basefilename}.json")
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
                self.save_as_json(extracted_text)
            return extracted_text
        return None

def main():
    # Set up argparse for CLI arguments
    parser = argparse.ArgumentParser(description="Batch Video Transcription Script")
    parser.add_argument("data_folder", type=str, help="Path to the folder containing mp4 video files.")
    parser.add_argument("json_output_folder", type=str, help="Path to the folder where JSON results will be saved.")
    parser.add_argument("mp3_output_folder", type=str, help="Path to the folder where MP3 files will be saved.")
    args = parser.parse_args()

    # Ensure output folders exist
    if not os.path.exists(args.json_output_folder):
        os.makedirs(args.json_output_folder)
    if not os.path.exists(args.mp3_output_folder):
        os.makedirs(args.mp3_output_folder)

    # Get list of all .mp4 files in the specified directory
    mp4_files = [f for f in os.listdir(args.data_folder) if f.endswith(".mp4")]

    if not mp4_files:
        print(f"No mp4 files found in directory {args.data_folder}.")
        return

    # Process each video file
    for mp4_file in mp4_files:
        mp4_filepath = os.path.join(args.data_folder, mp4_file)
        print(f"Processing video: {mp4_filepath}")
        speech_converter = SpeechConverter(mp4_filepath, args.json_output_folder, args.mp3_output_folder)
        transcription = speech_converter.extract_and_transform_speech()

        if transcription:
            print(f"Transcription completed for {mp4_file} successfully.")
        else:
            print(f"Transcription failed for {mp4_file}.")

if __name__ == "__main__":
    main()