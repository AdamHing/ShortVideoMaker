import tkinter as tk
from tkinter import ttk
from BlackSubtitles import VideoTranscriber
from pytube import YouTube
#from main import Stitcher
from VideoClips import Clipper,Stitcher
import os
import threading
minus_timestamp = 15
plus_timestamp = 30
def process_data():
    link1 = link1_entry.get()
    link2 = link2_entry.get()
    num_clips = num_clips_entry.get()
    captions = captions_var.get()
    manual_timestamp = timestamp_entry.get()

    # Your code for processing data goes here
    # Use link1, link2, num_clips, and captions as needed
    print(f"Link 1: {link1}")
    print(f"Link 2: {link2}")
    #https://www.youtube.com/watch?v=J3-m7dAL_cY #red dead
    # https://www.youtube.com/watch?v=a60UewomiCg
    #vid https://www.youtube.com/watch?v=OSEds3luvAg
    YouTube(link1).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/YTV.mp4')
    #MC https://www.youtube.com/watch?v=ZkHKGWKq9mY
    if manual_timestamp:
        timestamp = int(manual_timestamp)
    else: 
        print("getting video duration")
        vid_duration = Clipper.Video_duration(link1)
        print(vid_duration)
        #data = Clipper.getDataFromFile("heatmap.txt")
        data = Clipper.getHeatmap(link1)
        dataPointsArray = Clipper.preProcessData(data)
        print(dataPointsArray)
        highest_point = Clipper.plotCurve(dataPointsArray, vid_duration, N=num_clips)
        print("Highest point coordinates:", highest_point)
        timestamp = highest_point[0]

    print("downloading video")
    Clipper.download(link1,minus_timestamp, timestamp,plus_timestamp)
    if not link2:
        #use repo of other fun videos
        pass

    if not os.path.exists("Source_videos/MCV.mp4"):
        YouTube(link2).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')
    else:
        print("MC_video already exists, using that one")

    # MYVIDEO = "Source_videos/YTV"
    # MCVIDEO = 'Source_videos/MCV'

    MYVIDEO = "Source_videos/YTV.mp4"
    MCVIDEO = "Source_videos/MCV.mp4"
    stitcher = Stitcher(MYVIDEO,MCVIDEO)
    # stitcher.Clip(30, timestamp,30)
    print("=========1==========")
    stitcher.Crop_stitch()
    print("=========2==========")
    stitcher.Audio()
    print("=========3==========")

    print(f"Number of Clips: {num_clips}")
    print(f"Captions: {captions}")
    print(f"Timestamp: {timestamp}")
    print("Data processed!")

    if captions == True:
        model_path = "base.en"
        video_path = "finalvid.mp4"
        output_video_path = "outputvideos/output.mp4"
        transcriber = VideoTranscriber(model_path, video_path)
        transcriber.extract_audio()
        transcriber.transcribe_video()
        transcriber.create_video(output_video_path)

def start_process_data_function():
    t1 = threading.Thread(target=process_data, name="t1")
    t1.start()
    t1.join()


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Monkey!")
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
    create_button = ttk.Button(root, text="Create", command=start_process_data_function)
    create_button.grid(row=5, column=0, columnspan=2, pady=20)

    # Start the main loop
    root.mainloop()
