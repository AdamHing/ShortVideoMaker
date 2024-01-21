import numpy as np
import cv2
from moviepy.editor import *
import numpy as np
import yt_dlp
from yt_dlp.utils import download_range_func
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome  import ChromeDriverManager
 

options = Options()
options.add_argument('--headless')


#get url
#use url to get heatmap
#get length of video
#use that script to get timestamp
# return status of everyfunction as it runs
class Clipper():
    def __init__(self, main_vid_url):
        self.main_vid_url = main_vid_url
        #self.ClipsPerVideo = ClipsPerVideo # ClipsPerVideo is not supported at this time

    def get_most_rewatched_timestamp(self, video_duration):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        time.sleep(2)
        driver.get(self.main_vid_url)
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        heatmap = soup.find("path", {"class": "ytp-heat-map-path"}).get('d')
        heatmap = heatmap.replace("M 0.0,100.0 ","")

        tripletsArray = heatmap.split("C ")
        dataPointsArray = []
        for triplets in tripletsArray:
            if triplets != "":
                pointsArray = triplets.split(" ")[:3]
                for points in pointsArray:
                    p = points.split(",")
                    dataPointsArray.append([float(p[0]), float(p[1])])

        x = [((p[0] - 1) * (video_duration) / (1000 - 1)) for p in dataPointsArray]
        y = [-p[1] for p in dataPointsArray]

        max_point_index = y.index(max(y))
        highest_point = (x[max_point_index],y[max_point_index])
        return highest_point
        

    def download(self,minus_timestamp,timestamp, plus_timestamp):
        start_time = timestamp-minus_timestamp
        end_time = timestamp+plus_timestamp
        # start_time = 2  # accepts decimal value like 2.3
        # end_time = 7  
        yt_opts = {
            #"format": "mp4[height=720]",
            "format": "best",
            'verbose': True,
            'download_ranges': download_range_func(None, [(start_time, end_time)]),
            'force_keyframes_at_cuts': True,
            'outtmpl': os.path.join("Source_videos/ClippedVideo.mp4"),
        }
        
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download(self.main_vid_url)

    #not required
    def seconds_to_hms(seconds): 
        seconds = seconds[0]
        print(type(seconds))
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return hours, minutes, remaining_seconds   

class Stitcher:
    def __init__(self,main_video,fun_video):
        self.main_video = main_video
        self.fun_video = fun_video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vidcap = cv2.VideoCapture(self.main_video)
        self.fps = vidcap.get(cv2.CAP_PROP_FPS)
        self.result = cv2.VideoWriter("temp/stitchedVideo_no_audio.mp4", fourcc, self.fps, (360,640))

    #depricated 
    #used to clip full length mp4 videos
    def Clip(self,minus_timestamp, timestamp,plus_timestamp):
        timestamp-minus_timestamp,timestamp+plus_timestamp
        video = VideoFileClip(self.main_video).subclip(timestamp-minus_timestamp,timestamp+plus_timestamp)
        video.write_videofile(self.main_video,fps=self.fps) # Many options...

    def Crop_stitch(self):
        cap = cv2.VideoCapture(self.fun_video) #BOTTOM VIDEO
        cap2 = cv2.VideoCapture(self.main_video) #TOP VIDEO
        if (cap2.isOpened() == False): 
            print("Error opening video file") 
        # Read until video is completed 
        while(cap2.isOpened()): 
        # Capture frame-by-frame 
            ret, frame = cap.read()
            ret2,frame2 = cap2.read()
            if ret2 == True: 
                #print(frame.shape)#(1080, 1920, 3)
                #print(frame2.shape)#(720, 1280, 3)
                frame2 = cv2.resize(frame2,(360,384), interpolation = cv2.INTER_LINEAR)
                #frame = frame[200:880, 0:1920]
                frame = cv2.resize(frame,(360,256), interpolation = cv2.INTER_LINEAR)
                frame_out = np.concatenate((frame2, frame), axis=0)
                #frame_out = cv2.putText(frame_out,"Test",org=(310,480),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1,color=(255, 0, 0),thickness=2)
                # cv2.imshow('Frame', frame_out) 
                self.result.write(frame_out)
            # Press Q on keyboard to exit 
                if cv2.waitKey(25) & 0xFF == ord('q'): 
                    break
        # Break the loop 
            else: 
                break
        # When everything done, release 
        # the video capture object 
        self.result.release()
        cap.release() 
        cv2.destroyAllWindows()

    def Audio_watermark(self,StitchedVideoNoAudio,watermarkPath,StitchedVideo_W_audio_PATH):
        video_clip = VideoFileClip(StitchedVideoNoAudio)
        #add watermark 
        logo = (ImageClip(watermarkPath)
                .set_duration(video_clip.duration)
                .resize(height=50) # if you need to resize...
                .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
                .set_pos(("right","top")))
        video_clip = CompositeVideoClip([video_clip,logo])

        audio_clip = AudioFileClip(self.main_video)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(StitchedVideo_W_audio_PATH)
