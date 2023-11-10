import subprocess
import os

def extract_yuv_histogram(input_video, output_video):
    base_name, ext = os.path.splitext(os.path.basename(input_video))
    subprocess.run(f'ffmpeg -hide_banner -i {input_video} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" {base_name}_with_histogram{ext}', shell=True, check=True)