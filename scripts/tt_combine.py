import os
import json
import argparse

def load_json_file(file_path):
    """
    Load a JSON file from the specified path.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def load_text_file(file_path):
    """
    Load a text file (OCR result) from the specified path and return the content as a string.
    """
    with open(file_path, 'r') as file:
        return file.read()

def combine_transcription_and_ocr(transcription_data, ocr_text):
    """
    Combine the transcription data and OCR text into a single structure.
    """
    combined_data = {
        "transcription": transcription_data.get("text", ""),
        "ocr_text": ocr_text,
        "combined_text": transcription_data.get("text", "") + " " + ocr_text
    }
    return combined_data

def process_files(transcription_folder, ocr_folder, output_folder):
    """
    Process all transcription and OCR files in the specified folders, combine them,
    and save the results into the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(transcription_folder):
        if file_name.endswith(".json"):
            # Load the transcription JSON file
            transcription_path = os.path.join(transcription_folder, file_name)
            transcription_data = load_json_file(transcription_path)

            # Load the corresponding OCR text file
            ocr_file_name = file_name.replace('.json', '-text.txt')
            ocr_path = os.path.join(ocr_folder, ocr_file_name)
            if os.path.exists(ocr_path):
                ocr_text = load_text_file(ocr_path)
            else:
                ocr_text = ""

            # Combine the transcription and OCR data
            combined_data = combine_transcription_and_ocr(transcription_data, ocr_text)

            # Save the combined data as a new JSON file in the output folder
            output_file_path = os.path.join(output_folder, file_name)
            with open(output_file_path, 'w') as output_file:
                json.dump(combined_data, output_file, indent=4)

            print(f"Combined and saved data for {file_name}")

def main():
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description="Combine transcription and OCR text files into a unified format")
    parser.add_argument("transcription_folder", type=str, help="Path to the folder containing transcription JSON files.")
    parser.add_argument("ocr_folder", type=str, help="Path to the folder containing OCR text files.")
    parser.add_argument("output_folder", type=str, help="Path to the folder where combined JSON files will be saved.")

    args = parser.parse_args()

    # Process all files in the transcription and OCR folders
    process_files(args.transcription_folder, args.ocr_folder, args.output_folder)

if __name__ == "__main__":
    main()