import cv2
import pytesseract
import os
import argparse

# Configure pytesseract path if necessary (only required if Tesseract is not in the system path)
# pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract_executable'

def extract_text_from_frame(frame):
    """
    Extract text from a given video frame using Tesseract OCR.
    """
    # Convert the frame to grayscale (improves OCR accuracy)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text from the frame
    extracted_text = pytesseract.image_to_string(gray_frame)

    return extracted_text.strip()

def extract_frames_and_text(video_path, output_text_file, frame_interval=30):
    """
    Extract frames from a video at regular intervals and apply OCR to extract text.
    Save the extracted text to a file.
    """
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    frame_count = 0
    extracted_texts = []

    while True:
        # Read the next frame from the video
        success, frame = video_capture.read()

        if not success:
            break  # Stop the loop if there are no more frames

        # Process every nth frame (based on frame_interval)
        if frame_count % frame_interval == 0:
            # Extract text from the current frame
            text = extract_text_from_frame(frame)
            if text:
                extracted_texts.append(text)
                print(f"Extracted text from frame {frame_count}: {text}")

        frame_count += 1

    # Release the video capture object
    video_capture.release()

    # Save extracted text to the output file
    with open(output_text_file, 'w') as f:
        for text in extracted_texts:
            f.write(text + "\n")

    print(f"Extracted text saved to {output_text_file}")

def process_videos_in_folder(input_folder, output_folder, frame_interval=30):
    """
    Process all video files in a folder, extract text from them, and save the results.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp4"):
            video_path = os.path.join(input_folder, file_name)
            output_text_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_text.txt")

            print(f"Processing video: {video_path}")
            extract_frames_and_text(video_path, output_text_file, frame_interval)

def main():
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description="Extract text from video frames using OCR")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing video files.")
    parser.add_argument("output_folder", type=str, help="Path to the folder where extracted text will be saved.")
    parser.add_argument("--frame_interval", type=int, default=30, help="Interval of frames to process (default is every 30th frame).")

    args = parser.parse_args()

    # Process all video files in the input folder
    process_videos_in_folder(args.input_folder, args.output_folder, args.frame_interval)

if __name__ == "__main__":
    main()