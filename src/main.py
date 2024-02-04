
#from BlackSubtitles import VideoTranscriber
from pytube import YouTube
#from main import Stitcher
from moviepy.editor import *
import os
from VideoClips import Clipper,Stitcher
from subtitle_generators.dynamic_subtitles import DynamicSubtitles
import os
import argparse


#environment variables
MYVIDEO = "Source_videos/ClippedVideo.mp4" #top video
MCVIDEO = "Source_videos/MCV.mp4" #botton video
stitched_video_no_audio_path = "temp/StitchedVideo_no_audio.mp4"
# name and location of stitched video with audio file. 
stitched_video_with_audio_path = "temp/StitchedVideo_with_audio.mp4"
output_video_path = "outputvideos/output.mp4"
watermark_path = "img/watermark.png"
minus_timestamp = 15
plus_timestamp = 30

def process_data(main_link,peripheral_link,watermark_path,captions,manual_timestamp, num_clips):
    # Your code for processing data goes here
    # Use link1, link2, num_clips, and captions as needed
    print(f"Link 1: {main_link}")
    print(f"Link 2: {peripheral_link}")

    clipper = Clipper(main_link)
    if manual_timestamp:
        print("using manual_timestamp")
        timestamp = int(manual_timestamp)
    elif "www.youtube.com" in main_link:
        timestamp = clipper.get_most_rewatched_timestamp()
        print("Highest point at {}s:".format(timestamp))

    clipper.download(minus_timestamp, timestamp,plus_timestamp)

    # if "www.youtube.com" in link1:
    #     print("downloading video")
    #     Clipper.download(link1,minus_timestamp, timestamp,plus_timestamp)
    # else:
    #     print("link not valid, using local video")
    #     MYVIDEO="Source_videos/"+link1+"mp4"
    if peripheral_link:
        YouTube(peripheral_link).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')
    if not os.path.exists("Source_videos/MCV.mp4"):
        YouTube("https://www.youtube.com/watch?v=ZkHKGWKq9mY").streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')
    else:
        print("MC_video already exists, using that one")

    stitcher = Stitcher(MYVIDEO,MCVIDEO)
    # stitcher.Clip(30, timestamp,30)

    print("=========1==========")
    stitcher.Crop_stitch()
    print("=========2==========")
    stitcher.Audio_watermark(stitched_video_no_audio_path,watermark_path,stitched_video_with_audio_path)
    print("=========3==========")
    print(f"Number of Clips: {num_clips}")
    print(f"Captions: {captions}")
    print(f"Timestamp: {timestamp}")
    print("Data processed!")

    if captions == True:
        DynamicSubtitles(stitched_video_with_audio_path)

    status="compleated"
    return status


#this is only used if you want to run this without lambda function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("main_link")
    parser.add_argument("peripheral_link") #optional
    parser.add_argument("watermark_path") #optional
    parser.add_argument("captions") #optional
    parser.add_argument("manual_timestamp") #optional
    parser.add_argument("num_clips") #optional
    args = parser.parse_args()

    process_data(args.main_link,args.peripheral_link,args.watermark_location,args.captions,args.manual_timestamp,args.num_clips)

if __name__ == 'main':
    main()




