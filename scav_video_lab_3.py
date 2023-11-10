import argparse
import subprocess
import re
import os
import io
import numpy as np
import json

from download_and_embed_subtitles import download_and_embed_subtitles, get_single_vtt_file_name
from extract_yuv_histogram import extract_yuv_histogram

###################
### ALL METHODS ###
###################

class P3:
     
    def visualize_macroblocks_motion_vectors(input_video, output_video):
        base_name, ext = os.path.splitext(os.path.basename(input_video))
        command = f"ffmpeg -hide_banner -flags2 +export_mvs -i {input_video} -vf codecview=mv=pf+bf+bb -an {output_video}"
        subprocess.run(command, shell=True, check=True)

    def create_custom_bbb(input_video):
        output_video = "bbb_cut_50s.mp4"
        output_audio_mono_mp3 = "bbb_50s_mono.mp3"
        output_audio_stereo_lower_bitrate = "bbb_50s_stereo_lower_bitrate.mp3"
        output_audio_aac = "bbb_50s_aac.aac"

        #Cutting the video into a 50-second segment:
        subprocess.run(f"ffmpeg -i {input_video} -t 50 -c:v copy -c:a copy {output_video}", shell=True, check=True)

        #Extracting audio as MP3 mono track:
        subprocess.run(f"ffmpeg -i {output_video} -vn -ac 1 -ab 128k {output_audio_mono_mp3}", shell=True, check=True)

        #Extracting audio in MP3 stereo with lower bitrate:
        subprocess.run(f"ffmpeg -i {output_video} -vn -ac 2 -b:a 64k {output_audio_stereo_lower_bitrate}", shell=True, check=True)

        #Extracting audio in AAC codec:
        subprocess.run(f"ffmpeg -i {output_video} -vn -c:a aac {output_audio_aac}", shell=True, check=True)

        #Packaging everything into an MP4:
        subprocess.run(f"ffmpeg -i {output_video} -i {output_audio_mono_mp3} -i {output_audio_stereo_lower_bitrate} -i {output_audio_aac} -c:v copy -c:a copy -map 0 -map 1 -map 2 -map 3 final_output.mp4", shell=True, check=True)


    def count_tracks_in_mp4(input_video):
        command = f"ffprobe -v error -show_entries stream=index,codec_name,codec_type -of json {input_video}"
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            data = json.loads(result)
            tracks = data.get("streams", [])
            
            print(f"The MP4 container '{input_video}' contains {len(tracks)} tracks.")
            for track in tracks:
                print(f"Track {track['index']}: Type: {track['codec_type']}, Codec: {track['codec_name']}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def create_custom_bbb_full(input_video):
        output_video = "bbb_cut_50s.mp4"
        output_audio_mono_mp3 = "bbb_50s_mono.mp3"
        output_audio_stereo_lower_bitrate = "bbb_50s_stereo_lower_bitrate.mp3"
        output_audio_aac = "bbb_50s_aac.aac"
        temp_output_hist = "temp_histogram.mp4"
        temp_output_subtitles = "temp_subtitles.mp4"

        base_name, ext = os.path.splitext(os.path.basename(input_video))

        #Extracting YUV Histogram:
        subprocess.run(f'ffmpeg -hide_banner -i {input_video} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" {temp_output_hist}', shell=True, check=True)

        subtitle_file = get_single_vtt_file_name()

        #Creating the subtitle file:
        subprocess.run(f"ffmpeg -i {output_video} -vf subtitles={subtitle_file} -c:a aac -c:v libx264 {temp_output_subtitles}", shell=True, check=True)

        #Packaging everything into an MP4:
        subprocess.run(f"ffmpeg -i {output_video} -i {output_audio_mono_mp3} -i {output_audio_stereo_lower_bitrate} -i {output_audio_aac} -i {temp_output_hist} -i {temp_output_subtitles} -c:v copy -c:a copy -map 0 -map 1 -map 2 -map 3 -map 4 -map 5 final_output_full.mp4", shell=True, check=True)


##################
###    MAIN    ###
##################

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SCAV Video Lab 3")
    parser.add_argument("--visualize_macroblocks_motion_vectors", nargs=2, help="Visualize Macroblocks Motion Vectors")
    parser.add_argument("--create_custom_bbb", nargs=1, help="Create Custom BBB Video")
    parser.add_argument("--count_tracks_in_mp4", nargs=1, help="Count Tracks in MP4")
    parser.add_argument("--download_and_embed_subtitles", nargs=2, help="Download and Embed Subtitles")
    parser.add_argument("--extract_yuv_histogram", nargs=2, help="Extract YUV Histogram")
    parser.add_argument("--create_custom_bbb_full", nargs=1, help="Add Subtitles and Histogram")

    args = parser.parse_args()

    if args.visualize_macroblocks_motion_vectors:
        input_video, output_video = args.visualize_macroblocks_motion_vectors
        P3.visualize_macroblocks_motion_vectors(input_video, output_video)
        print(f"Video Completed. Output file: {output_video}")

    if args.create_custom_bbb:
        input_video = args.create_custom_bbb[0]
        P3.create_custom_bbb(input_video)
        print(f"5 Files Completed.")
    
    if args.count_tracks_in_mp4:
        input_video = args.count_tracks_in_mp4[0]
        P3.count_tracks_in_mp4(input_video)
    #EXPECTED OUTPUT:
    # The MP4 container 'final_output.mp4' contains 5 tracks.
    # Track 0: Type: video, Codec: h264
    # Track 1: Type: audio, Codec: aac
    # Track 2: Type: audio, Codec: mp3
    # Track 3: Type: audio, Codec: mp3
    # Track 4: Type: audio, Codec: aac

    if args.download_and_embed_subtitles:
        video_url, output_video = args.download_and_embed_subtitles
        download_and_embed_subtitles(video_url, output_video)
        print(f"Video Completed. Output file: {output_video}_with_subtitles.mp4")
    #https://www.youtube.com/watch?v=mwKJfNYwvm8

    if args.extract_yuv_histogram:
        input_video, output_video = args.extract_yuv_histogram
        extract_yuv_histogram(input_video, output_video)
        print(f"Video Completed. Output file: {output_video}")
    
    if args.create_custom_bbb_full:
        input_video = args.create_custom_bbb_full[0]
        P3.create_custom_bbb_full(input_video)
        print(f"Video Completed. Output file: final_output_full.mp4")

    # The MP4 container 'final_output_full.mp4' contains 9 tracks.
    # Track 0: Type: video, Codec: h264
    # Track 1: Type: audio, Codec: aac
    # Track 2: Type: audio, Codec: mp3
    # Track 3: Type: audio, Codec: mp3
    # Track 4: Type: audio, Codec: aac
    # Track 5: Type: video, Codec: h264
    # Track 6: Type: audio, Codec: aac
    # Track 7: Type: video, Codec: h264
    # Track 8: Type: audio, Codec: aac