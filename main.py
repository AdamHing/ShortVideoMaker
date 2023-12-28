from typing import Optional
from pytube import YouTube
from moviepy.editor import *
import os
import threading
from VideoClips import Clipper,Stitcher
from dynamic_subtitles import DynamicSubtitles


from models.post import UserPost
from queue import Queue 
from fastapi import FastAPI

MYVIDEO = "Source_videos/ClippedVideo.mp4" #top video
MCVIDEO = "Source_videos/MCV.mp4" #botton video
stitched_video_no_audio_path = "temp/StitchedVideo_no_audio.mp4"
# name and location of stitched video with audio file. 
stitched_video_with_audio_path = "temp/StitchedVideo_with_audio.mp4"
output_video_path = "outputvideos/output.mp4"
watermarkPath = "img/watermark.png"
minus_timestamp = 15
plus_timestamp = 30

def process_data(link1,link2,manual_timestamp,captions):
    if manual_timestamp:
        print("using manual_timestamp")
        timestamp = int(manual_timestamp)
    elif "www.youtube.com" in link1:
        print("getting video duration")
        #get length of video
        vid_duration = YouTube(link1).length
        print(vid_duration)
        #data = Clipper.getDataFromFile("heatmap.txt")
        data = Clipper.getHeatmap(link1)
        print(data)
        dataPointsArray = Clipper.preProcessData(data)
        highest_point = Clipper.plotCurve(dataPointsArray, vid_duration)
        print("Highest point coordinates:", highest_point)
        timestamp = highest_point[0]
    Clipper.download(link1,minus_timestamp, timestamp,plus_timestamp)

    if link2:
        YouTube(link2).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')
    if not os.path.exists("Source_videos/MCV.mp4"):
        #backup default video
        YouTube("https://www.youtube.com/watch?v=ZkHKGWKq9mY").streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')
    else:
        print("MC_video already exists, using that one")

    stitcher = Stitcher(MYVIDEO,MCVIDEO)
    print("=========1==========")
    stitcher.Crop_stitch()
    print("=========2==========")
    stitcher.Audio_watermark(stitched_video_no_audio_path,watermarkPath,stitched_video_with_audio_path)
    print("=========3==========")
    print(f"Captions: {captions}")
    print(f"Timestamp: {timestamp}")
    print("Data processed!")
    if captions == True:
        DynamicSubtitles(stitched_video_with_audio_path)

app = FastAPI()
@app.get("/form/")
async def read_item(main_vid: str, peripheral_vid: Optional[str] = None, time_stamp: Optional[int] = None, captions: Optional[bool]= None):
    print(f"Received request with main_vid={main_vid}, peripheral_vid={peripheral_vid}, time_stamp={time_stamp}, captions={captions}")
    return {"main_vid": main_vid, "peripheral_vid": peripheral_vid,"time_stamp": time_stamp, "captions": captions}

if __name__ =="__main__":
    t1 = threading.Thread(target=process_data, args=(10,))
    # t2 = threading.Thread(target=api, args=(10,))
    t1.start()
    # t2.start()
    t1.join()
    # t2.join()
    print("Done!")

# uvicorn main:app --reload