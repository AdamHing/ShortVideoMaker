from pytube import YouTube
#from main import Stitcher
from moviepy.editor import *
import os
from VideoClips import Clipper,Stitcher
from subtitle_generators.dynamic_subtitles import DynamicSubtitles
class main:
    def __init__(self,main_link,peripheral_link,watermark_path,captions,manual_timestamp=False):
        self.main_link = main_link
        self.peripheral_link = peripheral_link
        self.watermark_path = watermark_path
        self.captions = captions
        self.manual_timestamp = manual_timestamp
        # self.num_clips = num_clips
        self.tmp_folder = "tmp"
        self.minus_timestamp = 15
        self.plus_timestamp = 30

        # peripheral_video_list = [
        #     "https://www.youtube.com/watch?v=Ujvy-DEA-UM",
        #     "https://www.youtube.com/watch?v=ZkHKGWKq9mY",
        #     "https://www.youtube.com/watch?v=JwP6sCqmPAs"
        #                          ]

    def process_data(self):
        # Your code for processing data goes here
        # Use link1, link2, num_clips, and captions as needed
        print(f"Link 1: {self.main_link}")
        print(f"Link 2: {self.peripheral_link}")

        clipper = Clipper(self.main_link)
        if self.manual_timestamp:
            print("using manual_timestamp")
            timestamp = int(self.manual_timestamp)
        elif "www.youtube.com" in self.main_link:
            timestamp = clipper.get_most_rewatched_timestamp()
            print("Highest point at {}s:".format(timestamp))

        else:
            return "could not get timestamp"

        clipper.download(self.minus_timestamp, timestamp,self.plus_timestamp)

        # if "www.youtube.com" in link1:
        #     print("downloading video")
        #     Clipper.download(link1,minus_timestamp, timestamp,plus_timestamp)
        # else:
        #     print("link not valid, using local video")
        #     MYVIDEO="Source_videos/"+link1+"mp4"
        peripheral_video = self.tmp_folder+"/MCV.mp4"
        if self.peripheral_link:
            YouTube(self.peripheral_link,use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=peripheral_video)
        if not os.path.isfile(peripheral_video):
            YouTube("https://www.youtube.com/watch?v=Ujvy-DEA-UM",use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=peripheral_video)
        else:
            print("MC_video already exists, using that one")

        stitcher = Stitcher(self.tmp_folder+"/ClippedVideo.mp4",peripheral_video)
        # stitcher.Clip(30, timestamp,30)

        print("=========1==========")
        stitcher.Crop_stitch()
        print("=========2==========")
        stitcher.Audio_watermark(self.tmp_folder+"/StitchedVideo_no_audio.mp4",self.watermark_path,self.tmp_folder+"/StitchedVideo_with_audio.mp4")
        print("=========3==========")
        print(f"Number of Clips: {self.num_clips}")
        print(f"Captions: {self.captions}")
        print(f"Timestamp: {timestamp}")
        print("Data processed!")

        if self.captions == True:
            DynamicSubtitles(self.tmp_folder+"/StitchedVideo_with_audio.mp4",self.tmp_folder)

        status="compleated"
        return status


#this is only used if you want to run this without lambda function

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("main_link")
#     parser.add_argument("peripheral_link") #optional
#     parser.add_argument("watermark_path") #optional
#     parser.add_argument("captions") #optional
#     parser.add_argument("manual_timestamp") #optional
#     parser.add_argument("num_clips") #optional
#     args = parser.parse_args()

#     process_data(args.main_link,args.peripheral_link,args.watermark_location,args.captions,args.manual_timestamp,args.num_clips)

# if __name__ == 'main':
#     main()




