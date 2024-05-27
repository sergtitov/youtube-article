from typing import Union
import yt_dlp
import argparse
import os
from subprocess import run
from openai import OpenAI
import whisper
import json
from PIL import Image
import imagehash


AUDIO_FORMAT = "mp3"
PREFERRED_QUALITY = "96"
MAX_FILESIZE = 25 * 1024 * 1024  # 25MB
FFMPEG_AUDIO_CHANNELS = "1"  # Mono
FFMPEG_BITRATE = "32k"
SCREENSHOT_INTERVAL = 10  # Capture a screenshot every 10 seconds

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

USER_PROMPT = """Transcript: {}"""

def load_prompt(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def download_audio_from_youtube(url, title):
    """Downloads audio from the given YouTube URL and returns the filename."""
    print(f"Downloading audio from {url}")
    filename = None

    def my_hook(d):
        nonlocal filename
        if d["status"] == "finished":
            filename = d["filename"]

    ydl_opts = {
        "outtmpl": f"results/{title}/{title}.%(ext)s",
        "format": "worstaudio",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": AUDIO_FORMAT,
                "preferredquality": PREFERRED_QUALITY,
            }
        ],
        "max_filesize": MAX_FILESIZE,
        "progress_hooks": [my_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Strip the extension from the filename to use it for further processing
    if filename:
        return filename.rsplit(".", 1)[0]

def convert_audio_to_mono(audio_filename):
    """Converts the downloaded audio file to mono format with lower bitrate."""
    file_path = f"{audio_filename}_mono.{AUDIO_FORMAT}"
    if os.path.exists(file_path):
        return

    print(f"Converting audio to mono for {audio_filename}")
    command = [
        "ffmpeg",
        "-i",
        f"{audio_filename}.{AUDIO_FORMAT}",
        "-ac",
        FFMPEG_AUDIO_CHANNELS,
        "-ab",
        FFMPEG_BITRATE,
        "-y",
        file_path,
    ]
    run(command)

def transcribe_audio(audio_filename):
    print(f"Transcribing audio for {audio_filename}")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(f"{audio_filename}_mono.{AUDIO_FORMAT}")
        formatted_result = {
            "text": result["text"],
            "segments": [
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                } for segment in result["segments"]
            ]
        }
        return formatted_result
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def read_or_transcribe(audio_filename):
    file_path = f"{audio_filename}.json"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        content = transcribe_audio(audio_filename)
        if content is not None:
            with open(file_path, "w") as f:
                json.dump(content, f)
        else:
            print("Transcription failed, no content to save.")
            return None
    else:
        with open(file_path, "r") as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError:
                print(f"File {file_path} is empty or not properly formatted.")
                return None
    return content

def hash_image(image_path):
    """Generate a hash for an image."""
    with Image.open(image_path) as img:
        return imagehash.average_hash(img)
    

def deduplicate_screenshots(temp_dir, screenshots_dir, interval, hash_threshold=20):
    if os.path.exists(screenshots_dir):
        return

    os.makedirs(screenshots_dir, exist_ok=True)

    """Deduplicates screenshots by comparing image hashes and removing similar images."""
    unique_hashes = []
    for filename in sorted(os.listdir(temp_dir)):
        file_path = os.path.join(temp_dir, filename)
        img_hash = hash_image(file_path)
        
        # Check if the image hash is similar to any existing unique hash
        is_duplicate = any(img_hash - unique_hash < hash_threshold for unique_hash in unique_hashes)
        
        if not is_duplicate:
            unique_hashes.append(img_hash)
            timestamp = int(filename.split('_')[1].split('.')[0]) * interval
            new_filename = f"screenshot_{timestamp}.png"
            os.rename(file_path, os.path.join(screenshots_dir, new_filename))
        else:
            os.remove(file_path)

def capture_screenshots(video_filename, interval):
    """Captures screenshots from the video at the given interval and deduplicates them."""
    print(f"Capturing screenshots from {video_filename}")
    output_dir = os.path.dirname(video_filename)
    temp_dir = f"{output_dir}/temp_screenshots"
    screenshots_dir = f"{output_dir}/screenshots"

    if os.path.exists(screenshots_dir):
        return

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
        command = [
            "ffmpeg",
            "-i",
            f"{video_filename}.webm",
            "-vf",
            f"fps=1/{interval}",
            f"{temp_dir}/screenshot_%04d.png",
        ]
        run(command)
    
    # Deduplicate screenshots
    deduplicate_screenshots(temp_dir, screenshots_dir, interval)
    
    # os.rmdir(temp_dir)
    

