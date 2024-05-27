from typing import Union
import yt_dlp
import argparse
import os
from subprocess import run
from openai import OpenAI

AUDIO_FORMAT = "mp3"
PREFERRED_QUALITY = "96"
MAX_FILESIZE = 25 * 1024 * 1024  # 25MB
FFMPEG_AUDIO_CHANNELS = "1"  # Mono
FFMPEG_BITRATE = "32k"

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
        f"{audio_filename}_mono.{AUDIO_FORMAT}",
    ]
    run(command)

def transcribe_audio(audio_filename):
    print(f"Transcribing audio for {audio_filename}")
    with open(f"{audio_filename}_mono.{AUDIO_FORMAT}", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    return transcription

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
    print(f"Summarizing transcript for {transcript}")
    system_prompt = load_prompt("summarization_prompt.txt")
    user_prompt_template = USER_PROMPT.format(transcript)
    return call_model(system_prompt, user_prompt_template)

def provide_full_transcription(transcript):
    print(f"Generating full transcription for {transcript}")
    system_prompt = load_prompt("transcription_prompt.txt")
    user_prompt_template = USER_PROMPT.format(transcript)
    return call_model(system_prompt, user_prompt_template)


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
        if not os.path.exists(f"{audio_filename}.{AUDIO_FORMAT}"):
            audio_filename = download_audio_from_youtube(url, title)
            
        if not os.path.exists(f"{audio_filename}_mono.{AUDIO_FORMAT}"):
            convert_audio_to_mono(audio_filename)

        def read_or_transcribe(file_path, transcribe_func, *args):
            if not os.path.exists(file_path):
                content = transcribe_func(*args)
                with open(file_path, "w") as f:
                    f.write(content)
            else:
                with open(file_path, "r") as f:
                    content = f.read()
            return content

        transcript = read_or_transcribe(f"{audio_filename}.txt", transcribe_audio, audio_filename)

        def read_or_summarize(file_path, summarize_func, *args):
            if not os.path.exists(file_path):
                content = summarize_func(*args)
                with open(file_path, "w") as f:
                    f.write(content)

        read_or_summarize(f"{audio_filename}_summary.md", summarize_transcript, transcript)
        read_or_summarize(f"{audio_filename}_full.md", provide_full_transcription, transcript)
    finally:
        pass
        # Cleanup downloaded and processed files only if they exist
        # if os.path.exists(f"{audio_filename}.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}.{AUDIO_FORMAT}")
        # if os.path.exists(f"{audio_filename}_mono.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}_mono.{AUDIO_FORMAT}")

# url = "https://www.youtube.com/watch?v=BT6Aw6Q75Yg"
# title = "All Learning Algorithms Explained in 14 Minutes"

# url = "https://www.youtube.com/watch?v=_ArVh3Cj9rw"
# title = "The Future Of Reasoning"

url = "https://www.youtube.com/watch?v=XLY7lPSk9EE"
title = "Move to Dubai or Panama"

if __name__ == "__main__":
    main(url, title)            