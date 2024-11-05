import argparse
import os
import yt_dlp
import time
import random

def main():
    parser = argparse.ArgumentParser(description='Download TikTok videos from a list of URLs.')
    parser.add_argument('input_file', help='Path to the input txt file containing TikTok URLs.')
    parser.add_argument('output_dir', help='Directory to save downloaded videos.')
    parser.add_argument('--cookies', help='Path to cookies.txt file for authentication (optional).')
    args = parser.parse_args()
    
    # Read URLs from the input file
    with open(args.input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
        
    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set up yt_dlp options
    ydl_opts = {
        'outtmpl': os.path.join(args.output_dir, '%(title).60s [%(id)s].%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'trim_file_name': 100,  # Max length of the filename (excluding extension)
        'restrictfilenames': True,  # Restrict filenames to ASCII characters and avoid special characters
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/115.0.0.0 Safari/537.36'
            ),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
        },
        'retries': 3,
        'fragment_retries': 3,
        'socket_timeout': 15,  # Increase timeout to 15 seconds
        'sleep_interval_requests': 1,  # Sleep between requests
    }

    # Add cookies if provided
    if args.cookies:
        ydl_opts['cookiefile'] = args.cookies
        
    # Download each video using yt_dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            attempts = 0
            while attempts < 3:
                try:
                    print(f'Downloading {url}')
                    ydl.download([url])
                    # Sleep for a random duration between 5 to 10 seconds
                    time.sleep(random.uniform(5, 10))
                    break  # Break out of the retry loop if successful
                except yt_dlp.utils.DownloadError as e:
                    attempts += 1
                    print(f'Error downloading {url}: {e}')
                    # Sleep before retrying
                    time.sleep(random.uniform(10, 15))
                    if attempts >= 3:
                        print(f'Failed to download {url} after {attempts} attempts.')
                except Exception as e:
                    print(f'Unexpected error downloading {url}: {e}')
                    break  # Break on unexpected errors
    
if __name__ == '__main__':
    main()