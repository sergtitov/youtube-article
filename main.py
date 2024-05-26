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

def download_audio_from_youtube(url):
    """Downloads audio from the given YouTube URL and returns the filename."""

    filename = None

    def my_hook(d):
        nonlocal filename
        if d["status"] == "finished":
            filename = d["filename"]

    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
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
    with open(f"{audio_filename}_mono.{AUDIO_FORMAT}", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    return transcription

def summarize_transcript(transcript, system_prompt, user_prompt_template):
    summarize_prompt = user_prompt_template.format(transcript)

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": summarize_prompt},
        ],
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content

def main(url: Union[str, None]):
    """Main function to parse arguments and orchestrate the summarization of a YouTube video."""
    if not url:
        parser = argparse.ArgumentParser(description="Summarize YouTube videos.")
        parser.add_argument(
            "url", type=str, help="The URL of the YouTube video to summarize."
        )
        args = parser.parse_args()
        url = args.url.replace("\\", "")

    try:
        audio_filename = download_audio_from_youtube(url)
        convert_audio_to_mono(audio_filename)
        transcript = transcribe_audio(audio_filename)
        with open(f"{audio_filename}.txt", "w") as f:
            f.write(transcript)
        system_prompt = load_prompt("system_prompt.txt")
        user_prompt = USER_PROMPT.format(transcript)
        summary = summarize_transcript(transcript, system_prompt, user_prompt)
        # save the summary to a file
        with open(f"{audio_filename}_summary.md", "w") as f:
            f.write(summary)
    finally:
        pass
        # Cleanup downloaded and processed files only if they exist
        # if os.path.exists(f"{audio_filename}.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}.{AUDIO_FORMAT}")
        # if os.path.exists(f"{audio_filename}_mono.{AUDIO_FORMAT}"):
        #     os.remove(f"{audio_filename}_mono.{AUDIO_FORMAT}")

url = "https://www.youtube.com/watch?v=BT6Aw6Q75Yg"

if __name__ == "__main__":
    main(url)
