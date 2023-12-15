import cv2
import sklearn
import numpy as np
import pandas as pd

  
# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture('MC_Video/videoplayback.mp4')
cap2 = cv2.VideoCapture('MC_Video/Meghan Trainor - All About That Bass (Official Video).mp4')
  
# Check if camera opened successfully 
if (cap.isOpened()== False): 
    print("Error opening video file") 
  
# Read until video is completed 
while(cap.isOpened()): 
      
# Capture frame-by-frame 
    ret, frame = cap.read()
    ret2,frame2 = cap2.read()
    if ret == True: 
    # Display the resulting frame 
        #aspect ratio 16:9
        frame = cv2.resize(frame,(620,240), interpolation = cv2.INTER_LINEAR)
        # frame = frame[240:500, 40:460]

        frame2 = cv2.resize(frame2,(620,480), interpolation = cv2.INTER_LINEAR)


        frame_out = np.concatenate((frame2, frame), axis=0)
        frame_out = cv2.putText(frame_out,"Test",org=(310,480),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1,color=(255, 0, 0),thickness=2)
        cv2.imshow('Frame', frame_out) 
          
    # Press Q on keyboard to exit 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
  
# Break the loop 
    else: 
        break
  
# When everything done, release 
# the video capture object 
cap.release() 
  
# Closes all the frames 
cv2.destroyAllWindows() 