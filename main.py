import cv2
from moviepy.editor import *
import numpy as np
import whisper

print("test")

class Stitcher:
    def __init__(self,main_video,minecraft_video):
        self.main_video = main_video
        self.minecraft_video = minecraft_video

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.result = cv2.VideoWriter("testvid.mp4", fourcc, 25.0, (360,640))

    def Clipper(self,minus_timestamp, timestamp,plus_timestamp):

        timestamp-minus_timestamp,timestamp+plus_timestamp
        
        video = VideoFileClip(self.main_video).subclip(timestamp-minus_timestamp,timestamp+plus_timestamp)
        video.write_videofile("ClippedVideo.mp4",fps=25) # Many options...

    def Crop_stitch(self):
        cap = cv2.VideoCapture(self.minecraft_video)
        cap2 = cv2.VideoCapture('ClippedVideo.mp4')
        if (cap2.isOpened()== False): 
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
                frame = frame[200:880, 0:1920]
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

    def Audio(self):
        video_clip = VideoFileClip("testvid.mp4")
        audio_clip = AudioFileClip(self.main_video)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("finalvid" + ".mp4")


# MYVIDEO = "MC_Video/I Found A New AI Business That No One Knows! (TikTok Automation!).mp4"
# MCVIDEO = 'MC_Video/6 Minutes Minecraft Shader Parkour Gameplay (Night-Time) [Free to Use] [Map Download].mp4'

# Clipper(MYVIDEO)
# print("=========1==========")
# Crop_stitch(MCVIDEO)
# print("=========2==========")
# Audio()
# print("=========3==========")

