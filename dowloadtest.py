from pytube import YouTube
link1 =  "https://www.youtube.com/watch?v=OSEds3luvAg" # main vid
YouTube(link1).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/YTV.mp4')
link2 = "https://www.youtube.com/watch?v=ZkHKGWKq9mY" # mc vid
YouTube(link2).streams.filter(progressive=True, file_extension='mp4').first().download(filename='Source_videos/MCV.mp4')