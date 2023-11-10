import subprocess
import os
import yt_dlp

def get_single_vtt_file_name():
    vtt_files = [file for file in os.listdir() if file.endswith(".vtt")]

    if not vtt_files:
        print("No VTT files found in the current directory.")
        return None

    return vtt_files[0]

def download_and_embed_subtitles(video_url, output_video):
    #Downloading subtitles using yt-dlp which we will need to install first: pip install yt-dlp
    subprocess.run(f"yt-dlp --write-sub --skip-download {video_url}", shell=True, check=True)

    #Extracting the subtitle file (we are assuming that they are in .vtt format):
    original_subtitle_file = get_single_vtt_file_name()
    print(f"Original subtitle file: {original_subtitle_file}")
    
    #Renaming the subtitle file:
    video_id = video_url.split('=')[1]
    new_subtitle_file = f"{video_id}.vtt"
    os.rename(original_subtitle_file, new_subtitle_file)

    #Checking if the subtitle file exists:
    if not os.path.exists(new_subtitle_file):
        print(f"Error: Subtitle file '{new_subtitle_file}' not found.")
        return
    
    #Removing the .mp4 from the name:
    base_name, _ = os.path.splitext(output_video)
    
    #Embeding the subtitles into the video using ffmpeg with re-encoding:
    subprocess.run(f"ffmpeg -i {output_video} -vf subtitles={new_subtitle_file} -c:a aac -c:v libx264 {base_name}_with_subtitles.mp4", shell=True, check=True)