import os
import whisper
import yt_dlp

# Load the Whisper model once globally
model = whisper.load_model("large")

def download_audio_from_youtube(url, output_wav_path):
    os.makedirs(os.path.dirname(output_wav_path), exist_ok=True)

    # Strip .wav if already included
    if output_wav_path.lower().endswith(".wav"):
        output_wav_path = output_wav_path[:-4]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_wav_path,  # yt-dlp will add .wav
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {url} ...")
        ydl.download([url])

def transcribe_audio(audio_path, output_path):
    """Transcribe audio file and save transcript."""
    print(f"Transcribing {audio_path} ...")
    result = model.transcribe(audio_path, language="en")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcript saved to: {output_path}")

def map_input_to_output_path(input_path, input_root, output_root, new_ext=".txt"):
    """Map input file path to output file path, changing extension."""
    relative_path = os.path.relpath(input_path, input_root)
    base, _ = os.path.splitext(relative_path)
    output_relative_path = base + new_ext
    return os.path.join(output_root, output_relative_path)

def transcribe_folder(input_folder, output_folder, audio_output_folder):
    """Process each txt file in input_folder, download audio, transcribe, save transcript."""
    for dirpath, _, filenames in os.walk(input_folder):
        for filename in filenames:
            if not filename.lower().endswith(".txt"):
                continue

            input_txt_path = os.path.join(dirpath, filename)
            print(f"\nProcessing URL file: {input_txt_path}")

            # Read the YouTube URL from the txt file
            with open(input_txt_path, "r", encoding="utf-8") as f:
                url = f.read().strip()
                if not url:
                    print(f"Warning: {input_txt_path} is empty. Skipping.")
                    continue

            # Determine output paths
            wav_path = map_input_to_output_path(input_txt_path, input_folder, audio_output_folder, new_ext=".wav")
            transcript_path = map_input_to_output_path(input_txt_path, input_folder, output_folder, new_ext=".txt")

            # Download and transcribe
            download_audio_from_youtube(url, wav_path)
            transcribe_audio(wav_path, transcript_path)



######################################
input_folder = "links"         # .txt files with YouTube URLs
output_folder = "transcripts"   # where .txt transcripts go
audio_output_folder = "audios"  # where permanent .wav files go

transcribe_folder(input_folder, output_folder, audio_output_folder)
######################################