def download_video_and_extract_screenshots(url, title, video_filename):
    # Download the video file for screenshots
    if not os.path.exists(f"{video_filename}.webm"):
        print(f"Downloading video for {title}")
        ydl_opts = {
            "outtmpl": f"results/{title}/{title}.%(ext)s",
            "format": "bestvideo[height<=1080]",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    capture_screenshots(video_filename, SCREENSHOT_INTERVAL)

def call_model(system_prompt: str, user_prompt: str, model: str = "gpt-4o") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content

def summarize_transcript(transcript):
    print(f"Summarizing transcript...")
    system_prompt = load_prompt("summarization_prompt.md")
    user_prompt_template = USER_PROMPT.format(transcript)
    return call_model(system_prompt, user_prompt_template)

def provide_full_transcription(transcript):
    print(f"Generating improved transcription...")
    system_prompt = load_prompt("transcription_prompt.txt")
    user_prompt_template = USER_PROMPT.format(transcript)
    return call_model(system_prompt, user_prompt_template)

def integrate_screenshots(transcript, title):
    """Integrates screenshots into the transcript at the appropriate timestamps."""
    print("Generating article with screenshots")
    transcript_with_screenshots = []
    relative_dir = f"screenshots"
    screenshots_dir = f"results/{title}/{relative_dir}"
    
    screenshot_files = sorted(os.listdir(screenshots_dir))
    screenshot_times = [int(f.split('_')[1].split('.')[0]) for f in screenshot_files]
    
    last_screenshot = None
    current_segment_text = []

    for segment in transcript["segments"]:
        start_time = segment["start"]
        text = segment["text"]
        
        # Find the closest screenshot time
        closest_screenshot_time = min(screenshot_times, key=lambda x: abs(x - start_time))
        screenshot_id = screenshot_times.index(closest_screenshot_time)
        screenshots_filename = screenshot_files[screenshot_id]
        relative_path = os.path.join(relative_dir, screenshots_filename)
        
        if last_screenshot != relative_path:
            if current_segment_text:
                transcript_with_screenshots.append(" ".join(current_segment_text))
                current_segment_text = []
            transcript_with_screenshots.append(f"![Screenshot]({relative_path})")
            last_screenshot = relative_path
        
        current_segment_text.append(text)
    
    if current_segment_text:
        transcript_with_screenshots.append(" ".join(current_segment_text))
    
    return "\n".join(transcript_with_screenshots)

def main(url: Union[str, None], title: Union[str, None]):
    """Main function to parse arguments and orchestrate the summarization of a YouTube video."""
    if not url or not title:
        parser = argparse.ArgumentParser(description="Summarize YouTube videos.")
        parser.add_argument(
            "url", type=str, help="The URL of the YouTube video to summarize."
        )
        parser.add_argument(
            "title", type=str, help="The title to use for naming files."
        )
        args = parser.parse_args()
        url = args.url.replace("\\", "")
        title = args.title

    try:
        audio_filename = f"results/{title}/{title}"
        video_filename = f"results/{title}/{title}"
        if not os.path.exists(f"{audio_filename}.{AUDIO_FORMAT}"):
            audio_filename = download_audio_from_youtube(url, title)
            
        convert_audio_to_mono(audio_filename)

        download_video_and_extract_screenshots(url, title, video_filename)

        transcript = read_or_transcribe(audio_filename)
        if transcript is None:
            print("Failed to obtain transcript.")
            return

        def generate_if_absent(file_path, summarize_func, *args):
            if not os.path.exists(file_path):
                content = summarize_func(*args)
                with open(file_path, "w") as f:
                    f.write(content)

        transcript_text = transcript["text"]

        generate_if_absent(f"{audio_filename}_summary.md", summarize_transcript, transcript_text)

        # Integrate screenshots into the full transcript
        transcript_with_screenshots = integrate_screenshots(transcript, title)
        with open(f"{audio_filename}_with_screenshots.md", "w") as f:
            f.write(transcript_with_screenshots)

        # Apply full transcription formatting to the markdown with screenshots
        generate_if_absent(f"{audio_filename}_formatted_with_screenshots.md", provide_full_transcription, transcript_with_screenshots)        
    finally:
        pass
        # Cleanup downloaded and processed files only if they exist
        # if os.path.exists(f"{audio_filename}.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}.{AUDIO_FORMAT}")
        # if os.path.exists(f"{audio_filename}_mono.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}_mono.{AUDIO_FORMAT}")
    print("Done!")

# url = "https://www.youtube.com/watch?v=BT6Aw6Q75Yg"
# title = "All Learning Algorithms Explained in 14 Minutes"

# url = "https://www.youtube.com/watch?v=_ArVh3Cj9rw"
# title = "The Future Of Reasoning"

url = "https://www.youtube.com/watch?v=XLY7lPSk9EE"
title = "Move to Dubai or Panama"

if __name__ == "__main__":
    main(url, title)