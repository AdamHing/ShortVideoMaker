import tkinter as tk
from tkinter import ttk
#from BlackSubtitles import VideoTranscriber
from pytube import YouTube
#from main import Stitcher
from moviepy.editor import *
import os
from VideoClips import Clipper,Stitcher
from subtitle_generators.dynamic_subtitles import DynamicSubtitles
import random
#https://www.youtube.com/watch?v=x0beKqQW3Io
#MCVido and peripheral video are used interchangeably 

cwd = os.getcwd()
print(cwd)

tmp_folder = os.path.abspath(os.path.join(cwd, os.pardir))+ "/tmp"

MYVIDEO = tmp_folder+"/ClippedVideo.mp4" #top video
PERIPHERAL_VIDEO = tmp_folder+"/MCV.mp4" #botton video
stitched_video_no_audio_path = tmp_folder+"/StitchedVideo_no_audio.mp4"
# name and location of stitched video with audio file. 
stitched_video_with_audio_path = tmp_folder+"/StitchedVideo_with_audio.mp4"
watermarkPath = "img/watermark.png"
minus_timestamp = 15
plus_timestamp = 30



peripheral_video_list = [
    "https://www.youtube.com/watch?v=Ujvy-DEA-UM",
    "https://www.youtube.com/watch?v=ZkHKGWKq9mY",
    "https://www.youtube.com/watch?v=JwP6sCqmPAs"
                         ]
def process_data():
    link1 = link1_entry.get().strip() #top video
    link2 = link2_entry.get().strip() #bottom video
    num_clips = num_clips_entry.get()
    captions = captions_var.get()
    manual_timestamp = timestamp_entry.get()

    # Your code for processing data goes here
    # Use link1, link2, num_clips, and captions as needed
    print(f"Link 1: {link1}")
    print(f"Link 2: {link2}")
    #https://www.youtube.com/watch?v=J3-m7dAL_cY #red dead
    # https://www.youtube.com/watch?v=a60UewomiCg
    #vid https://www.youtube.com/watch?v=Y5RQgchauHs
    # https://www.youtube.com/watch?v=S94ETUiMZwQ
    # https://www.youtube.com/watch?v=9RhWXPcKBI8
    #YouTube(link1).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/YTV.mp4')
    #MC https://www.youtube.com/watch?v=ZkHKGWKq9mY
    #https://www.youtube.com/watch?v=Ujvy-DEA-UM

    clipper = Clipper(link1)
    if manual_timestamp:
        print("using manual_timestamp")
        timestamp = int(manual_timestamp)
    elif "www.youtube.com" in link1:
        timestamp = clipper.get_most_rewatched_timestamp()
        print("Highest point at {}s:".format(timestamp))
        
    clipper.download(minus_timestamp, timestamp,plus_timestamp)

    # if "www.youtube.com" in link1:
    #     print("downloading video")
    #     Clipper.download(link1,minus_timestamp, timestamp,plus_timestamp)
    # else:
    #     print("link not valid, using local video")
    #     MYVIDEO="Source_videos/"+link1+"mp4"
    if link2:
        YouTube(link2,use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=PERIPHERAL_VIDEO)
        print("downloading peripheral video")

    if not os.path.isfile(PERIPHERAL_VIDEO):
        YouTube("https://www.youtube.com/watch?v=Ujvy-DEA-UM",use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=PERIPHERAL_VIDEO)
    else:
        print("peripheral video already exists, using that one")

    stitcher = Stitcher(MYVIDEO,PERIPHERAL_VIDEO)
    # stitcher.Clip(30, timestamp,30)
    print("=========1==========")
    stitcher.Crop_stitch()
    print("=========2==========")
    stitcher.Audio_watermark(stitched_video_no_audio_path,watermarkPath,stitched_video_with_audio_path)
    print("=========3==========")
    print(f"Number of Clips: {num_clips}")
    print(f"Captions: {captions}")
    print(f"Timestamp: {timestamp}")
    print("Data processed!")

    # if captions == True:
    #     model_path = "base.en"
    #     transcriber = VideoTranscriber(model_path, StitchedVideo_W_audio)
    #     transcriber.extract_audio()
    #     transcriber.transcribe_video()
    #     transcriber.create_video(output_video_path)
    if captions == True:
        DynamicSubtitles(stitched_video_with_audio_path,tmp_folder)

# Create the main window
root = tk.Tk()
root.title("Clippr")
root.iconbitmap("img/icon.ico")
# Set the background color to black
root.configure(bg="#000000")
# Configure a dark theme
style = ttk.Style()
style.theme_use('clam')  # You can experiment with other available themes
# Dark-themed settings
style.configure("TLabel", foreground="#ffffff", background="#000000")
style.configure("TButton", foreground="#ffffff", background="#333333")
style.configure("TEntry", fieldbackground="#444444", foreground="#ffffff")
# Link 1 entry
link1_label = ttk.Label(root, text="MainVideo:")
link1_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
link1_entry = ttk.Entry(root, width=30)
link1_entry.grid(row=0, column=1, padx=10, pady=10)
# Link 2 entry
link2_label = ttk.Label(root, text="OtherVideo:")
link2_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
link2_entry = ttk.Entry(root, width=30)
link2_entry.grid(row=1, column=1, padx=10, pady=10)
# Number of clips entry
num_clips_label = ttk.Label(root, text="Number of Clips:")
num_clips_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
num_clips_entry = ttk.Entry(root, width=10)
num_clips_entry.grid(row=2, column=1, padx=10, pady=10)
# Timestamp format entry
timestamp_label = ttk.Label(root, text="Timestamp Format:")
timestamp_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
timestamp_entry = ttk.Entry(root, width=15)
timestamp_entry.grid(row=3, column=1, padx=10, pady=10)
# Captions checkbutton
captions_label = ttk.Label(root, text="Captions:")
captions_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
captions_var = tk.BooleanVar()
captions_checkbox = ttk.Checkbutton(root, variable=captions_var)
captions_checkbox.grid(row=4, column=1, padx=10, pady=10)
# Create button
create_button = ttk.Button(root, text="Create", command=process_data)
create_button.grid(row=5, column=0, columnspan=2, pady=20)
# Start the main loop
root.mainloop()

