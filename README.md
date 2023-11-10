# SCAV VIDEO LAB 3
## USE IN TERMINAL THE FOLLOWING COMMAND-LINE ARGUMENTS TO USE THE DIFFERENT IMPLEMENTED METHODS:
### FOR THIS LAB I'VE USED A bbb9s.mp4 segment, and a bbb60s.mp4
### EXERCISE 1: Visualize Macroblocks Motion Vectors:

```ruby
python3 scav_video_lab_3.py --visualize_macroblocks_motion_vectors bbb9s.mp4 bbb9s_mmv.mp4
```

### EXERCISE 2: Create Custom BBB Video Container:
In this exercise we will package into a single mp4 5 tracks.
```ruby
python3 scav_video_lab_3.py --create_custom_bbb bbb60s.mp4
```
### EXERCISE 3: Count Tracks in Container:
In this third exercise we will count all the tracks of the container created on the last exercise:
```ruby
python3 scav_video_lab_3.py --count_tracks_in_mp4 final_output.mp4
```
If we take a look at the output with different tests, an mp3/aac audio file only contains 1 track. The original bbb mp4 file contains 2 tracks [h264 + aac]. And the container created on the last exercise contains a total amount of 5 tracks:
```ruby
The MP4 container 'final_output.mp4' contains 5 tracks.
Track 0: Type: video, Codec: h264 #Original Video.
Track 1: Type: audio, Codec: aac #Original Video Audio.
Track 2: Type: audio, Codec: mp3 #Mono track.
Track 3: Type: audio, Codec: mp3 #Stereo with Lower Bitrate.
Track 4: Type: audio, Codec: aac #AAC Codec.
```

### EXERCISE 4-5: Download and Embed Subtitles:
For this exercise after searching for different solution I ended up using yt-dlp to download the subtitles from youtube directly.
yt-dlp can be easily installed from the terminal using:
```ruby
pip install yt-dlp
```
The subtitles embed in the video have been extracted from here: https://www.youtube.com/watch?v=mwKJfNYwvm8
This has added a bit more of complexity to the code since from the beginning of this year Youtube has implemented multiple audio solutions for a same video id so I set the language to "en" into the script.

```ruby
python3 scav_video_lab_3.py --download_and_embed_subtitles https://www.youtube.com/watch?v=mwKJfNYwvm8 final_output.mp4
```
This step has been a bit difficult since yt-dlp automatically renames the vtt subtitles when it is downloaded so I had to create a method for checking the name and renaming it so it can be embed correctly into the video. We can find both methods needed into the _download_and_embed_subtitles.py_ script.

### EXERCISE 6:
This exercise extracts the yuv histogram and creates a new container in which the histogram is displayed.
```ruby
python3 scav_video_lab_3.py --extract_yuv_histogram final_output_with_subtitles.mp4 final_output_with_subtitles_with_histogram.mp4
```

### EXERCISE 7 [EXTRA]:
_To end this practice, I thought it might be cool to create a container into a single method with all the different exports that we have been doing on the previous exercises, meaning a container which will contain, the original video "h264", the original audio video track, the mono mp3 track, the stereo mp3 track with lower bitrate, the aac audio track, the yuv histogram and the subtitles, all packages into a single .mp4 using FFMPEG_
```ruby
python3 scav_video_lab_3.py --create_custom_bbb_full bbb_cut_50s.mp4
```
Notice that for this exercise in the script we are not creating again all the files, cutting the video and exporting the audios, meaning that we need to pass as argument the video cut into 50s segment already so everything has the same number of frames/samples.

```ruby
python3 scav_video_lab_3.py --count_tracks_in_mp4 final_output_full.mp4
```

If we take a look at the output of the last command we can observe how the final_output_full.mp4 file contains a total amount of 9 tracks:

```ruby
The MP4 container 'final_output_full.mp4' contains 9 tracks.
Track 0: Type: video, Codec: h264
Track 1: Type: audio, Codec: aac
Track 2: Type: audio, Codec: mp3
Track 3: Type: audio, Codec: mp3
Track 4: Type: audio, Codec: aac
Track 5: Type: video, Codec: h264
Track 6: Type: audio, Codec: aac
Track 7: Type: video, Codec: h264
Track 8: Type: audio, Codec: aac
```

